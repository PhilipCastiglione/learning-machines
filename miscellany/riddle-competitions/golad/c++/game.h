#ifndef GAME_H_
#define GAME_H_ 

#include <iostream>
#include <sstream>

using namespace std;

struct node
{
  char state[16][18];
};

void game();
void processAction();
void processUpdate();
void processSettings();
void parseState(const string value);
void makeMove();
void calculatePass(node nodes[]);
void calculateKill(node nodes[]);
void findBestKillMoves(const node nodes[], int bestKillMoves[]);
void calculateBirth(node nodes[], const int bestKillMoves[]);
void copyState(char target[][18]);
void calculateNextState(node n);

#endif
