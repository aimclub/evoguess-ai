from enum import Enum
from typing import List, Dict, Union, Any

from util.work_path import WorkPath
from typings.optional import Primitive


class LogFormat(Enum):
    [
        BINARY,
        JSON_LINE
    ] = [
        '.bin',
        '.jsonl'
    ]


Config = Dict[str, Union[Primitive, List, 'Config']]


class Output:
    slug = None

    def __init__(self, out_path: WorkPath, log_format: LogFormat):
        self.out_path = out_path
        self.log_format = log_format

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def config(self, filename: str) -> Any:
        raise NotImplementedError

    def __config__(self) -> Config:
        return {
            'slug': self.slug,
            'out_path': self.out_path,
            'log_format': self.log_format
        }


__all__ = [
    'Output',
    # types
    'Config',
    'LogFormat',
]
