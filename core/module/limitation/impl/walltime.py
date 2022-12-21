from ..limitation import *


class WallTime(Limitation):
    key = 'time'
    slug = 'limitation:time'
    time_scale = [1, 60, 60, 24]

    def __init__(self, from_string: str):
        time_units = from_string.split(':')[::-1]
        time_units = time_units[:len(self.time_scale)]

        value, acc = 0, 1
        for i in range(len(time_units)):
            acc *= self.time_scale[i]
            value += int(time_units[i]) * acc

        super().__init__(value)
        self.from_string = from_string

    def __config__(self):
        return {
            'slug': self.slug,
            'from_string': self.from_string
        }


__all__ = [
    'WallTime'
]
