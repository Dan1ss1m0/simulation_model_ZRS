import numpy as np


class Position(np.ndarray):

    def length(self):

        return np.sqrt(np.sum(self ** 2))

    def __new__(cls, x, y, z, *args, **kwargs):

        res = super().__new__(cls, shape=[3], *args, **kwargs)
        res[0] = x
        res[1] = y
        res[2] = z

        return res

    def __array_finalize__(self, obj):
        pass


position = Position(1, 1, 0)

print(position + 1)
