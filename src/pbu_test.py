from Environment import Environment
from pbu2 import Pbu
import yaml

environment = Environment(None)

# нужно для тестирования добавления тагретов, не для инициализации класса ПБУ.
pos = (50,50,50)

with open("./config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)

pbu = Pbu('config_file', config["Pbu"])

print(pbu.add_target(pos,environment))
print(pbu.clear_exploded(0))