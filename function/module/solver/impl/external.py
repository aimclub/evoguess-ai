import os
import re

from time import time as now
from tempfile import NamedTemporaryFile as NTFile
from subprocess import Popen, TimeoutExpired, PIPE

from util.iterable import concat
from ..solver import Report, Solver, IncrSolver
from typings.searchable import Constraints, Supplements

from function.module.measure import Measure
from instance.module.encoding import EncodingData, CNFData

STATUSES = {
    10: True,
    20: False
}


class External(Solver):
    limits = {}
    statistic = {}
    stdin_file = None
    stdout_file = None
    executable_file = None

    solution = re.compile(r'^v ([-\d ]*)', re.MULTILINE)

    def __init__(self, from_executable: str):
        self.from_executable = from_executable

    def solve(self, encoding_data: EncodingData, measure: Measure,
              supplements: Supplements, add_model: bool = True) -> Report:
        timeout, files, launch_args = None, [], [self.from_executable]

        if isinstance(encoding_data, CNFData):
            source = encoding_data.source(supplements)
        else:
            raise TypeError('External solvers works only with CNF or CNF+ encodings')

        if self.stdin_file is not None:
            with NTFile(delete=False) as in_file:
                in_file.write(source)
                files.append(in_file.name)
                launch_args.append(self.stdin_file % in_file.name)

        if self.stdout_file is not None:
            with NTFile(delete=False) as out_file:
                files.append(out_file.name)
                launch_args.append(self.stdout_file % out_file.name)

        key, value = measure.get_budget()
        if value is not None and key == 'time':
            timeout = value + len(source) * 6e-08
        if value is not None and key in self.limits:
            launch_args.append(self.limits[key] % value)

        timestamp = now()
        process = Popen(launch_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        try:
            data = None if self.stdin_file else source.encode()
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

        # print(len(supplements[0]), status, stats['time'])
        value, status = measure.check_and_get(stats, status)
        return Report(stats['time'], value, status, solution)

    def propagate(self, encoding_data: EncodingData, measure: Measure,
                  supplements: Supplements, add_model: bool = True) -> Report:
        raise RuntimeError('External solvers supports only solve procedure')

    def use_incremental(self, encoding_data: EncodingData, measure: Measure,
                        constraints: Constraints = ()) -> IncrSolver:
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


__all__ = [
    'Kissat'
]
