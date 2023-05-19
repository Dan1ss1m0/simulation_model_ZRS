from misc import *
from Trajectory import trajectory_typename_to_class
from Projectiles import projectile_typename_to_class
from Targets import Target
from logs import logger

# ToDo: выделить траектории в типы движения, а не в классы


class Environment:

    def __init__(self, initialization_type, config=None):

        self.targets = {}
        self.projectiles = {}
        self.projectile_id_to_target_id = {}

        if initialization_type == 'config_file':
            init = self.initialize_with_file_data(config)
            if init:
                logger.info("Environment: initialization performed using the config file")
            else:
                logger.warning("Environment: initializing with empty field")

        self.exploded_not_cleared_projectiles = []
        self.exploded_not_cleared_targets = []

    def update_targets(self, time_step):

        for target in self.targets.values():
            target.update(time_step=time_step)

    def update_projectiles(self, time_step, new_targets: dict):

        """new_targets: словарь, где ключи - id ракет, значения - новые цели для соответствующих ракет"""

        for projectile in self.projectiles.values():
            if projectile.id in new_targets.keys():
                projectile.update(time_step=time_step, new_target=new_targets[projectile.id])
            else:
                logger.warning(f"Environment: for projectile {projectile.id} wasn't provided new target")
                projectile.update(time_step=time_step, new_target=projectile.target)

            if projectile.exploded:

                self.exploded_not_cleared_projectiles.append(projectile.id)

                for target in self.targets.values():  # ракеты не связаны напрямую с целями, поэтому ищем вручную
                    if dist(target.position, projectile.position) < projectile.explosion_range:
                        target.destroyed = True
                        self.exploded_not_cleared_targets.append(target.id)

        # self.clear_exploded()

    def check_exploded(self):
            
        for projectile in self.projectiles.values():

            if projectile.exploded:

                self.exploded_not_cleared_projectiles.append(projectile.id)

                for target in self.targets.values():  # ракеты не связаны напрямую с целями, поэтому ищем вручную
                    if dist(target.position, projectile.position) < projectile.explosion_range:
                        target.destroyed = True
                        self.exploded_not_cleared_targets.append(target.id)

    def get_targets(self):

        return self.targets

    def get_projectiles(self):
        return self.projectiles

    def add_target(self, trajectory_type, **kwargs):

        if self.targets.get(kwargs['id']):
            logger.error(f"Environment: error adding target {kwargs['id']}: target with such id already exists")
            return False

        try:
            trajectory = trajectory_typename_to_class[trajectory_type](**kwargs['trajectory_arguments'])
            print("hello")
            self.targets[kwargs['id']] = Target(kwargs['id'], trajectory)

        except Exception as e:
            logger.error(f"Environment: adding target failed with exception: {e}")
            return False
        
        logger.info(f"Environment: target {kwargs['id']} have been successfully set")
        return True

    def add_projectile(self, projectile_type, **kwargs):

        if self.projectiles.get(kwargs['id']):
            logger.error(f"Environment: error adding projectile {kwargs['id']}: projectile with such id already exists")
            return False

        try:
            self.projectiles[kwargs['id']] = projectile_typename_to_class[projectile_type](**kwargs)

        except Exception as e:
            logger.error(f"Environment: adding projectile failed with exception: {e}")
            return False

        logger.info(f"Environment: projectile {kwargs['id']} have been successfully set")
        return True

    def clear_exploded(self):

        for projectile_id in self.exploded_not_cleared_projectiles:
            del self.projectiles[projectile_id]
        self.exploded_not_cleared_projectiles.clear()

        for target_id in self.exploded_not_cleared_targets:
            del self.targets[target_id]
        self.exploded_not_cleared_targets.clear()

    def initialize_with_file_data(self, config):

        if config is None:
            logger.error(f"Environment: initialization error: config is not provided")
            return False
            
        for item in config["targets"].items():
            ids, params_dict = item
            self.add_target(trajectory_type=params_dict["trajectory_type"],
                            **dict(id=ids, trajectory_arguments=params_dict["trajectory_arguments"]))
        
        return True
