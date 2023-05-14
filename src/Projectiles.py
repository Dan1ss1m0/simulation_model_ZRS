import numpy as np
from typing import Union
from misc import *


def calculate_velocity(position, target, max_velocity):

    r = np.sqrt(np.sum((position - target) ** 2))

    return max_velocity * (target - position) / r


class Projectile:

    def __init__(self, position: Union[list, tuple, np.ndarray],
                 target: Union[list, tuple, np.ndarray],
                 id: int,
                 trigger_distance: float,
                 explosion_range: float,
                 max_velocity: float):

        self.position = position
        self.velocity = np.array([0, 0, 0])
        self.id = id
        self.target = target if isinstance(target, np.ndarray) else np.array(target, dtype=np.float64)
        self.max_velocity = max_velocity

        self.velocity = calculate_velocity(self.position, self.target, self.max_velocity)

        self.trigger_distance = trigger_distance
        self.explosion_range = explosion_range
        self.exploded = False

        self.update_functions = [self._update_position]

    def _update_position(self, time_step: float):

        if self.exploded:
            return

        self.position += self.velocity * time_step

        if dist(self.target, self.position) < self.trigger_distance:
            self.exploded = True

    def update(self, **kwargs):

        for func in self.update_functions:
            func(**kwargs)


class GuidedMissile(Projectile):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    def update_target(self, target):  # должна вызываться ПБУ перед обновлением положения самой ракеты

        self.target = target if isinstance(target, np.ndarray) else np.array(target, dtype=np.float64)
        self.velocity = calculate_velocity(self.position, self.target, self.max_velocity)

    def update(self, **kwargs):
        self.update_target(kwargs['new_target'])
        super().update(time_step=kwargs['time_step'])


class PreemptiveMissile(Projectile):

    def __init__(self, preemption: float, **kwargs):

        super().__init__(**kwargs)
        self.prev_target = None
        self.preemption = preemption

    def update_target(self, target):
        self.prev_target = self.target
        self.target = target if isinstance(target, np.ndarray) else np.array(target, dtype=np.float64)
        self.velocity = calculate_velocity(self.position,
                                           self.target + self.preemption * (self.target - self.prev_target),
                                           self.max_velocity)

    def update(self, **kwargs):
        self.update_target(kwargs['new_target'])
        super().update(time_step=kwargs['time_step'])

projectile_typename_to_class = {
    'simple projectile': Projectile,
    'guided missile': GuidedMissile,
    'preemptive missile': PreemptiveMissile
}
