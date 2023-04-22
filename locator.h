#ifndef LOCATOR_H
#define LOCATOR_H

class ray{
private:
   float width = 1.5; //width of the ray in degrees in both sections
   float Rmax = 10000;
   float phi;   //azimut
   float teta;  //elevation
public:
   position to_coordinates(float R); // (R, Teta, Phi) to (x, y, z)
   ray(float p, float t){
       this->phi = p;
       this->teta = t;
   }
   position pos;
   virtual void update_angles(vector <positon> targets, ControlCenter& PBU); //should be update_angles(targets_pool, &pbu);
   float get_teta();
   float get_phi();
};

class tracking_ray:public ray{
public:
    float get_delta_phi();  //it CALCULATES delta_phi
    float get_delta_teta();
    tracking_ray(int p, int t, int target_id):ray(p,t){ this->target_id = target_id;}
    void update_angles(vector <positons> targets, ControlCenter& PBU);
private:
    float p = 1;     //propoertional coefficent
    float d = 0.01;  //differentional coefficient
    float delta_phi = 0;
    float delta_teta = 0;
    int target_id;
};

class locator
{
public:
    position pos;
    locator(float x, float y, float z);
    void add_ray();
    void del_ray(int n); //delete
private:
    int locator_id;
    ray* rays[10];
};

#endif // LOCATOR_H
