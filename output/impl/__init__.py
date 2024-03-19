from .logger_none import NoneLogger
from .logger_combine import CombineLogger
from .logger_optimize import OptimizeLogger
from .parser_optimize import OptimizeParser

outputs = {
    # loggers
    NoneLogger.slug: NoneLogger,
    CombineLogger.slug: CombineLogger,
    OptimizeLogger.slug: OptimizeLogger,
    # parsers
    OptimizeParser.slug: OptimizeParser
}

__all__ = [
    'outputs',
    # loggers
    'NoneLogger',
    'CombineLogger',
    'OptimizeLogger',
    # parsers
    'OptimizeParser'
]
