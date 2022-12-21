from .instance import *
from .cipher_s import *
from .cipher_b import *

instances = {
    Instance.slug: Instance,
    BlockCipher.slug: BlockCipher,
    StreamCipher.slug: StreamCipher
}

__all__ = [
    'instances',
    # impls
    'Instance',
    'BlockCipher',
    'StreamCipher',
]
