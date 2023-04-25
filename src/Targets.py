from FlyingObject import FlyingObject
import numpy as np


class Target(FlyingObject):

    def __init__(self, id: int, **kwargs):

        super().__init__(**kwargs)
        self.destroyed = False
        self.id = id


class TargetAccelerating(Target):

    def __init__(self, acceleration, **kwargs):

        super().__init__(**kwargs)
        self.acceleration = (acceleration if isinstance(acceleration, np.ndarray) else np.array(acceleration, dtype=np.float64))

        self.update_time_only_functions.append(self._update_velocity)

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

    def _update_position(self, time_step: float):

        self.angle += time_step * self.angular_velocity
        self.position[0] = self.R * np.cos(self.angle) + self.center[0]
        self.position[2] = self.R * np.sin(self.angle) + self.center[2]


target_typename_to_class = {
    'simple target': Target,
    'accelerating target': TargetAccelerating,
    'circled target': TargetCircled
}
