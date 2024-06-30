import os
import re

from threading import Timer
from time import time as now
from typing import List, Dict, Tuple
from tempfile import NamedTemporaryFile
from subprocess import PIPE, Popen, TimeoutExpired

from utility.iterable import concat
from ...variables import Supplements

from .pysat import PySatSetts, \
    FormulaError, _PySatSolver, PySatSolver
from ..solver import Report, KeyLimit, UNLIMITED
from ...encoding import PySatFormula, SatFormula, \
    MaxSatFormula, is_sat_formula, is_max_sat_formula

STATUSES = {
    10: True,
    20: False
}


def communicate(
        process: Popen, timeout: float = None
) -> Tuple[bytes, bytes]:
    timer = Timer(timeout, process.kill, ())
    try:
        timer.start()
        return b''.join(iter(process.stdout.readline, b'')), \
            b''.join(iter(process.stderr.readline, b''))
    finally:
        if timer and timer.is_alive():
            timer.cancel()


class _ExternalSolver(_PySatSolver):
    limits = {}
    statistic = {}
    stdin_file = None
    stdout_file = None
    launch_payload = []

    def __init__(
            self,
            formula: PySatFormula,
            settings: PySatSetts,
            from_executable: str,
            use_timer: bool = True,
    ):
        super().__init__(formula, settings, use_timer)
        self.from_executable = from_executable

    def _parse_stats(self, output: str) -> Dict[str, int]:
        def get_number(res):
            return res and int(res[-1])

        return {
            key: get_number(p.findall(output))
            for key, p in self.statistic.items()
        }

    def _parse_solution(self, output: str) -> List[int]:
        raise NotImplementedError

    def solve(
            self, supplements: Supplements,
            limit: KeyLimit = UNLIMITED,
            extract_model: bool = True,
    ) -> Report:
        files, source = [], None
        launch_args = [self.from_executable]
        assumptions, constraints = supplements
        launch_args.extend(self.launch_payload)

        str_clauses = [
            *map(str, assumptions),
            *(' '.join(map(str, cl))
              for cl in constraints)
        ]

        if is_sat_formula(self.formula):
            str_supplements = '\n'.join([
                f'{cl} 0' for cl in str_clauses
            ])
            formula_len = sum((
                len(str_clauses),
                len(self.formula.clauses)
            ))
        elif is_max_sat_formula(self.formula):
            str_supplements = '\n'.join([
                f'{self.formula.topw} {cl} 0'
                for cl in str_clauses
            ])
            formula_len = sum((
                len(str_clauses),
                len(self.formula.hard),
                len(self.formula.soft),
            ))
        else:
            raise FormulaError(self.formula)

        if self.stdin_file is not None:
            with NamedTemporaryFile(
                    delete=False, mode='w+'
            ) as in_file:
                files.append(in_file.name)
                self.formula.to_fp(in_file)
                in_file.write(str_supplements)
                launch_args.append(
                    self.stdin_file % in_file.name
                )
        else:
            self.formula.comments = []
            [header, source] = self.formula \
                .to_dimacs().split('\n', 1)
            header_parts = header.split(' ')
            header_parts[3] = str(formula_len)
            new_header = ' '.join(header_parts)
            source = new_header + '\n' + source
            source += f'\n{str_supplements}'

        if self.stdout_file is not None:
            with NamedTemporaryFile(
                    delete=False, mode='w+'
            ) as out_file:
                files.append(out_file.name)
                launch_args.append(
                    self.stdout_file % out_file.name
                )

        timeout, (key, value) = None, limit
        if value is not None and key == 'time':
            timeout = value + formula_len * 2e-06
        if value is not None and key in self.limits:
            launch_args.append(self.limits[key] % value)

        timestamp, process = now(), Popen(
            launch_args, stdout=PIPE, stderr=PIPE,
            stdin=PIPE if source else None
        )
        try:
            data = None if source is None else source.encode()
            if data is None and is_max_sat_formula(self.formula):
                output, error = communicate(process, timeout)
            else:
                output, error = process.communicate(data, timeout)

            # todo: handle error
            if self.stdout_file is not None:
                with open(files[-1], 'r') as handle:
                    output = handle.read()
            else:
                output = output.decode()

            stats = self._parse_stats(output)
            stats['time'] = now() - timestamp

            status = STATUSES.get(process.returncode)
            solution = self._parse_solution(output) \
                if extract_model and status else None
        except TimeoutExpired:
            process.terminate()
            status, solution = None, None
            stats = {'time': now() - timestamp}
        finally:
            [os.remove(file) for file in files]

        return Report(status, stats, solution, stats.get('cost'))


class ExternalSolver(PySatSolver):
    slug = 'solver:external'

    def __init__(self, from_executable: str, pysat_propagator: str = 'm22'):
        super().__init__(sat_name=pysat_propagator)
        self.from_executable = from_executable

    def get_instance(
            self, formula: PySatFormula, use_timer: bool = True
    ) -> _ExternalSolver:
        raise NotImplementedError


class _Kissat(_ExternalSolver):
    limits = {
        'time': '--time=%d',
        'conflicts': '--conflicts=%d',
        'decisions': '--decisions=%d',
    }
    statistic = {
        'restarts': re.compile(r'^c restarts:\s+(\d+)', re.MULTILINE),
        'conflicts': re.compile(r'^c conflicts:\s+(\d+)', re.MULTILINE),
        'decisions': re.compile(r'^c decisions:\s+(\d+)', re.MULTILINE),
        'propagations': re.compile(r'^c propagations:\s+(\d+)', re.MULTILINE)
    }

    def _parse_solution(self, output: str) -> List[int]:
        return concat(*(
            [int(var) for var in line.split()] for line in
            re.findall(r'^v ([-\d ]*)', output, re.MULTILINE)
        ))


class Kissat(ExternalSolver):
    slug = 'solver:external:kissat'

    def get_instance(
            self, formula: SatFormula, use_timer: bool = True
    ) -> _Kissat:
        return _Kissat(
            formula, self.settings, self.from_executable, use_timer
        )


class _Loandra(_ExternalSolver):
    launch_payload = [
        '-verbosity=1'
    ]
    stdin_file = '%s'
    statistic = {
        'cost': re.compile(r'^o (\d*)', re.MULTILINE)
    }

    def _parse_solution(self, output: str) -> List[int]:
        line = re.findall(r'^v \d* (\d*)', output, re.MULTILINE)[-1]
        return [i + 1 if c else -(i + 1) for i, c in enumerate(line)]


class Loandra(ExternalSolver):
    slug = 'solver:external:loandra'

    def get_instance(
            self, formula: MaxSatFormula, use_timer: bool = True
    ) -> _Loandra:
        return _Loandra(
            formula, self.settings, self.from_executable, use_timer
        )


class _Cadical(_ExternalSolver):
    launch_payload = [
        '--no-colors'
    ]
    limits = {
        'time': '-t %d',
        'conflicts': '-c %d',
        'decisions': '-d %d',
    }
    statistic = {
        'restarts': re.compile(r'^c restarts:\s+(\d+)', re.MULTILINE),
        'conflicts': re.compile(r'^c conflicts:\s+(\d+)', re.MULTILINE),
        'decisions': re.compile(r'^c decisions:\s+(\d+)', re.MULTILINE),
        'propagations': re.compile(r'^c propagations:\s+(\d+)', re.MULTILINE)
    }

    def _parse_solution(self, output: str) -> List[int]:
        return concat(*(
            [int(var) for var in line.split()] for line in
            re.findall(r'^v ([-\d ]*)', output, re.MULTILINE)
        ))


class Cadical(ExternalSolver):
    slug = 'solver:external:cadical'

    def get_instance(
            self, formula: SatFormula, use_timer: bool = True
    ) -> _Cadical:
        return _Cadical(
            formula, self.settings, self.from_executable, use_timer
        )


__all__ = [
    'Kissat',
    '_Kissat',
    'Cadical',
    '_Cadical',
    'Loandra',
    '_Loandra',
    # types
    'ExternalSolver',
    '_ExternalSolver',
]
