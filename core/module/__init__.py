from . import sampling, limitation, comparator

modules = {
    **sampling.impls,
    **comparator.impls,
    **limitation.impls,
}
