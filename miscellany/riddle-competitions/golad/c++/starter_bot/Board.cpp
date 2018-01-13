#include "Board.h"
using namespace std;

Board::Board(int width, int height)
{
  this->width = width;
  this->height = height;
  board = new char *[width];
  for (int i = 0; i < width; ++i)
    board[i] = new char[height];
}

void Board::UpdateBoard(stringstream &stream)
{
  int x = 0, y = 0;
  string field;
  while (getline(stream, field, ','))
  {
    board[x][y] = field.at(0);
    x = (x + 1) % this->width;
    if (x == 0)
      y++;
  }
}

vector<Coordinate>* Board::GetCells(char type)
{
  vector<Coordinate> *selectedCells = new vector<Coordinate>;
  for (int x = 0; x < width; ++x)
  {
    for (int y = 0; y < height; ++y)
    {
      if (board[x][y] == type) {
        selectedCells->push_back(Coordinate(x, y));
      }
    }
  }
  return selectedCells;
}
