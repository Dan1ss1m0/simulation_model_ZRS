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
# A = Locator('config_file', config["Locator"])
locators_num = list(config["Locator"].keys())
locators = [Locator('config_file', config["Locator"][item]) for item in locators_num]


time_step = config["Environment"]["time_step"]

fig, (ax, ax1) = plt.subplots(1, 2)
fig.set_size_inches(12, 8)


def animate(i):

    ax.clear()
    ax1.clear()
    ax1.grid(True)
    ax.grid(True)

    for j, lctr in enumerate(locators):
        # print(f"iteration number: {i}, {len(lctr.rays)}")
        lctr.do_step(environment, pbu)
        xr = lctr.curr_ray_x
        yr = lctr.curr_ray_y
        zr = lctr.curr_ray_z
        ax.plot(lctr.x, lctr.y, color='blue',
            label='original', marker='s')
        ax1.plot(lctr.x, lctr.z, color='blue',
             label='original', marker='s')
        ax.plot(xr, yr)
        ax1.plot(xr, zr)

    for launcher in pbu.get_launchers().values():
        ax.plot(launcher.launcher_pos[0], launcher.launcher_pos[1], marker='^', color='y')
        ax.plot(launcher.launcher_pos[0], launcher.launcher_pos[2], marker='^', color='y')

    print(f"time passed: {time_step * (i + 1)}")

    plt.rcParams.update({'font.size': 9, 'font.weight': 'light'})

    environment.update_targets(time_step)

    for target in environment.targets.values():
        print(
            f"\ttarget id: {target.id}; position: {np.round(target.position, 2)}; velocity: {np.round(target.velocity, 2)}")

        [x, y, z] = target.position
        ax.scatter(x, y, color='green',
                   label='original', marker='o')
        ax.annotate(f"id: {target.id}", xy=(x, y), xycoords='data', xytext=(-5, 4.), textcoords='offset points', style='italic')
        ax1.scatter(x, z, color='green',
                    label='original', marker='o')
        ax1.annotate(f"id: {target.id}", xy=(x, z), xycoords='data', xytext=(-5, 4.), textcoords='offset points', style='italic')

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
            ax.annotate(f"id: {projectile.id}", xy=(x, y), xycoords='data', xytext=(-5, 4.), textcoords='offset points', style='italic')
            ax1.scatter(x, z, color='red',
                        label='original', marker='x')
            ax1.annotate(f"id: {projectile.id}", xy=(x, z), xycoords='data', xytext=(-5, 4.), textcoords='offset points', style='italic')

    environment.check_exploded()
    environment.clear_exploded()

    ax.set_xlim([0, 10000])
    ax.set_ylim([0, 10000])
    ax1.set_xlim([0, 10000])
    ax1.set_ylim([0, 10000])


ani = animation.FuncAnimation(fig, animate, 1000,
                              interval=1, repeat=False)
# ani.save('./1_0.gif')

plt.show()
plt.close()

