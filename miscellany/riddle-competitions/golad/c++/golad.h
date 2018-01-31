#ifndef GOLAD_H_
#define GOLAD_H_

#include "types.h"

void calculateNextState(move &m, int lookahead);
void calculateHeuristic(move &m, char myId);

#endif
