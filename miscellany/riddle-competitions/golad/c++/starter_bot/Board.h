#ifndef BOARD_h
#define BOARD_h

#include <sstream>
#include <vector>
#include "Enums.h"
#include "Coordinate.h"
using namespace std;

class Board {
private:
  int width, height;
  char **board;
public:
  Board(int width, int height);
  virtual void UpdateBoard(stringstream &stream);
  virtual vector<Coordinate>* GetCells(char type);
};

#endif
