from misc import *
from Targets import target_typename_to_class
from Projectiles import projectile_typename_to_class
import logging


class Environment:

    def __init__(self, initialization_type, config=None):

        self.targets = {}
        self.projectiles = {}
        self.projectile_id_to_target_id = {}

        if initialization_type == 'config_file':
            init = self.initialize_with_file_data(config)
            if init:
                logging.info("initialization performed using the config file")
        else:
            logging.warning("initializing with empty field")

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
                print(f"for projectile {projectile.id} wasn't provided new target")
                projectile.update(time_step=time_step, new_target=projectile.target)

            if projectile.exploded:

                self.exploded_not_cleared_projectiles.append(projectile.id)

                for target in self.targets.values():  # ракеты не связаны напрямую с целями, поэтому ищем вручную
                    if dist(target.position, projectile.position) < projectile.explosion_distance:
                        target.destroyed = True
                        self.exploded_not_cleared_targets.append(target.id)


    def get_targets(self):
        return self.targets

    def get_projectile(self):
        return self.projectiles

    def add_target(self, target_type, **kwargs):

        if self.targets.get(kwargs['id']):
            logging.error(f"error adding target {kwargs['id']}: target with such id already exists")
            return False
        try:
            self.targets[kwargs['id']] = target_typename_to_class[target_type](**kwargs)

        except Exception as e:
            logging.error(f"adding target failed with exception: {e}")
            return False

        logging.info(f"target {kwargs['id']} have been successfully set")
        return True

    def add_projectile(self, projectile_type, **kwargs):

        if self.projectiles.get(kwargs['id']):
            logging.error(f"error adding projectile {kwargs['id']}: projectile with such id already exists")
            return False

        try:
            self.projectiles[kwargs['id']] = projectile_typename_to_class[projectile_type](**kwargs)

        except Exception as e:
            logging.error(f"adding projectile failed with exception: {e}")
            return False

        logging.info(f"projectile {kwargs['id']} have been successfully set")
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
            logging.error(f"initialization error: config is not provided")
            return False
            
        for item in config["targets"].items():
            ids, params_dict = item
            self.add_target(target_type=params_dict["class"],
                            id=ids,
                            **params_dict["parameters"])
            
        if len(self.targets) != 0:
            for projectile_id, target in enumerate(self.targets.values()):
                self.add_projectile(projectile_type=config["projectiles"]["class"],
                                    id=projectile_id,
                                    target=target.position + np.random.normal(scale=0.03, size=3),
                                    **config["projectiles"]["parameters"])
                self.projectile_id_to_target_id[projectile_id] = target.id
        else:
            logging.error(f"initialization error: projectiles are not created, targets list is empty")
            return False
        
        return True
    
    # other types of initialization here

