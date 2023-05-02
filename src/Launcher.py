from lib import *
from Missile import *

class Launcher:
    def __init__(self, launcher_pos, name, missile_amount): # должна быть в public
        self.launcher_pos = launcher_pos
        self.name = name
        self.missile_amount = missile_amount
        
        self.time = 0
        self.status = Status.FREE
        
        
        
        # input:
        self.order = []
        # output:
        self.missiles = []
        
    def missile_launch(self, target_pos, target_ID): # должна быть в private
        if (self.missile_amount != 0):
            self.missile_amount = self.missile_amount - 1
            speed = 500 # m/s
            missile = Missile(self.launcher_pos, self.target_pos, self.target_ID, speed)
            self.missiles.append(missile)
        
        
    def update(self): # должна быть в public
        self.missiles.clear()
        
        if (self.time > 0):
            self.time = self.time - time_step
            if (self.time <= 0):
                self.time = 0
                self.status = Status.FREE
        
        if ((len(self.order) != 0) and (self.status == Status.FREE)):
            self.missile_launch(self.order[0][1], self.order[0][2])
            self.order.pop(0)
            self.time = 1.0
            self.status = Status.BUSY
        
    
    def __del__(self):
        pass