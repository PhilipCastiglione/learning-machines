#include "game.h"

using namespace std; // TODO: can I remove this?

/*
 * BOT PARAMETERS
 * These are parameters that can be varied to change bot performance. In
 * general, higher numbers result in smarter behaviour but slower runtime.
 */
int lookahead = 2;
int sacrificeOptions = 2;
int opponentMoves = 2;

void play()
{

  game g = newGame();

}

game newGame()
{
  game g;
  g.sacrificeCombinations = (sacrificeOptions == 2) ? 1 : factorial(sacrificeOptions) / (factorial(sacrificeOptions - 2) * factorial(2));
  return g;
}

void makeMove(const game &g)
{
  int cellCount = g.botCellCount + g.opponentCellCount;
  int numMoves = 1 + (cellCount) + (g.sacrificeCombinations * (288 - cellCount));

  node nodes[numMoves];

  buildChildren(nodes, g.state, g.botId, cellCount, numMoves);
  // TODO: remove
  for (int i = 0; i < numMoves; i++) {
    cerr << "node " << i << nodes[i].type<< ": " << nodes[i].heuristicValue << "\n";
  }
  considerOpponentMoves(g, nodes);
  // TODO: remove
  for (int i = 0; i < numMoves; i++) {
    cerr << "node " << i << nodes[i].type<< ": " << nodes[i].heuristicValue << "\n";
  }

  node bestNode = findBestNode(nodes, opponentMoves);

  sendMove(bestNode);
}

void buildChildren(node nodes[], const char state[][18], char botId, int cellCount, int numMoves)
{
  // TODO: handle less then n of my cells alive for birthing calcs
  addKillNodes(nodes, state, botId);

  node bestKillNodes[sacrificeOptions];

  sort(nodes, nodes + cellCount, nodeCompare);

  findBestKillNodes(nodes, botId, bestKillNodes, cellCount);

  addPassNode(nodes, state, cellCount, botId);

  addBirthNodes(nodes, state, bestKillNodes, cellCount + 1, botId);

  sort(nodes, nodes + numMoves, nodeCompare);
}

void addKillNodes(node nodes[], const char state[][18], char botId)
{
  int i = 0;
  for (int r = 0; r < 16; r++) {
    for (int c = 0; c < 18; c++) {
      if (state[r][c] != '.') {
        node n;
        n.targetId = state[r][c];
        n.type = 'k';
        n.targetIdx = r * 18 + c;
        copyState(state, n.state);
        n.state[r][c] = '.';
        calculateNextState(n, lookahead);
        calculateHeuristic(n, botId);
        nodes[i++] = n;
      }
    }
  }
}

void findBestKillNodes(const node nodes[], char botId, node bestKillNodes[], int idx)
{
  int killNodeCount = 0;
  for (int i = 0; i < idx; i++) {
    if (nodes[i].targetId == botId) {
      bestKillNodes[killNodeCount++] = nodes[i];

      if (killNodeCount == sacrificeOptions) {
        break;
      }
    }
  }
}

void addPassNode(node nodes[], const char state[][18], int idx, char botId)
{
  node n;
  n.type = 'p';
  copyState(state, n.state);
  calculateNextState(n, lookahead);
  calculateHeuristic(n, botId);
  nodes[idx] = n;
}

void addBirthNodes(node nodes[], const char state[][18], const node bestKillNodes[], int idx, char botId)
{
  for (int x = 0; x < sacrificeOptions - 1; x++) {
    for (int y = x + 1; y < sacrificeOptions; y++) {
      for (int r = 0; r < 16; r++) {
        for (int c = 0; c < 18; c++) {
          if (state[r][c] == '.') {
            node n;
            n.type = 'b';
            n.targetIdx = r * 18 + c;
            n.sac1Idx = bestKillNodes[x].targetIdx;
            n.sac2Idx = bestKillNodes[y].targetIdx;
            copyState(state, n.state);
            n.state[r][c] = botId;
            n.state[n.sac1Idx / 18][n.sac1Idx % 18] = '.';
            n.state[n.sac2Idx / 18][n.sac2Idx % 18] = '.';
            calculateNextState(n, lookahead);
            calculateHeuristic(n, botId);
            nodes[idx++] = n;
          }
        }
      }
    }
  }
}

void considerOpponentMoves(const game &g, node nodes[])
{
  for (int i = 0; i < opponentMoves; i++) {
    node n = nodes[i];

    int liveCellCount = 0;

    for (int r = 0; r < 16; r++) {
      for (int c = 0; c < 18; c++) {
        if (n.state[r][c] != '.')
          liveCellCount++;
      }
    }

    int numMoves = 1 + (liveCellCount) + (g.sacrificeCombinations * (288 - liveCellCount));

    node childNodes[numMoves];

    buildChildren(childNodes, n.state, g.opponentId, liveCellCount, numMoves);

    n.heuristicValue = childNodes[numMoves - 1].heuristicValue;
  }
}

node findBestNode(const node nodes[], int idxBound)
{
  int topHeuristic = -288;
  int topHeuristicIdx = 0;
  for (int i = 0; i < idxBound; i++) {
    if (nodes[i].heuristicValue > topHeuristic) {
      topHeuristic = nodes[topHeuristicIdx].heuristicValue;
      topHeuristicIdx = i;
    }
  }

  return nodes[topHeuristicIdx];
}

// debug/test functions
void zeroGameState()
{
  game g; //  TODO: remove, tests not on now
  for (int r = 0; r < 16; r++) {
    for (int c = 0; c < 18; c++) {
      g.state[r][c] = '.';
    }
  }
}

void pasteState(char target[][18])
{
  game g; //  TODO: remove, tests not on now
  for (int r = 0; r < 16; r++) {
    for (int c = 0; c < 18; c++) {
      target[r][c] = g.state[r][c];
    }
  }
}

void setBotId(const char id)
{
  game g; //  TODO: remove, tests not on now
  g.botId = id;
}

