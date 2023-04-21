#ifndef LOCATOR_H
#define LOCATOR_H

class ray{
private:
   float phi;   //azimut
   float teta;  //elevation
public:
   ray(float p, float t){
       this->phi = p;
       this->teta = t;
   }
   virtual void update_angles(); //should be update_angles(targets_pool, &pbu);
   float get_teta();
   float get_phi();
};
class tracking_ray:public ray{
public:
    tracking_ray(int p, int t):ray(p,t){}
    void update_angles();
};

class locator
{
public:
    locator();
    void add_ray();
    void del_ray(int i);
private:
    ray* rays[10];
};

#endif // LOCATOR_H
