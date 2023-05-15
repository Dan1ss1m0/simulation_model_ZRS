import numpy as np


class Trajectory:

    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.update_time_only_functions = [self._update_position]

    def _update_position(self, time_step: float):
        pass

    def update(self, time_step):

        for func in self.update_time_only_functions:
            func(time_step)

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity


class TrajectoryUniform(Trajectory):

    def __init__(self, position, velocity):

        super().__init__(position, velocity)

    def _update_position(self, time_step: float):

        self.position += self.velocity * time_step

    def get_velocity(self):
        return self.velocity


class TrajectoryAccelerating(Trajectory):

    def __init__(self, position, velocity, acceleration):

        super().__init__(position, velocity)
        self.acceleration = np.array(acceleration, dtype=np.float64)

        self.update_time_only_functions.append(self._update_velocity)

    def _update_position(self, time_step: float):
        self.position += self.velocity * time_step + self.acceleration * time_step ** 2 / 2

    def _update_velocity(self, time_step):
        self.velocity += self.acceleration * time_step

    def get_velocity(self):
        return self.velocity


class TrajectoryCircled(Trajectory):

    def __init__(self, position, velocity, center):

        super().__init__(position, velocity)

        self.center = np.array(center, dtype=np.float64)

        assert self.velocity[1] == 0

        self.R = np.sqrt((self.position[0] - self.center[0]) ** 2 + (self.position[2] - self.center[2]) ** 2)
        self.angle = np.arccos((self.position[0] - self.center[0]) / self.R)

        if np.abs(np.arcsin((self.position[2] - self.center[2]) / self.R) - self.angle) > 0.001:

            self.angle *= -1.

        self.angular_velocity = np.sqrt(np.sum(self.velocity ** 2)) / self.R
        if self.velocity[2]:
            self.angular_velocity *= np.sign(-(self.center[0] - self.position[0]) / self.velocity[2])
        else:
            self.angular_velocity *= np.sign((self.center[2] - self.position[2]) / self.velocity[0])

    def _update_position(self, time_step: float):

        self.angle += time_step * self.angular_velocity

        new_position = self.position.copy()
        new_position[0] = self.R * np.cos(self.angle) + self.center[0]
        new_position[2] = self.R * np.sin(self.angle) + self.center[2]

        self.velocity = (new_position - self.position) / time_step
        self.position = new_position


class TrajectoryComplex(Trajectory):

    def __init__(self, position, trajectories):

        super().__init__(position, velocity=(0, 0, 0))
        self.current_trajectory_number = -1
        self.trajectories = trajectories
        self.time_passed = 0
        self._change_trajectory()

    def _change_trajectory(self):

        self.current_trajectory_number = (self.current_trajectory_number + 1) % len(self.trajectories)
        self.trajectory_duration, trajectory_type, trajectory_arguments = self.trajectories[self.current_trajectory_number].values()

        trajectory_arguments['position'] = self.position

        if trajectory_arguments.get('velocity', None) is None:
            trajectory_arguments['velocity'] = self.current_trajectory.velocity

        self.current_trajectory = trajectory_typename_to_class[trajectory_type](**trajectory_arguments)

    def update(self, time_step):

        self.current_trajectory.update(time_step)
        self.time_passed += time_step

        self.position = self.current_trajectory.get_position()
        self.velocity = self.current_trajectory.get_velocity()

        if self.time_passed >= self.trajectory_duration:
            self._change_trajectory()
            self.time_passed = 0


trajectory_typename_to_class = {
    'uniform': TrajectoryUniform,
    'accelerating': TrajectoryAccelerating,
    'circled': TrajectoryCircled,
    'complex': TrajectoryComplex
}
