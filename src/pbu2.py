from misc import *

from Targets import Target
from Launcher import *
from Trajectory import trajectory_typename_to_class
from logs import logger

# пбу создаётся либо через файл, либо текстовую заглушку, 
# принимает на вход: дистанцию между целями, ближе которой цель не будет добавлена и набор параметров

#локатор находит цель
#передаёт инфу пбу о цели
#она глядит по следующим целям у других локаторов
#пбу имеет список всех координат целей, которые находятся в режиме слежения
#если расстояние между целями меньше заданного значения, то цель пропускаем в список активных целей, не переходит в режим слежения
#если цель оказалась новой, она должна запустить ракету из ближайшей к цели установки и передавать значение куда ракете лететь
#локатор заметил цель, передаёт три точки, пбу проверяет есть ли цель с похожими координатами
class Pbu:

    def __init__(self, initialization_type, config=None):

        self.add_distance = None
        self.min_dist = None
        self.launcher_init_id = None
        self.targets = {}
        # набор целей
        self.launchers = {}
        # набор ПУ

        if initialization_type == 'config_file':
            init = self.initialize_with_file_data(config)
            if init:
                logger.info("Pbu: initialization performed using the config file")
            else:
                logger.warning("Pbu: initializing with empty field")

        self.exploded_not_cleared_targets = []
            
    def update_targets(self, target_id, pos):
            self.targets[target_id].position = pos
            # print({target_id: target.position for target_id, target in self.targets.items()})

    def get_targets(self):
        return self.targets
    
    def get_launchers(self):
        return self.launchers

    def add_target(self,  pos, env):
        for target in self.targets.values():
            if (dist(target.position, pos) < self.add_distance) or (dist(target.position+ target.position*self.time_step, pos) < self.add_distance):
                logger.info(f"Pbu: add already existing target")
                return -1, -1
        try:
            if len(self.targets.keys()) > 0:
                new_id = max(self.targets.keys()) + 1
            else:
                new_id = 0

            trajectory = trajectory_typename_to_class['uniform'](**dict(position=pos, velocity=(0,0,0)))
            self.targets[new_id] = Target(id = new_id, trajectory=trajectory)
        except Exception as e:
            logger.error(f"Pbu: adding target failed with exception: {e}")
            return -1, -1
        
        min_dist = [1000000, 'nan']
        for launcher_id in self.launchers.keys():
            pos = pos if isinstance(pos, np.ndarray) else np.array(pos, dtype=np.float64)
            dist1 = [dist(self.launchers[launcher_id].launcher_pos, 
                          pos),launcher_id]
            
            if (dist1[0] < min_dist[0]) and (self.launchers[launcher_id].missile_amount > 0):
                min_dist = dist1

        if min_dist[0] < 1000000:
            proj_id = self.launch(min_dist[1], new_id, pos, env)
            return new_id, proj_id

        else:
            logger.warning(f"Pbu: no one nearest launcher")
            return -1, -1

    def add_launchers(self, **kwargs):

        if self.launchers.get(kwargs['id']):
            logger.warning(f"Pbu: error adding launcher {kwargs['id']}: launcher with such id already exists")
            return False

        try:
            self.launchers[kwargs['id']] = Launcher(**kwargs)

        except Exception as e:
            logger.error(f"Pbu: adding launcher failed with exception: {e}")
            return False

        logger.info(f"Pbu: launcher {kwargs['id']} have been successfully set")
        return True

    def clear_exploded(self, target_num):

        del self.targets[target_num]

    
    def launch(self, launcher_id, missle_id_counter, pos, env):
        return self.launchers[launcher_id].launch(pos, missle_id_counter, env)

    def initialize_with_file_data(self, config):

        if config is None:
            logger.error(f"Pbu: initialization error: config is not provided")
            return False

        self.time_step = config["time_step"]
        self.add_distance = config["add_distance"]
        for item in config["launchers"].items():
            ids, params_dict = item
            self.add_launchers(id=ids, **params_dict)

        return True