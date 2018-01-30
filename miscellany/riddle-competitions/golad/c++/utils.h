#ifndef UTILS_H_
#define UTILS_H_

#include "types.h"

int factorial(int x, int result = 1);
bool moveCompare(move &lhs, move &rhs);
void copyState(const char source[][18], char target[][18]);

#endif
