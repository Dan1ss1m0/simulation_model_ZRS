import random as rdm
import math as mth
omega_az, omega_el, Rmax = 100, 100, 1000
ray_width = 1.5 / 180 * mth.pi
class ray(object):
    def __init__(self):
        self.omega_az = omega_az
        self.omega_el = omega_el
        self.phi = rdm.random()*2*mth.pi
        self.teta = rdm.random()*mth.pi/2
        self.Rmax = Rmax
    def upd_coord(self):
        self.phi = (self.ph + self.omega_az) % (2*mth.pi)
        self.teta = (self.teta + self.omega_el) % (2*mth.pi)



class tracking_ray(object):
    def __init__(self, phi, teta, id):
        self.phi = phi
        self.teta = teta
        self.err_phi = 0
        self.err_teta
        self.target_id = id
    def upd_coord(self,d_phi, d_teta):
        self.phi = self.phi + d_phi + (d_phi - self.err_phi) *0.1
        self.err_phi = d_phi
        self.teta = self.teta + d_teta + (d_teta - self.err_teta) * 0.1
        self.err_teta = d_teta




 class locator(object):
     rays = []
     state = 0 # state of locator, represents the current ray
     def __init__(self, x,y,z):
         self.x = x
         self.y = y
         self.z = z
         self.rays[0] = ray

     def del_ray(self,index):
         self.rays.pop(index)
         self.state = self.state - 1 #is it necessary?
     def add_ray(self,id,phi,teta):
         self.rays.append(tracking_ray(phi, teta, id))

     def to_xyz(self,r):
         x = self.x + r*mth.cos(self.rays[self.state].phi)*mth.cos(self.rays[self.state].teta)
         y = self.y + r*mth.sin(self.rays[self.state].phi)*mth.cos(self.rays[self.state].teta)
         z = self.z + r *  mth.sin(self.rays[self.state].teta)
         return x,y,z
     def distance(target, x,y,z):
         dist = mth.sqrt((target.x - x)**2 + (target.y - y)**2 + (target.z - z)**2)
         return dist
     def do_step(self, targets, PBU):
         if(self.state == 0):
             for r in range(0,Rmax,5):
                 for i in range(targets.len):
                     if(self.dist(targets[i]), self.to_xyz(r) < r*mth.sin(ray_width)):
                         PBU.check(self.to_xyz(r))
             self.rays[0].upd_coord()
         else:
             id = self.rays[self.state].target_id #its not actually true,  index = foo(id) or its may be not true that index == id
             if(targets[id].is_deleted == True or self.distance(targets[id], self.x, self.y, self.z) > Rmax):
                 self.del_ray(self.state)
             else:
                 Tx,Ty,Tz = self.to_xyz(self,10)
                 Tx = Tx - self.x
                 Ty = Ty - self.y
                 Tz = Tz - self.z
                 Vx = targets[id].x - self.x
                 Vy = targets[id].y - self.y
                 Vz = targets[id].z - self.z
                 d_phi = mth.sign(Tx*Vy - Ty*Vx)*mth.acos((Tx*Vx+Ty*Vy)/(mth.sqrt(Tx**2+Ty**2)*mth.sqrt(Vx**2+Vy**2)))
                 d_teta = mth.acos(targets[id]/mth.sqrt(Vx**2 + Vy**2 + Vz**2)) - self.rays[self.state].teta
                 self.rays[self.state].upd_coord(d_phi, d_teta)

         self.state = (self.state + 1) % self.rays.len()










