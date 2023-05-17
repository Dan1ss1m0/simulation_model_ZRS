from Environment import *
from typing import Union
from logs import logger

class Launcher:
    def __init__(self, id: int, launcher_pos: Union[list, tuple, np.ndarray], 
                 missile_amount: int, speed: int, missile_type: str, trigger_distance: float,
                 explosion_range: float): # должна быть в public
        self.launcher_pos = launcher_pos if isinstance(launcher_pos, np.ndarray) else np.array(launcher_pos, dtype=np.float64)
        self.missile_amount = missile_amount
        self.id = id
        self.trigger = trigger_distance
        self.explosion = explosion_range
        self.speed = speed
        self.missile_type = missile_type
        
    def launch(self, pos, missle_id_counter, env): # должна быть в private
        if (self.missile_amount != 0):
            self.missile_amount = self.missile_amount - 1
            
            env.add_projectile(self.missile_type,
                                       **dict(position=self.launcher_pos.copy(),
                                              target=pos,  id=missle_id_counter, trigger_distance = self.trigger,
                                              explosion_range = self.explosion, max_velocity = self.speed))
            logger.info(f"Launcher: add projectile with type {self.missile_type}")

        return missle_id_counter