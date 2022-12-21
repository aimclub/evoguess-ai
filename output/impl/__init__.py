from .logger_optimize import OptimizeLogger
from .parser_optimize import OptimizeParser

outputs = {
    # loggers
    OptimizeLogger.slug: OptimizeLogger,
    # parsers
    OptimizeParser.slug: OptimizeParser
}

__all__ = [
    'outputs',
    # loggers
    'OptimizeLogger',
    # parsers
    'OptimizeParser'
]
