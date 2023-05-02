import math 
import numpy as np
import enum

class Status(enum.Enum):
    FREE = True
    BUSY = False
    
class Target_ID:
    def __init__(self, ID):
        self.ID = ID
        
    def __del__(self):
        pass
    
    
class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
           
    def length(self):
        return ((self.x)**2 + (self.y)**2 + (self.z)**2)**(0.5)
        
    def normalize(self):
        abs = self.length()
        self.x = self.x/abs
        self.y = self.y/abs
        self.z = self.z/abs
     
    def __del__(self):
        pass
    
def scalar_prod(pos_a, pos_b):
    return (pos_a.x * pos_b.x + pos_a.y * pos_b.y + pos_a.z * pos_b.z)
    
time_step = 0.001 # такт обновления модели


class Launch_event:
    def __init__(self, missile_ID, target_pos, target_ID): # должна быть в public
        self.missile_ID = missile_ID
        self.target_pos = target_pos
        self.target_ID = target_ID
    def __del__(self):
        pass
    