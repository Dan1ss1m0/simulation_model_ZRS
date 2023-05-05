from misc import *
from typing import Union


class FlyingObject:

    def __init__(self, position: Union[list, tuple, np.ndarray],
                 velocity: Union[list, tuple, np.ndarray]):

        self.position = position if isinstance(position, np.ndarray) else np.array(position, dtype=np.float64)
        self.velocity = velocity if isinstance(velocity, np.ndarray) else np.array(velocity, dtype=np.float64)

        self.update_time_only_functions = [self._update_position]

    def _update_position(self, time_step: float):

        self.position += self.velocity * time_step

    def update(self, **kwargs):

        for func in self.update_time_only_functions:
            func(**kwargs)