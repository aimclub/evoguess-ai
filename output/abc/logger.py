import os
import json

from time import sleep
from typing import Any, Dict
from datetime import datetime

from util.work_path import WorkPath
from typings.error import OutputSessionError

from .output import Output, LogFormat, Config


def date_now() -> str:
    return datetime.today().strftime("%Y.%m.%d-%H:%M:%S")


class Logger(Output):
    _name = None
    _session = None

    def __init__(self, out_path: WorkPath, log_format: LogFormat = LogFormat.JSON_LINE):
        super().__init__(out_path, log_format)

    def __enter__(self):
        session = None
        path = str(self.out_path)
        name = f'{date_now()}_?'
        while session is None:
            try:
                os.mkdir(os.path.join(path, name))
                session = self.out_path.to_path(name)
            except FileExistsError:
                name = sleep(1) or f'{date_now()}_?'

        self._session = session
        self._name = name
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        path = self._session.base
        name = self._name.replace('?', date_now())
        os.rename(path, path.replace(self._name, name))
        self._session, self._name = None, None

    def _write(self, string: str, filename: str) -> 'Logger':
        if self._session is None:
            raise OutputSessionError

        filepath = self._session.to_file(filename)
        with open(filepath, 'a+') as handle:
            handle.write(string)
        return self

    def _format(self, obj: Dict[str, Any], filename: str) -> 'Logger':
        if self.log_format == LogFormat.JSON_LINE:
            return self._write(f'{json.dumps(obj)}\n', filename)
        else:
            raise NotImplementedError

    def config(self, config: Config, filename: str = 'config.json') -> 'Logger':
        return self._write(json.dumps(config, indent=2), filename)

    def write(self, *args: Any, **kwargs: Any) -> 'Logger':
        raise NotImplementedError

    # def debug(self, verbosity: int, level: int, *strings: str):
    #     if self.debug_verb >= verbosity:
    #         prefix = f"{datetime.datetime.today()} --{'--' * level}"
    #         strings = [f'{prefix} {string}' for string in strings]
    #         return self.write('debug', *strings)
    #     return self


__all__ = [
    'Logger'
]
