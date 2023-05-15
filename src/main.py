from Targets import *
from Projectiles import *
from Trajectory import *
from Environment import Environment
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yaml

from locator import Locator
from Launcher import Launcher
from pbu2 import Pbu

with open("./src/config.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)

pbu = Pbu('config_file', config["Pbu"])
environment = Environment('config_file', config["Environment"])
A = Locator('config_file', config["Locator"])

time_step = config["Environment"]["time_step"]

fig, (ax, ax1) = plt.subplots(1, 2)
fig.set_size_inches(10, 10)


def animate(i):

    ax.clear()
    ax1.clear()
    ax1.grid(True)
    ax.grid(True)

    A.do_step(environment, pbu)
    xr = A.curr_ray_x
    yr = A.curr_ray_y
    ax.plot(A.x, A.y, color='blue',
            label='original', marker='s')
    ax1.plot(A.x, A.z, color='blue',
             label='original', marker='s')
    ax.plot(A.curr_ray_x, A.curr_ray_y)
    ax1.plot(A.curr_ray_x, A.curr_ray_z)

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

        [x,y,z] = target.position
        ax.scatter(x, y, color='green',
                 label='original', marker='o')
        ax1.scatter(x, z, color='green',
                label='original', marker='o')

    for projectile in environment.projectiles.values():
        if projectile.exploded:
            print(f"\tmissile {projectile.id} exploded in point {projectile.position}")

        else:
            [x, y, z] = projectile.position
            print(f"\tmissile id: {projectile.id}; position: {projectile.position}")
            ax.scatter(x, y, color='red',
                       label='original', marker='x')
            ax1.scatter(x, z, color='red',
                        label='original', marker='x')
    environment.check_exploded()
    environment.clear_exploded()

    ax.set_xlim([0, 10000])
    ax.set_ylim([0, 10000])
    ax1.set_xlim([0, 10000])
    ax1.set_ylim([0, 10000])


ani = animation.FuncAnimation(fig, animate, 1000,
                              interval=1, repeat=False)

plt.show()
plt.close()
