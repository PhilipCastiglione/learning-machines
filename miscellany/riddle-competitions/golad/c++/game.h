#ifndef GAME_H_
#define GAME_H_ 

#include <iostream>
#include <sstream>
#include <string>
#include <algorithm>
#include <chrono> // TODO: remove

using namespace std;


/* Node is the primary structure representing a move and associated state */
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

void play();
game newGame();
void makeMove(const game &g);
void buildChildren(node nodes[], const char state[][18], char botId, int cellCount, int numMoves);
void addKillNodes(node nodes[], const char state[][18], char botId);
void findBestKillNodes(const node nodes[], char botId, node bestKillNodes[], int idx);
void addPassNode(node nodes[], const char state[][18], int idx, char botId);
void addBirthNodes(node nodes[], const char state[][18], const node bestKillNodes[], int idx, char botId);
void considerOpponentMoves(const game &g, node nodes[]);
node findBestNode(const node nodes[], int idxBound);

// debug/test functions
void zeroGameState();
void pasteState(char target[][18]);
void setBotId(const char id);

#endif
