import matplotlib.pyplot as plt
import matplotlib.animation as animation
import locator as loc
T = 0.1
class CC(object):
    def __init__(self):
        """Constructor"""
        self.name = "PB"
    def check(self):
        A.add_ray(0,A.rays[0].phi, A.rays[0].teta,0)
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
        self.z = 0

    def upd(self):
        self.x0 = self.x0 + self.Vx * T
        self.y0 = self.y0 + self.Vy * T
        self.x = self.x0
        self.y = self.y0
    def update(self,x,y,z):
        print('ok')
    def get_xyz(self):
        return self.x,self.y,self.z

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
mis1 = plane(1,-1,1,10)
pl1 = plane(0.1,0,1,1)
targ.append(pl1)
missle.append(mis1)
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(10, 10)

A = loc.locator(1, 2, 0)
def animate(i):
    #plt.waitforbuttonpress()
    ax.clear()
    ax.grid(True)
    A.do_step(targ, PBU, missle)    # Plot that point using the x and y coordinates
    ax.plot(pl1.x0, pl1.y0, color='green',
            label='original', marker='o')
    ax.plot(mis1.x0, mis1.y0, color='red',
            label='original', marker='4')
    ax.plot(A.x, A.y, color='blue',
            label='original', marker='s')
    xr = A.curr_ray_x
    yr = A.curr_ray_y
    ax.plot(A.curr_ray_x, A.curr_ray_y)
    pl1.upd()
    mis1.upd()
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
ani = animation.FuncAnimation(fig, animate, 200,
                    interval=50, repeat=False)
plt.show()
plt.close()











