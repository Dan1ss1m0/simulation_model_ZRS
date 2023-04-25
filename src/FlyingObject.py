import numpy as np

from misc import *
from typing import List, Union, Tuple


class FlyingObject:

    def __init__(self, position: Union[list, tuple, np.ndarray],
                 velocity: Union[list, tuple, np.ndarray]):

        self.position = position if isinstance(position, np.ndarray) else np.array(position, dtype=np.float64)
        self.velocity = velocity if isinstance(velocity, np.ndarray) else np.array(velocity, dtype=np.float64)


class Target(FlyingObject):

    def __init__(self, id: int, **kwargs):

        super().__init__(**kwargs)
        self.destroyed = False
        self.id = id

        self.update_functions = [self._update_position]

    def _update_position(self, time_step: float):

        self.position += self.velocity * time_step

    def update(self, time_step):

        for func in self.update_functions:
            func(time_step)


class TargetAccelerating(Target):

    def __init__(self, acceleration, **kwargs):

        super().__init__(**kwargs)
        self.acceleration = (acceleration if isinstance(acceleration, np.ndarray) else np.array(acceleration, dtype=np.float64))

        self.update_functions.append(self._update_velocity)

    def _update_position(self, time_step: float):

        self.position += self.velocity * time_step + self.acceleration * time_step ** 2 / 2

    def _update_velocity(self, time_step):

        self.velocity += self.acceleration * time_step


class TargetCircled(Target):

    def __init__(self, center, **kwargs):

        super().__init__(**kwargs)
        self.center = center

        assert self.velocity[1] == 0

        self.R = np.sqrt((self.position[0] - self.center[0]) ** 2 + (self.position[2] - self.center[2]) ** 2)
        self.angle = np.arccos((self.position[0] - self.center[0]) / self.R)

        if np.arcsin((self.position[2] - self.center[2]) / self.R) != self.angle:
            self.angle *= -1.

        self.angular_velocity = np.sqrt(np.sum(self.velocity ** 2)) / self.R
        if self.velocity[2]:
            self.angular_velocity *= np.sign(-(self.center[0] - self.position[0]) / self.velocity[2])
        else:
            self.angular_velocity *= np.sign((self.center[2] - self.position[2]) / self.velocity[0])

        print(self.R, self.angle, self.angular_velocity)

    def _update_position(self, time_step: float):

        self.angle += time_step * self.angular_velocity
        self.position[0] = self.R * np.cos(self.angle) + self.center[0]
        self.position[2] = self.R * np.sin(self.angle) + self.center[2]


