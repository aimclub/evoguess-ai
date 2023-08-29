import os
import re

from time import time as now
from pysat import formula as fml
from tempfile import NamedTemporaryFile as NTFile
from subprocess import Popen, TimeoutExpired, PIPE

from util.iterable import concat

from ..solver import Report, Solver, IncrSolver

from instance.module.encoding import Formula
from function.module.budget import KeyLimit, UNLIMITED
from typings.searchable import Constraints, Supplements

STATUSES = {
    10: True,
    20: False
}


def source(formula: fml.CNF) -> bytes:
    return ''.join([
        f'p cnf {formula.nv} {len(formula.clauses)}\n',
        *(' '.join(map(str, c)) + ' 0\n' for c in formula.clauses)
    ]).encode()


class External(Solver):
    limits = {}
    statistic = {}
    stdin_file = None
    stdout_file = None
    executable_file = None

    solution = re.compile(r'^v ([-\d ]*)', re.MULTILINE)

    def __init__(self, from_executable: str):
        self.from_executable = from_executable

    def use_incremental(self, formula: Formula,
                        constraints: Constraints = ()) -> IncrSolver:
        raise RuntimeError('External solvers supports only solve procedure')

    def solve(self, formula: Formula, supplements: Supplements,
              limit: KeyLimit = UNLIMITED, add_model: bool = False) -> Report:
        files, launch_args = [], [self.from_executable]
        assumptions, constraints = supplements

        if isinstance(formula, fml.CNF):
            formula.extend(constraints + [[lit] for lit in assumptions])
        else:
            raise TypeError('External solvers works only with CNF or CNF+ encodings')

        if self.stdin_file is not None:
            with NTFile(delete=False) as in_file:
                formula.to_fp(in_file)
                files.append(in_file.name)
                launch_args.append(self.stdin_file % in_file.name)

        if self.stdout_file is not None:
            with NTFile(delete=False) as out_file:
                files.append(out_file.name)
                launch_args.append(self.stdout_file % out_file.name)

        timeout, (key, value) = None, limit
        if value is not None and key == 'time':
            timeout = value + len(formula.clauses) * 6e-08
        if value is not None and key in self.limits:
            launch_args.append(self.limits[key] % value)

        timestamp, process = now(), Popen(
            launch_args, stdin=PIPE, stdout=PIPE, stderr=PIPE
        )
        try:
            data = None if self.stdin_file else source(formula)
            output, error = process.communicate(data, timeout)
            # todo: handle error

            if self.stdout_file is not None:
                with open(files[-1], 'r+') as handle:
                    output = handle.read()
            else:
                output = output.decode()

            stats = {'time': now() - timestamp}
            for key, pattern in self.statistic.items():
                result = pattern.search(output)
                stats[key] = result and int(result.group(1))

            status = STATUSES.get(process.returncode)
            solution = concat(*[
                [int(var) for var in line.split()]
                for line in self.solution.findall(output)
            ]) if add_model and status else None
        except TimeoutExpired:
            process.terminate()
            status, solution = None, None
            stats = {'time': now() - timestamp}
        finally:
            [os.remove(file) for file in files]

        return Report(status, stats, solution)

    def propagate(self, formula: Formula, supplements: Supplements) -> Report:
        raise RuntimeError('External solvers supports only solve procedure')


class Kissat(External):
    slug = 'solver:ext:kissat'

    stdin_file = None
    stdout_file = None
    limits = {
        'time': '--time=%d',
        'conflicts': '--conflicts=%d',
        'decisions': '--decisions=%d',
    }
    statistic = {
        'restarts': re.compile(r'^c restarts:\s+(\d+)', re.MULTILINE),
        'conflicts': re.compile(r'^c conflicts:\s+(\d+)', re.MULTILINE),
        'decisions': re.compile(r'^c decisions:\s+(\d+)', re.MULTILINE),
        'propagations': re.compile(r'^c propagations:\s+(\d+)', re.MULTILINE),
        'learned_literals': re.compile(r'^c clauses_learned:\s+(\d+)', re.MULTILINE),
    }


class MinisatCS(External):
    slug = 'solver:ext:minisat_cs'

    stdin_file = f'%s'
    # stdout_file = f'%s'
    stdout_file = None
    limits = {}
    statistic = {
        'restarts': re.compile(r'^restarts\s+:\s+(\d+)', re.MULTILINE),
        'conflicts': re.compile(r'^conflicts\s+:\s+(\d+)', re.MULTILINE),
        'decisions': re.compile(r'^decisions\s+:\s+(\d+)', re.MULTILINE),
        'propagations': re.compile(r'^propagations\s+:\s+(\d+)', re.MULTILINE),
        'learned_literals': re.compile(r'^conflict literals\s+:\s+(\d+)', re.MULTILINE),
    }


__all__ = [
    'Kissat',
    'MinisatCS'
]
