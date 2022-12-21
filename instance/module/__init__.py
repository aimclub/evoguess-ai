from . import encoding
from . import variables

modules = {
    **encoding.impls,
    **variables.impls
}
