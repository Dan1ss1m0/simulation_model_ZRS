import numpy as np
from Trajectory import *


class Target:

    def __init__(self, id: int, trajectory):

        self.trajectory = trajectory
        self.position = trajectory.get_position()
        self.velocity = trajectory.get_velocity()
        self.destroyed = False
        self.id = id

    def update(self, time_step):

        self.trajectory.update(time_step)
        self.position = self.trajectory.get_position()
        self.velocity = self.trajectory.get_velocity()
