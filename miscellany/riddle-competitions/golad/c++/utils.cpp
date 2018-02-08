#include "utils.h"

/* PUBLIC FUNCTIONS */
int factorial(int x, int result) {
  return (x == 1) ? result : factorial(x - 1, x * result);
}

bool moveCompare(gameMove &lhs, gameMove &rhs)
{
  // used to sort moves in descending order
  return lhs.b.heuristicValue > rhs.b.heuristicValue;
}

void copyState(const char source[], char target[])
{
  for (int i = 0; i < MAX_CELLS; i++) {
    target[i] = source[i];
  }
}
