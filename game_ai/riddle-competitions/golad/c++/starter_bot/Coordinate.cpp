#include "Coordinate.h"
using namespace std;

Coordinate::Coordinate(int x, int y)
{
    this->x = x;
    this->y = y;
}

string Coordinate::toString()
{
    ostringstream stringStream;
    stringStream << x << "," << y;
    return stringStream.str();
}