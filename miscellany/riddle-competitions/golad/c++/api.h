#ifndef API_H_
#define API_H_

#include <functional>
#include <chrono>

#include "types.h"

using namespace std;

void listenForInput(game &g, function<void (game &g)> act);
void sendMove(const move &m);

#endif
