from . import mutation, crossover, selection

modules = {
    **mutation.impls,
    **crossover.impls,
    **selection.impls,
}
