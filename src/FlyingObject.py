from misc import *
from typing import List, Union, Tuple


class FlyingObject:

    def __init__(self, position: Union[list, tuple, Position], velocity: Union[list, tuple, Velocity]):

        self.position = position if isinstance(position, Position) else Position(*position)
        self.velocity = velocity if isinstance(velocity, Velocity) else Velocity(*velocity)


class
