from output import Logger


class Debugger:
    logger = None

    def initialize(self, logger: Logger):
        self.logger = logger

    def write(self, *strings: str) -> 'Debugger':
        self.logger._write(*strings, filename='debug.txt')
        return self


DEBUGGER = Debugger()

__all__ = [
    'DEBUGGER'
]
