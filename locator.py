import random as rdm
import math as mth
from misc import *
from Targets import Target
from Launcher import *
# PARAMETRS#
T = 0.005 #time step 0.1 second
omega_az, omega_el, Rmax = 10, 5, 1000  # omega_az, omega_el - angular speed of the ray, Rmax - maximum distance of scanning
dr = 1
ray_width = 4 / 180 * mth.pi  # width of the ray
Eps = 10  # minimal distance between plane and missle
omega_el = omega_el * T
omega_az = omega_az * T
def find(id, list):
    tmp = -1
    for i in range(len(list)):
        if list[i].id == id:
            tmp = i
    return tmp
def sign(x):
    if x>0:
        return 1
    if x==0:
        return 0
    if x<0:
        return -1
# CLASSES#

class ray(object):
    def __init__(self):
        self.omega_az = omega_az
        self.omega_el = omega_el
        self.phi = rdm.random() * 2 * mth.pi
        self.teta = rdm.random() * mth.pi / 2
        self.Rmax = Rmax

    def upd_coord(self):
        self.phi = (self.phi + self.omega_az)
        self.teta = (self.teta + self.omega_el)
        if self.phi > 2*mth.pi:
            self.phi = self.phi % 2*mth.pi
        if self.phi >  (mth.pi / 2):
            self.teta =  self.teta % (mth.pi / 2)




class tracking_ray(object):
    def __init__(self, phi, teta, t_id, m_id, pbu_target_id):
        self.phi = phi
        self.teta = teta
        self.err_phi = 0
        self.err_teta = 0
        self.target_id = t_id
        self.missle_id = m_id
        self.pbu_target_id = pbu_target_id

    def upd_coord(self, d_phi, d_teta):
        self.phi = self.phi + 0.5*d_phi + (d_phi - self.err_phi) * 0
        self.err_phi = d_phi
        self.teta = self.teta + 0.5*d_teta + (d_teta - self.err_teta) * 0
        self.err_teta = d_teta


class locator(object):
    rays = []
    state = 0  # state of locator, represents the current ray
    curr_ray_x = []
    curr_ray_y = []
    curr_ray_z = []

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.rays.append(ray())
        self.state = 0

    def del_ray(self, index, PBU):
        PBU.del_target(self.rays[index].pbu_target_id)
        self.rays.pop(index)
        self.state = self.state - 1  # is it necessary?

    def add_ray(self, phi, teta, m_id, id, pbu_target_id):
        self.rays.append(tracking_ray(phi, teta, id, m_id, pbu_target_id))

    def to_xyz(self, r):
        x = self.x + r * mth.cos(self.rays[self.state].phi) * mth.cos(self.rays[self.state].teta)
        y = self.y + r * mth.sin(self.rays[self.state].phi) * mth.cos(self.rays[self.state].teta)
        z = self.z + r * mth.sin(self.rays[self.state].teta)
        return x, y, z

    def distance(self, target, x, y, z):
        dist = mth.sqrt((target.x - x) ** 2 + (target.y - y) ** 2 + (target.z - z) ** 2)
        return dist

    def do_step(self, targets, PBU, missles):
        self.curr_ray_x = []
        self.curr_ray_y = []
        self.curr_ray_z = []
        if (self.state == 0):
            flag = False
            for r in range(0, Rmax, dr):
                for i in range(len(targets)):
                    x,y,z  = self.to_xyz(r) 
                    self.curr_ray_x.append(x)
                    self.curr_ray_y.append(y)
                    self.curr_ray_z.append(z)
                    pos = np.array([x,y,z])
                    if (self.distance(targets[i], x, y, z) < 1.1*mth.sqrt((r * mth.sin(ray_width))**2 +(2*dr)**2)):
                        pbu_target_id, mis_id = PBU.add_target(pos)
                        if pbu_target_id !=-1:
                            self.add_ray(self.rays[self.state].phi, self.rays[self.state].teta, mis_id,targets[i].id, pbu_target_id)
                        flag = True
                        break
                if flag == True:
                    break
            self.rays[0].upd_coord()
        else:
            self.curr_ray_x = []
            self.curr_ray_y = []
            self.curr_ray_z = []

            m_id = find(self.rays[
                self.state].missle_id, missles)
            id = find(self.rays[
                self.state].target_id, targets)
            if (m_id!=-1 and id !=-1):
                [x, y, z] = missles[m_id].position()
                Tx, Ty, Tz = self.to_xyz(100)
                Tx = Tx - self.x
                Ty = Ty - self.y
                Tz = Tz - self.z
                Vx = targets[id].x - self.x
                Vy = targets[id].y - self.y
                Vz = targets[id].z - self.z
                d_phi = mth.acos(
                    (Tx * Vx + Ty * Vy) / (mth.sqrt(Tx ** 2 + Ty ** 2) * mth.sqrt(Vx ** 2 + Vy ** 2)))
                d_teta = mth.asin((targets[id].z - self.z) / mth.sqrt(Vx ** 2 + Vy ** 2 + Vz ** 2)) - self.rays[
                    self.state].teta
                self.rays[self.state].upd_coord(d_phi, d_teta)
                for r in range(0, Rmax, dr):
                    x, y, z = self.to_xyz(r)
                    if (self.distance(targets[id], x, y, z) < 1.1 * mth.sqrt(
                            (r * mth.sin(ray_width)) ** 2 + (2 * dr) ** 2)):
                        break
                missles[m_id].update(T, np.array([x, y, z]))
                for r in range(0, Rmax, dr):
                    x, y, z = self.to_xyz(r)
                    self.curr_ray_x.append(x)
                    self.curr_ray_y.append(y)
                    self.curr_ray_z.append(z)
            else:
                self.del_ray(self.state, PBU)

        self.state = (self.state + 1) % len(self.rays)