#ifndef GAME_H_
#define GAME_H_ 

#include <iostream>
#include <sstream>

using namespace std;

void game();
void processAction();
void processUpdate();
void processSettings();
void parseState(const string value);

#endif
