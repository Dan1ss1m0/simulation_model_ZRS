from Environment import Environment
import numpy as np

time_step = 0.01
missile_base_position = (0, 0, 0)

environment = Environment(None)

environment.add_target('uniform', **dict(id=1, trajectory_arguments=dict(position=(5, 0, 5), velocity=(-1, 0, -3))))
environment.add_target('accelerating', **dict(trajectory_arguments=dict(position=(-1, 2, -1), velocity=(0, 0, 0), acceleration=(1, 0, 2)), id=2))
environment.add_target('circled', **dict(trajectory_arguments=dict(position=(-1, 0, 0), velocity=(0, 0, 1), center=(0, 0, 0)), id=3))
environment.add_target('complex', **dict(
    trajectory_arguments=dict(position=(-1, 0, 0), velocity=(0, 0, 1), center=(0, 0, 0)),
                                         id=4)
                       )

projectile_id_to_target_id = {}

for projectile_id, target in enumerate(environment.targets.values()):

    environment.add_projectile('guided missile', **dict(
        position=missile_base_position,
        target=target.position + np.random.normal(scale=0.00003, size=3),
        id=projectile_id,
        trigger_distance=0.1,
        explosion_range=0.3,
        max_velocity=5
    ))

    projectile_id_to_target_id[projectile_id] = target.id

for i in range(200):

    print(f"time passed: {time_step * (i + 1)}")

    environment.update_targets(time_step)

    for target in environment.targets.values():
        print(f"\ttarget id: {target.id}; position: {target.position}")

    environment.update_projectiles(time_step, {projectile_id:
        environment.targets[projectile_id_to_target_id[projectile_id]].position + np.random.normal(scale=0.000003, size=3)
        for projectile_id in environment.projectiles.keys()})

    for projectile in environment.projectiles.values():
        if projectile.exploded:
            print(f"\tmissile {projectile.id} exploded in point {projectile.position} chasing target "
                  f"{projectile_id_to_target_id[projectile.id]} at position "
                  f"{environment.targets[projectile_id_to_target_id[projectile.id]].position}")

        else:
            print(f"\tmissile id: {projectile.id}; position: {projectile.position}")

    environment.clear_exploded()

    if not environment.projectiles or not environment.targets:

        break


class Locator:

    targets = {1: np.array([1, 1, 1]), }


