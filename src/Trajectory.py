import numpy as np


class Trajectory:

    def __init__(self, position):
        self.position = position
        self.update_time_only_functions = [self._update_position]

    def _update_position(self, time_step: float):
        pass

    def update(self, time_step):

        for func in self.update_time_only_functions:
            func(time_step)


class TrajectoryUniform(Trajectory):

    def __init__(self, position, velocity):

        super().__init__(position)
        self.velocity = velocity

    def _update_position(self, time_step: float):

        self.position += self.velocity * time_step


class TrajectoryAccelerating(Trajectory):

    def __init__(self, position, velocity, acceleration):

        super().__init__(position)
        self.velocity = velocity
        self.acceleration = acceleration

        self.update_time_only_functions.append(self._update_velocity)

    def _update_position(self, time_step: float):
        self.position += self.velocity * time_step + self.acceleration * time_step ** 2 / 2

    def _update_velocity(self, time_step):
        self.velocity += self.acceleration * time_step


class TrajectoryCircled(Trajectory):

    def __init__(self, position, center, velocity):

        super().__init__(position)

        self.center = center
        self.velocity = velocity

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


class TrajectoryComplex(Trajectory):

    def __init__(self, position, trajectories):

        super().__init__(position)
        self.current_trajectory_number = -1
        self.trajectories = trajectories
        self.time_passed = 0
        self._change_trajectory()

    def _change_trajectory(self):

        self.current_trajectory_number = (self.current_trajectory_number + 1) % len(self.trajectories)
        self.trajectory_duration, trajectory_name, trajectory_arguments = self.trajectories[self.current_trajectory_number]
        self.current_trajectory = trajectory_typename_to_class[trajectory_name](**trajectory_arguments)

    def update(self, time_step):

        super().update(time_step)
        self.time_passed += time_step

        if self.time_passed >= self.trajectory_duration:
            self._change_trajectory()
            self.time_passed = 0


trajectory_typename_to_class = {
    'uniform': TrajectoryUniform,
    'accelerating': TrajectoryAccelerating,
    'circled': TrajectoryCircled
}
