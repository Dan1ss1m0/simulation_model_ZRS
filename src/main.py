from Targets import *
from Projectiles import *
from Trajectory import *
from Environment import Environment
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import locator as loc

T = 0.1
time_step = T
missile_base_position = (0, 0, 0)

environment = Environment(None)

environment.add_target('uniform',
                       **dict(id=1, trajectory_arguments=dict(position=(1000, 0, 2000), velocity=(100, 0, 200))))
environment.add_target('accelerating', **dict(
    trajectory_arguments=dict(position=(1000, 0, 1000), velocity=(0, 0, 0), acceleration=(10, 0, 20)), id=2))
environment.add_target('circled', **dict(
    trajectory_arguments=dict(position=(4000, 0, 2000), velocity=(0, 0, 350), center=(2000, 0, 2000)), id=3))
environment.add_target('complex', **dict(
    trajectory_arguments=dict(
        position=(8000, 0, 4000),
        trajectories=[[2, 'uniform', {'position': None, 'velocity': (100, 10, 100)}],
                      [2, 'uniform', {'position': None, 'velocity': (-200, 0, 100)}],
                      [4, 'circled', {'position': None, 'center': (7000, 0, 6000), 'velocity': (100, 0, 100)}],
                      [3, 'accelerating', {'position': None, 'velocity': None, 'acceleration': (-5, 0, -5)}]]
    ),
    id=4
))

projectile_id_to_target_id = {}

for projectile_id, target in enumerate(environment.targets.values()):
    environment.add_projectile('preemptive missile', **dict(
        position=missile_base_position,
        target=target.position + np.random.normal(scale=0.00003, size=3),
        id=projectile_id,
        trigger_distance=5,
        explosion_range=10,
        max_velocity=600,
        preemption=0.5
    ))

    projectile_id_to_target_id[projectile_id] = target.id


# for i in range(200):
#
#     print(f"time passed: {time_step * (i + 1)}")
#
#     environment.update_targets(time_step)
#
#     for target in environment.targets.values():
#         print(f"\ttarget id: {target.id}; position: {np.round(target.position, 2)}; velocity: {np.round(target.velocity, 2)}")

# environment.update_projectiles(time_step, {projectile_id:
#     environment.targets[projectile_id_to_target_id[projectile_id]].position + np.random.normal(scale=0.000003, size=3)
#     for projectile_id in environment.projectiles.keys()})

# for projectile in environment.projectiles.values():
#     if projectile.exploded:
#         print(f"\tmissile {projectile.id} exploded in point {projectile.position} chasing target "
#               f"{projectile_id_to_target_id[projectile.id]} at position "
#               f"{environment.targets[projectile_id_to_target_id[projectile.id]].position}")
#
#     else:
#         print(f"\tmissile id: {projectile.id}; position: {projectile.position}")
#
# environment.clear_exploded()

# if not environment.projectiles or not environment.targets:
#
#     break

class CC(object):
    def __init__(self):
        """Constructor"""
        self.name = "PB"

    def check(self):
        A.add_ray(0, A.rays[0].phi, A.rays[0].teta, 0)
        A.state = A.state + 1


class plane(object):
    """docstring"""

    def __init__(self, Vx, Vy, x0, y0):
        """Constructor"""
        self.Vx = Vx
        self.Vy = Vy
        self.x0 = x0
        self.y0 = y0
        self.x = self.x0
        self.y = self.y0
        self.z = 100

    def upd(self):
        self.x0 = self.x0 + self.Vx * T
        self.y0 = self.y0 + self.Vy * T
        self.x = self.x0
        self.y = self.y0

    def update(self, x, y, z):
        print('\n')

    def get_xyz(self):
        return self.x, self.y, self.z


'''
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)

points = [(0.1, 0.5), (0.5, 0.6), (0.9, 0.7)]
points1 = [(0.1, 0.5), (0.5, 0.5), (0.9, 0.5)]
locators =  [(2, 0.2), (0.3, 0.3)]
def animate(i):
    plt.waitforbuttonpress()
    ax.clear()
    # Get the point from the points list at index i
    point = points[i]
    point1 = points1[i]
    l1 = locators[0]
    l2 = locators[1]
    # Plot that point using the x and y coordinates
    ax.plot(point[0], point[1], color='green',
            label='original', marker='o')
    ax.plot(l1[0], l1[1], color='blue',
            label='original', marker='s')
    ax.plot(l2[0], l2[1], color='blue',
            label='original', marker='s')
    ax.plot(point1[0], point1[1], color='red',
            label='original', marker='4')
    # Set the x and y axis to display a fixed range
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])


ani = animation.FuncAnimation(fig, animate, frames=len(points),
                    interval=500, repeat=False)
plt.show()
plt.close()
'''
targ = []
missle = []
PBU = CC()
mis1 = plane(222, -500, 50, 50)
pl1 = plane(400, 0, 500, 500)
targ.append(pl1)
missle.append(mis1)
fig, (ax, ax1) = plt.subplots(1, 2)

fig.set_size_inches(10, 10)

A = loc.locator(1000, 1000, 0)


def animate(i):
    ax.clear()
    ax1.clear()
    ax1.grid(True)
    ax.grid(True)
    print(f"time passed: {time_step * (i + 1)}")

    environment.update_targets(time_step)

    for target in environment.targets.values():
        print(
            f"\ttarget id: {target.id}; position: {np.round(target.position, 2)}; velocity: {np.round(target.velocity, 2)}")
        [x, y, z] = target.position
        ax.scatter(x, y, color='green',
                   label='original', marker='o')
        ax1.scatter(x, z, color='green',
                    label='original', marker='o')

    environment.update_projectiles(time_step, {projectile_id:
                                                   environment.targets[projectile_id_to_target_id[
                                                       projectile_id]].position + np.random.normal(scale=0.000003,
                                                                                                   size=3)
                                               for projectile_id in environment.projectiles.keys()})

    for projectile in environment.projectiles.values():
        if projectile.exploded:
            print(f"\tmissile {projectile.id} exploded in point {projectile.position} chasing target "
                  f"{projectile_id_to_target_id[projectile.id]} at position "
                  f"{environment.targets[projectile_id_to_target_id[projectile.id]].position}")

        else:
            [x, y, z] = projectile.position
            print(f"\tmissile id: {projectile.id}; position: {projectile.position}")
            ax.scatter(x, y, color='red',
                       label='original', marker='x')
            ax1.scatter(x, z, color='red',
                        label='original', marker='x')

    environment.clear_exploded()

    # plt.waitforbuttonpress()

    # A.do_step(targ, PBU, missle)    # Plot that point using the x and y coordinates
    # ax.plot(pl1.x0, pl1.y0, color='green',
    # label='original', marker='o')
    # ax1.plot(pl1.x0, pl1.z, color='green',
    # label='original', marker='o')
    # ax.plot(mis1.x0, mis1.z, color='red',
    # label='original', marker='4')
    # ax.plot(A.x, A.y, color='blue',
    #  label='original', marker='s')
    # ax1.plot(A.x, A.z, color='blue',
    #  label='original', marker='s')
    # xr = A.curr_ray_x
    # yr = A.curr_ray_y
    # ax.plot(A.curr_ray_x, A.curr_ray_y)
    # ax1.plot(A.curr_ray_x, A.curr_ray_z)
    pl1.upd()
    mis1.upd()
    ax.set_xlim([0, 10000])
    ax.set_ylim([0, 10000])
    ax1.set_xlim([0, 10000])
    ax1.set_ylim([0, 10000])


ani = animation.FuncAnimation(fig, animate, 200,
                              interval=1, repeat=False)

plt.show()
plt.close()
