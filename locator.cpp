#include <stdlib.h>
#include "locator.h"
#include <ctime>
using namespace std;

int sign(float x) { if (x<0) return -1; else if (x==0) return 0; else return 1; }
float scale(position pos){
    return sqrt(pow(pos.x,2) + pow(pos.y,2) + pow(pos.z,2));
}
float dist(position pos1, position pos2){
    return sqrt(pow((pos1.x - pos2.x),2) + pow((pos1.y - pos2.y),2) + pow((pos1.z - pos2.z),2));
}
position ray::to_coordinates(float R){
    position tmp;
    tmp.x = pos.x + R*cos(M_PI/180*phi)*cos(M_PI/180*teta);
    tmp.y = pos.y + R*cos(M_PI/180*teta)*sin(M_PI/180*phi);
    tmp.z = pos.z + R*sin(M_PI/180*teta);
}

void ray::update_angles(vector <positons> targets, ControlCenter& PBU){
    phi = phi + 5;
    if (phi > 360){
        teta += 5;
        phi = int(phi) % 360;
    }

    if (teta > 90){
        teta = int(teta) % 90;
    }
    for (int r = 0; r < Rmax; r += 10){
        position tmp = to_coordinates(r);
        for (int i = 0; i < targets.size(); i++){
            if (dist(tmp, targets[i]) > r*sin(M_PI/180*width)){

                PBU.add_target(tmp , i);
            }
        }
    }

}


void tracking_ray::update_angles(vector<positons> targets, ControlCenter &PBU){

   float d_phi = -(delta_phi - get_delta_phi(targets[target_id]))*d;
   phi = phi + p*delta_phi + d_phi;
   float d_teta =  -(delta_teta - get_delta_teta(targets[target_id]))*d;
   teta = teta +p*delta_teta + d_teta;
}


locator::locator(float x, float y, float z)
{
       pos.x = x; pos.y = y; pos.z = z; // инициализируем положение объекта
       std::srand(time(nullptr)); // инициализируем генератор случайных чисел
       int max_teta = 9;
       int max_phi = 36;
       int p = (std::rand() % (max_phi + 1))*10;
       int t = (std::rand() % (max_teta + 1))*10;
       rays[0] = new ray(p,t);

}
float tracking_ray::get_delta_phi(position target_position){
    position direction = to_coordinates(100) - pos;
    position target = target_position - pos;
    int s = sign(direction.x*target.y - direction.y*target.x); //turning direction
    delta_phi = acos((direction.x * target.x + direction.y * target.y + direction.z * target.z)/(scale(direction)*scale(target)))*s/M_PI*180;
    return delta_phi;
}
float tracking_ray::get_teta(position target_position){
    position target = target_position - pos;
    delta_phi = acos(target.z/scale(target))*180/M_PI - teta;
    return delta_phi;
}
