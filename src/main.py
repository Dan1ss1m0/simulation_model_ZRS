from FlyingObject import *

time_step = 0.01

targets = [
    Target(position=(3, 2, 3), velocity=(-1, 0, -1), id=1),
    TargetAccelerating(position=(-1, 10, -1), velocity=(0, 0, 0), acceleration=(1, 0, 2), id=2),
    TargetCircled(position=(-1, 0, 0), velocity=(0, 0, 1), center=(0, 0, 0), id=3)
]

for i in range(1000):

    print(f"time passed: {time_step * (i + 1)}")

    for target in targets:
        target.update(time_step)
        print(f"\ttarget id: {target.id}; position: {target.position}")
