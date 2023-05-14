from FlyingObject import FlyingObject
import numpy as np


class Target(FlyingObject):

    def __init__(self, id: int, **kwargs):

        super().__init__(**kwargs)
        self.destroyed = False
        self.id = id
