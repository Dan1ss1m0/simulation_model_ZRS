from Environment import Environment
import numpy as np
import logging
import yaml


logging.basicConfig(level=logging.INFO, filename="environment.log",filemode="w",
                    format="%(asctime)s %(levelname)s: %(message)s")

# сейчас config-file тестировался для модуля Environment, далее в нем будут содержаться поля каждого модуля
# и в каждый модуль будет приходить часть соотвествующая ему.
with open("./config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)

environment = Environment('config_file', config["Environment"])
time_step = config["Environment"]["time_step"]

for i in range(200):

    print(f"time passed: {time_step * (i + 1)}")

    environment.update_targets(time_step)

    for target in environment.targets.values():
        print(f"\ttarget id: {target.id}; position: {target.position}")

    environment.update_projectiles(time_step, {projectile_id:
        environment.targets[environment.projectile_id_to_target_id[projectile_id]].position + np.random.normal(scale=0.03, size=3)
        for projectile_id in environment.projectiles.keys()})

    for projectile in environment.projectiles.values():
        if projectile.exploded:
            print(f"\tmissile {projectile.id} exploded in point {projectile.position} chasing target "
                  f"{environment.projectile_id_to_target_id[projectile.id]} at position "
                  f"{environment.targets[environment.projectile_id_to_target_id[projectile.id]].position}")

        else:
            print(f"\tmissile id: {projectile.id}; position: {projectile.position}")

    environment.clear_exploded()

    if not environment.projectiles or not environment.targets:

        break

