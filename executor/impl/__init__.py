from .mpi_executor import *
from .thread_executor import *
from .process_executor import *

executors = {
    MPIExecutor.slug: MPIExecutor,
    ThreadExecutor.slug: ThreadExecutor,
    ProcessExecutor.slug: ProcessExecutor,
}

__all__ = [
    'executors',
    # impls
    'MPIExecutor',
    'ThreadExecutor',
    'ProcessExecutor'
]
