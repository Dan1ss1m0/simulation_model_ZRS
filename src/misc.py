import numpy as np


def dist(lhs, rhs):
    return np.sqrt(np.sum((lhs - rhs) ** 2))
