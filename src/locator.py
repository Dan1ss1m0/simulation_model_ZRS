import random as rdm
import math as mth
from misc import *
from Targets import Target
from Launcher import *

def sign(x):
    if x>0:
        return 1
    if x==0:
        return 0
    if x<0:
        return -1


class Ray(object):
    def __init__(self, omega_az, omega_el, r_max):
        self.omega_az = omega_az
        self.omega_el = omega_el
        self.phi = rdm.random() * 2 * mth.pi
        self.teta = rdm.random() * mth.pi / 2
        self.Rmax = r_max

    def upd_coord(self):
        self.phi = (self.phi + self.omega_az)
        self.teta = (self.teta + self.omega_el)
        if self.phi > 2*mth.pi:
            self.phi = self.phi % 2*mth.pi
        if self.phi >  (mth.pi / 2):
            self.teta =  self.teta % (mth.pi / 2)


class TrackingRay(object):
    def __init__(self, phi, teta, t_id, m_id, pbu_target_id):
        self.phi = phi
        self.teta = teta
        self.err_phi = 0
        self.err_teta = 0
        self.target_id = t_id
        self.missle_id = m_id
        self.pbu_target_id = pbu_target_id

    def upd_coord(self, d_phi, d_teta):
        self.phi = self.phi + 0.7*d_phi + (d_phi - self.err_phi) * 0.3
        self.err_phi = d_phi
        self.teta = self.teta + 0.7*d_teta + (d_teta - self.err_teta) * 0.3
        self.err_teta = d_teta


class Locator(object):
    # rays = []
    state = 0
    curr_ray_x = []
    curr_ray_y = []
    curr_ray_z = []

    def __init__(self, initialization_type, config=None):

        if initialization_type == 'config_file':
            init = self.initialize_with_file_data(config)
            if init:
                logging.info("initialization performed using the config file")
            else:
                logging.warning("initializing with empty field")

        self.rays = []
        self.rays.append(Ray(self.omega_az, self.omega_el, self.r_max))
        self.state = 0


    def initialize_with_file_data(self, config):

        if config is None:
            logging.error(f"initialization error: config is not provided")
            return False

        self.x, self.y, self.z = config["coordinates"].values()
        self.time_step = config["time_step"]
        self.omega_az = config["omega_az"] * config["time_step"]
        self.omega_el = config["omega_el"] * config["time_step"]
        self.r_max = config["r_max"]
        self.dr = config["dr"]
        self.ray_width = 5 / 100 * mth.pi

        return True

    def del_ray(self, index, PBU):
        PBU.clear_exploded(self.rays[index].pbu_target_id)
        self.rays.pop(index)
        self.state = self.state - 1  # is it necessary?

    def add_ray(self, phi, teta, m_id, id, pbu_target_id):
        self.rays.append(TrackingRay(phi, teta, id, m_id, pbu_target_id))

    def to_xyz(self, r):
        x = self.x + r * mth.cos(self.rays[self.state].phi) * mth.cos(self.rays[self.state].teta)
        y = self.y + r * mth.sin(self.rays[self.state].phi) * mth.cos(self.rays[self.state].teta)
        z = self.z + r * mth.sin(self.rays[self.state].teta)
        return x, y, z

    def distance(self, target, x, y, z):
        [tx, ty, tz] = target.position
        dist = mth.sqrt((tx - x) ** 2 + (ty - y) ** 2 + (tz - z) ** 2)
        return dist

    def do_step(self, env, PBU):
        targets = env.get_targets()
        missles = env.get_projectiles()
        self.curr_ray_x = []
        self.curr_ray_y = []
        self.curr_ray_z = []

        if (self.state == 0):
            flag = False
            for r in range(0, self.r_max, self.dr):
                for target_id, target in targets.items():
                    [x,y,z]  = self.to_xyz(r)
                    self.curr_ray_x.append(x)
                    self.curr_ray_y.append(y)
                    self.curr_ray_z.append(z)
                    pos = np.array([x,y,z])
                    if (self.distance(target, x, y, z) < mth.sqrt((r * mth.sin(self.ray_width))**2 +(2*self.dr)**2)):
                        pbu_target_id, mis_id = PBU.add_target(pos, env)
                        if pbu_target_id !=-1:
                            self.add_ray(self.rays[self.state].phi, self.rays[self.state].teta, mis_id,target_id, pbu_target_id)
                        flag = True
                        break
                if flag == True:
                    break
            self.rays[0].upd_coord()
        else:
            self.curr_ray_x = []
            self.curr_ray_y = []
            self.curr_ray_z = []
            target = targets.get(self.rays[
                self.state].target_id, None)
            missle = missles.get(self.rays[
                                     self.state].missle_id, None)

            if (target!=None and missle !=None and self.distance(target, self.x, self.y, self.z) < self.r_max):
                [x, y, z] = target.position
                Tx, Ty, Tz = self.to_xyz(100)
                Tx = Tx - self.x
                Ty = Ty - self.y
                Tz = Tz - self.z
                Vx = x - self.x
                Vy = y - self.y
                Vz = z - self.z
                d_phi = sign(Tx*Vy - Ty*Vx)*mth.acos(
                    (Tx * Vx + Ty * Vy) / (mth.sqrt(Tx ** 2 + Ty ** 2) * mth.sqrt(Vx ** 2 + Vy ** 2)))
                d_teta = mth.asin((z - self.z) / mth.sqrt(Vx ** 2 + Vy ** 2 + Vz ** 2)) - self.rays[
                    self.state].teta
                self.rays[self.state].upd_coord(d_phi, d_teta)
                for r in range(0, self.r_max, self.dr):
                    x, y, z = self.to_xyz(r)
                    if (self.distance(target, x, y, z) <  mth.sqrt(
                            (r * mth.sin(self.ray_width)*0.0) ** 2 + (2 * self.dr) ** 2)):
                        pos = np.array([x, y, z])
                        PBU.update_targets(self.rays[self.state].pbu_target_id, pos)
                        break

                missle.update(time_step=self.time_step, new_target=np.array([x, y, z]))

                for r in range(0, self.r_max, self.dr):
                    x, y, z = self.to_xyz(r)
                    self.curr_ray_x.append(x)
                    self.curr_ray_y.append(y)
                    self.curr_ray_z.append(z)
            else:
                self.del_ray(self.state, PBU)

        if self.state!=0:
            print(PBU.targets[self.rays[self.state].pbu_target_id].position)

        self.state = (self.state + 1) % len(self.rays)