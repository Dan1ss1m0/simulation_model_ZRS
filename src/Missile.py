from lib import *

class Missile:
    def __init__(self, missile_pos, target_pos, target_ID, missile_speed): # должна быть в private
        self.missile_pos = missile_pos
        self.target_pos = target_pos
        self.target_ID = target_ID
        self.missile_speed = missile_speed #скаляр
        self.exploded = False
        
        self.direction = (target_pos - missile_pos).normalize()
        
        # output:
        self.log_position.insert(missile_pos) #вектор положений, проходимых ракетой
    
    def update(self): # должна быть в public
        e = 0.001
        if ((target_pos - missile_pos) <= e):
            self.exploded = True
        self.direction = (target_pos - missile_pos).normalize()
        self.missile_pos = self.direction * self.missile_speed * time_step
        if (scalar_prod(direction, (target_pos - missile_pos)) <= 0):
            # self.missile_pos = target_pos #???
            self.exploded = True
        self.log_position.insert(missile_pos)
    
    def __del__(self):
        pass