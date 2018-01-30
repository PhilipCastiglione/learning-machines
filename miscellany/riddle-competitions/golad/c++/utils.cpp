#include "utils.h"

/* PUBLIC FUNCTIONS */
int factorial(int x, int result = 1) {
  return (x == 1) ? result : factorial(x - 1, x * result);
}

bool moveCompare(move &lhs, move &rhs)
{
  // used to sort moves in descending order
  return lhs.b.heuristicValue > rhs.b.heuristicValue;
}

void copyState(const char source[][18], char target[][18])
{
  for (int r = 0; r < 16; r++) {
    for (int c = 0; c < 18; c++) {
      target[r][c] = source[r][c];
    }
  }
}
