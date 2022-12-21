import os
import json

from typing import Iterable, Any

from .output import Output, Config, LogFormat

from typings.work_path import WorkPath
from typings.error import OutputSessionError


class Parser(Output):
    _session = None

    def __init__(self, log_path: WorkPath, log_format: LogFormat = LogFormat.JSON_LINE):
        super().__init__(log_path, log_format)

    def __enter__(self):
        self._session = self.out_path
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session = None

    def _read_json(self, filename: str) -> Config:
        if self._session is None:
            raise OutputSessionError

        filepath = self._session.to_file(filename)
        with open(filepath, 'r') as handle:
            return json.load(handle)

    def config(self, filename: str = 'config.json') -> Config:
        return self._read_json(filename)

    def read(self, filename: str) -> Iterable[str]:
        if self._session is None:
            raise OutputSessionError

        filepath = self._session.to_file(filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as handle:
                for line in iter(handle.readline, ''):
                    yield line

    def parse(self, *args, **kwargs) -> Any:
        raise NotImplementedError


__all__ = [
    'Parser'
]
