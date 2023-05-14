from Targets import *
from Projectiles import *
from Trajectory import *

time_step = 0.1

trajectories = {'uniform_1': TrajectoryUniform((0, 1, 0), (1, 1, 1)),
                'uniform_2': TrajectoryUniform((-1, 1, 1), (1, 0, -1)),
                'accelerating_1': TrajectoryAccelerating((10, 0, 10), (0, 0, 0), (-2, 0, -2)),
                'accelerating_2': TrajectoryAccelerating((2, 2, 2), (2, 0, 0), (0, 0, 2)),
                'circled_1': TrajectoryCircled((-3, 0, 0), (0, 0, 1), (0, 0, 0)),
                'complex_1': TrajectoryComplex((0, 1, 0),
                                               [[2, 'uniform', {'position': None, 'velocity': (-1, -1, -1)}],
                                                [2, 'uniform', {'position': None, 'velocity': (2, 0, 1)}],
                                                [4, 'circled', {'position': None, 'center': (0, 0, 0), 'velocity': (-1, 0, 1)}],
                                                [3, 'accelerating', {'position': None, 'velocity': None, 'acceleration': (1, 0, 1)}]]
                                               )}

targets = {
    1: Target(id=1, trajectory=trajectories['uniform_1']),
    2: Target(id=2, trajectory=trajectories['uniform_2']),
    3: Target(id=3, trajectory=trajectories['accelerating_1']),
    4: Target(id=4, trajectory=trajectories['accelerating_2']),
    5: Target(id=5, trajectory=trajectories['circled_1']),
    6: Target(id=6, trajectory=trajectories['complex_1'])
}

missiles_id_to_targets_id = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
}

missile_base_position = (0, 0, 0)

missiles = {
    1: PreemptiveMissile(position=missile_base_position,
                         target=targets[missiles_id_to_targets_id[1]].position,
                         id=1,
                         explosion_distance=0.1,
                         max_velocity=6,
                         preemption=5.),
    2: PreemptiveMissile(position=missile_base_position,
                         target=targets[missiles_id_to_targets_id[2]].position,
                         id=2,
                         explosion_distance=0.1,
                         max_velocity=6,
                         preemption=5.),
    3: PreemptiveMissile(position=missile_base_position,
                         target=targets[missiles_id_to_targets_id[3]].position,
                         id=3,
                         explosion_distance=0.1,
                         max_velocity=6,
                         preemption=5.),
    4: PreemptiveMissile(position=missile_base_position,
                         target=targets[missiles_id_to_targets_id[4]].position,
                         id=4,
                         explosion_distance=0.1,
                         max_velocity=6,
                         preemption=5.),
    5: PreemptiveMissile(position=missile_base_position,
                         target=targets[missiles_id_to_targets_id[5]].position,
                         id=5,
                         explosion_distance=0.1,
                         max_velocity=6,
                         preemption=5.),
    6: PreemptiveMissile(position=missile_base_position,
                         target=targets[missiles_id_to_targets_id[6]].position,
                         id=6,
                         explosion_distance=0.1,
                         max_velocity=6,
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
        print(f"\ttarget id: {target.id}; position: {target.position}; velocity: {target.trajectory.velocity}")

    for missile in missiles.values():
        missile.update_target(targets[missile.id].position.copy())
        missile.update(time_step=time_step)
        if missile.exploded:
            print(f"\tmissile {missile.id} exploded in point {missile.position} chasing target {targets[missile.id].id} at position {targets[missile.id].position}")
            exploded_targets += [missiles_id_to_targets_id[missile.id]]
            exploded_missiles += [missile.id]

        else:
            print(f"\tmissile id: {missile.id}; position: {missile.position}; velocity: {missile.velocity}")

    for exploded_target in exploded_targets:
        del targets[exploded_target]

    for exploded_missile in exploded_missiles:
        del missiles[exploded_missile]

    input()
