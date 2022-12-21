class AlreadyRunning(Exception):
    pass


class CancelledError(Exception):
    pass


class OutputSessionError(Exception):
    """The Output session didn't enter."""
    pass
