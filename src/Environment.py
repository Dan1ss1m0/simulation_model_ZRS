from misc import *
from Trajectory import trajectory_typename_to_class
from Projectiles import projectile_typename_to_class
from Targets import Target

# ToDo: выделить траектории в типы движения, а не в классы


class Environment:

    def __init__(self, initialization_type, **kwargs):

        self.targets = {}
        self.projectiles = {}

        if initialization_type == 'config_file':
            self.initialize_with_file_data(**kwargs)
        else:
            print("initializing with empty field")

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
                    if dist(target.position, projectile.position) < projectile.explosion_range:
                        target.destroyed = True
                        self.exploded_not_cleared_targets.append(target.id)

        # self.clear_exploded()

    def get_targets(self):

        return self.targets

    def get_projectiles(self):
        return self.projectiles

    def add_target(self, trajectory_type, **kwargs):

        if self.targets.get(kwargs['id']):
            print(f"error adding target {kwargs['id']}: target with such id already exists")
            return False

        try:
            # print(kwargs['trajectory_arguments'])
            trajectory = trajectory_typename_to_class[trajectory_type](**kwargs['trajectory_arguments'])
            self.targets[kwargs['id']] = Target(kwargs['id'], trajectory)

        except Exception as e:
            print(f"adding target failed with exception: {e}")
            return False

        return True

    def add_projectile(self, projectile_type, **kwargs):

        if self.projectiles.get(kwargs['id']):
            print(f"error adding projectile {kwargs['id']}: projectile with such id already exists")
            return False

        try:
            self.projectiles[kwargs['id']] = projectile_typename_to_class[projectile_type](**kwargs)

        except Exception as e:
            print(f"adding projectile failed with exception: {e}")
            return False

        return True

    def clear_exploded(self):

        for projectile_id in self.exploded_not_cleared_projectiles:
            del self.projectiles[projectile_id]
        self.exploded_not_cleared_projectiles.clear()

        for target_id in self.exploded_not_cleared_targets:
            del self.targets[target_id]
        self.exploded_not_cleared_targets.clear()

    def initialize_with_file_data(self, config_path):
        pass

    # other types of initialization here
