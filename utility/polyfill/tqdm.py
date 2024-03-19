import sys

from utility.format import passedh

try:  # if tqdm is installed
    from tqdm import tqdm as _tqdm


    class tqdm(_tqdm):
        def __init__(self, total, desc=None, unit='it',
                     file=sys.stdout, postfix=None):
            super().__init__(total=total, postfix=postfix,
                             desc=f'{passedh()} {desc}',
                             unit=unit, file=file)
except ImportError:
    pass


    class tqdm:
        def __init__(self, total, desc=None, unit='it',
                     file=sys.stdout, postfix=None):
            self.total, self.desc = total, desc
            self.file, self.unit = file, unit
            self.postfix = postfix

            self._progress = 0

        def _print(self):
            pass

        def __enter__(self):
            self.progress = 0

        def update(self, n: int = 1):
            self.progress += n
            self._print()

        def set_postfix_str(self, s: str):
            self.postfix = s

__all__ = [
    'tqdm'
]
