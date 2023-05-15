from Environment import *
from typing import Union
class Launcher:
    def __init__(self,id: int, launcher_pos: Union[list, tuple, np.ndarray], missile_amount: int): # должна быть в public
        self.launcher_pos = launcher_pos if isinstance(launcher_pos, np.ndarray) else np.array(launcher_pos, dtype=np.float64)
        self.missile_amount = missile_amount
        self.id = id



        
    def launch(self, pos, missle_id_counter, env): # должна быть в private
        if (self.missile_amount != 0):
            self.missile_amount = self.missile_amount - 1
            speed = 20000
            env.add_projectile('guided missile',
                                       **dict(position=self.launcher_pos.copy(),
                                              target=pos,  id=missle_id_counter, trigger_distance = 10.0,
                                              explosion_range = 100.0,max_velocity = speed))
        return missle_id_counter