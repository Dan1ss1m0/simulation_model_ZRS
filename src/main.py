from Targets import *
from Projectiles import *

time_step = 0.01

targets = {
    1: Target(position=(5, 0, 5), velocity=(-1, 0, -3), id=1),
    2: TargetAccelerating(position=(-1, 2, -1), velocity=(0, 0, 0), acceleration=(1, 0, 2), id=2),
    3: TargetCircled(position=(-1, 0, 0), velocity=(0, 0, 1), center=(0, 0, 0), id=3)
}

missiles_id_to_targets_id = {
    1: 1,
    2: 2,
    3: 3
}

missile_base_position = (0, 0, 0)

missiles = {
    1: HomingMissile(position=missile_base_position,
                     target=targets[missiles_id_to_targets_id[1]].position,
                     id=1,
                     explosion_distance=0.1,
                     max_velocity=4,
                     preemption=5.),
    2: HomingMissile(position=missile_base_position,
                     target=targets[missiles_id_to_targets_id[2]].position,
                     id=2,
                     explosion_distance=0.1,
                     max_velocity=4,
                     preemption=5.),
    3: HomingMissile(position=missile_base_position,
                     target=targets[missiles_id_to_targets_id[3]].position,
                     id=3,
                     explosion_distance=0.1,
                     max_velocity=4,
                     preemption=5.),
}

i = 0

while targets:

    print(f"time passed: {time_step * (i + 1)}")
    i += 1

    exploded_targets = []
    exploded_missiles = []

    for target in targets.values():
        target.update(time_step)
        print(f"\ttarget id: {target.id}; position: {target.position}")

    for missile in missiles.values():
        missile.update_target(targets[missile.id].position.copy())
        missile.update(time_step)
        if missile.exploded:
            print(f"\tmissile {missile.id} exploded in point {missile.position} chasing target {targets[missile.id].id} at position {targets[missile.id].position}")
            exploded_targets += [missiles_id_to_targets_id[missile.id]]
            exploded_missiles += [missile.id]

        else:
            print(f"\tmissile id: {missile.id}; position: {missile.position}")

    for exploded_target in exploded_targets:
        del targets[exploded_target]

    for exploded_missile in exploded_missiles:
        del missiles[exploded_missile]


