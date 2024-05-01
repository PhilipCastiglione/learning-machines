#ifndef COORDINATE_H
#define COORDINATE_H

#include <iostream>
#include <sstream>
#include <stdio.h>
using namespace std;

class Coordinate
{
public:
    int x, y;
    Coordinate(int x, int y);
    virtual string toString();
};

#endif