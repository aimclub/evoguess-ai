from .logger_none import NoneLogger
from .logger_optimize import OptimizeLogger
from .parser_optimize import OptimizeParser

outputs = {
    # loggers
    NoneLogger.slug: NoneLogger,
    OptimizeLogger.slug: OptimizeLogger,
    # parsers
    OptimizeParser.slug: OptimizeParser
}

__all__ = [
    'outputs',
    # loggers
    'NoneLogger',
    'OptimizeLogger',
    # parsers
    'OptimizeParser'
]
