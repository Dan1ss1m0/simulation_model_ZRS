#include <stdlib.h>
#include "locator.h"
#include <ctime>
using namespace std;
locator::locator()
{
       std::srand(time(nullptr)); // инициализируем генератор случайных чисел
       int max_teta = 9;
       int max_phi = 36;
       int p = (std::rand() % (max_phi + 1))*10;
       int t = (std::rand() % (max_teta + 1))*10;
       rays[0] = new ray(p,t);

}
