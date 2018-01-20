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
  int target;
  char value;
  int sacrifice1;
  int sacrifice2;
};

void game();
void processAction();
void processUpdate();
void processSettings();
void parseState(const string &value);
void makeMove();
void addKillNodes(node nodes[]);
void findBestKillNodes(node nodes[], node bestKillNodes[]);
void addPassNode(node nodes[]);
void addBirthNodes(node nodes[], const node bestKillNodes[]);
node findBestNode(const node nodes[], int nodeCount);
void sendMove(const node &n);
void calculateNextState(node &n);
void calculateHeuristic(node &n);
int factorial(int x, int result = 1);
string coords(int cellIdx);
void copyState(char target[][18]);
bool nodeCompare(node lhs, node rhs);
void setBotId(const char id);

#endif
