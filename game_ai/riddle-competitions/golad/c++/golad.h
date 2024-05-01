#ifndef GOLAD_H_
#define GOLAD_H_

#include "types.h"

void calculateNextState(board &b, int lookahead);
void calculateHeuristic(board &b, char myId);

#endif
