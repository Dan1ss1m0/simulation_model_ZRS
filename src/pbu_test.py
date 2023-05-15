from Environment import Environment

environment = Environment(None)
from Launcher import Launcher
from pbu2 import Pbu

launcher_pos = (0, 0, 0)
missile_amount = 5
pos = (50,50,50)
add_distance = 1
pbu = Pbu(None, add_distance)

pbu.add_launchers(**dict(id=0, launcher_pos=launcher_pos, missile_amount=missile_amount))


print(pbu.add_target(pos,environment))
print(pbu.clear_exploded(0))