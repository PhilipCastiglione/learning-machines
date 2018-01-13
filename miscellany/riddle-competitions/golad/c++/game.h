#ifndef GAME_H_
#define GAME_H_ 

#include <iostream>
#include <sstream>

using namespace std;

struct node
{
  char state[16][18];
  int heuristicValue;
  char type;
};

void game();
void processAction();
void processUpdate();
void processSettings();
void parseState(const string value);
void makeMove();
void addPassNodes(node nodes[]);
void addKillNodes(node nodes[]);
void findBestKillNodes(const node nodes[], int bestKillMoves[]);
void addBirthNodes(node nodes[], const int bestKillMoves[]);
void copyState(char target[][18]);
void calculateNextState(node n);
void calculateHeuristic(node n);

#endif
