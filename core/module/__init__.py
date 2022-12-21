from . import space, sampling, limitation, comparator

modules = {
    **space.impls,
    **sampling.impls,
    **comparator.impls,
    **limitation.impls,
}
