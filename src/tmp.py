import numpy as np


class Target:

    def __init__(self, position):

        self.position = np.array(position, dtype=np.float64)

    def __repr__(self):
        return str(self.position)


d = {1: Target((0, 0, 0)),
     2: Target((1, 1, 1)),
     3: Target((2, 2, 2))}

target = d.get(2, None)

if target is None:
    print("target doesn't exist")
else:
    print(target.position)

print(list(d.values()))
print(list(d.keys()))
print(list(d.items()))

for target_id, target in d.items():

    print(target_id, target)
