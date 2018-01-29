#ifndef GAME_H_
#define GAME_H_ 

#include <iostream>
#include <sstream>
#include <string>
#include <algorithm>
#include <chrono> // TODO: remove

using namespace std;

struct node
{
  char state[16][18];
  int heuristicValue;
  char type;
  int targetIdx;
  char targetId;
  int sac1Idx;
  int sac2Idx;
};

void game();
void processAction();
void processUpdate();
void processSettings();
void parseState(const string &value);
void makeMove();
void addKillNodes(node nodes[], const char state[][18]);
void findBestKillNodes(const node nodes[], char id, node bestKillNodes[]);
void addPassNode(node nodes[], const char state[][18], int idx);
void addBirthNodes(node nodes[], const char state[][18], int id, const node bestKillNodes[], int idx);
void considerOpponentMoves(node nodes[]);
node findBestNode(const node nodes[], int nodeCount);
void sendMove(const node &n);
void calculateNextState(node &n, int lookahead);
void calculateHeuristic(node &n);
int factorial(int x, int result = 1);
string coords(int cellIdx);
void copyState(const char source[][18], char target[][18]);
bool nodeCompare(node lhs, node rhs);

// debug/test functions
void zeroGameState();
void pasteState(char target[][18]);
void setBotId(const char id);

#endif
