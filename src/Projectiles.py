from FlyingObject import FlyingObject
import numpy as np
from typing import Union
from misc import *


def calculate_velocity(position, target, max_velocity):

    r = np.sqrt(np.sum((position - target) ** 2))

    return max_velocity * (target - position) / r


class Projectile(FlyingObject):

    def __init__(self, position: Union[list, tuple, np.ndarray],
                 target: Union[list, tuple, np.ndarray],
                 id: int,
                 explosion_distance: float,
                 max_velocity: float):

        super().__init__(position=position, velocity=(0, 0, 0))

        self.id = id
        self.target = target if isinstance(target, np.ndarray) else np.array(target, dtype=np.float64)
        self.max_velocity = max_velocity

        self.velocity = calculate_velocity(self.position, self.target, self.max_velocity)

        self.explosion_distance = explosion_distance
        self.exploded = False

    def _update_position(self, time_step: float):

        if self.exploded:
            return

        super()._update_position(time_step)

        if dist(self.target, self.position) < self.explosion_distance:
            self.exploded = True


class GuidedMissile(Projectile):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def update_target(self, target):  # должна вызываться ПБУ перед обновлением положения самой ракеты

        self.target = target if isinstance(target, np.ndarray) else np.array(target, dtype=np.float64)
        self.velocity = calculate_velocity(self.position, self.target, self.max_velocity)

    def update(self, **kwargs):
        super().update(time_step=kwargs['time_step'])
        self.update_target(kwargs['new_target'])


class PreemptiveMissile(Projectile):

    def __init__(self, preemption: float, **kwargs):

        super().__init__(**kwargs)
        self.prev_target = None
        self.preemption = preemption
        print(self.target)

    def update_target(self, target):
        self.prev_target = self.target
        self.target = target if isinstance(target, np.ndarray) else np.array(target, dtype=np.float64)
        self.velocity = calculate_velocity(self.position,
                                           self.target + self.preemption * (self.target - self.prev_target),
                                           self.max_velocity)


projectile_typename_to_class = {
    'simple projectile': Projectile,
    'guided missile': GuidedMissile,
    'preemptive missile': PreemptiveMissile
}
