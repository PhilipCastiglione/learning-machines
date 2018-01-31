#include "skynet.h"
#include "api.h"

/* FORWARD DECLARATIONS */
// TODO: add these

/* PUBLIC FUNCTIONS */
void crushEnemies()
{
  game g;
  listenForInput(g, _act);
}

/* PRIVATE FUNCTIONS */
void _act(game &g)
{
  int numMoves = _numMovesFor(g.myCellCount + g.yourCellCount);
  move moves[numMoves];

  _buildMoves(g, moves, numMoves);

  // TODO: placeholder
  _projectOpponentMoves(g, moves);

  move m = _selectMove(moves);

  sendMove(m);
}

int _numMovesFor(int cellCount)
{
  int sacrificeCombinations;

  if (SACRIFICE_OPTIONS == 2) {
    sacrificeCombinations = 1;
  } else {
    sacrificeCombinations = factorial(SACRIFICE_OPTIONS) / (factorial(SACRIFICE_OPTIONS - 2) * factorial(2));
  }

  return 1 + (cellCount) + (sacrificeCombinations * (MAX_CELLS - cellCount));
}

void _buildMoves(const game &g, move moves[], int numMoves)
{
  _buildKillMoves(g, moves);
  _buildBirthMoves(g, moves);
  _buildPassMove(g, moves, numMoves);
}

void _buildKillMoves(const game &g, move moves[])
{
  int mIdx = 0;
  for (int i = 0; i < MAX_CELLS; i++) {
    if (state[i] != '.') {
      move m;
      m.type = 'k';
      m.targetId = state[i];
      m.targetIdx = i;

      copyState(g.b.state, m.b.state);
      m.b.state[i] = '.';

      calculateNextState(m.b, LOOKAHEAD);
      calculateHeuristic(m.b, g.myId);

      moves[mIdx++] = m;
    }
  }
}

void _buildBirthMoves(const game &g, move moves[])
{
  int mIdx = g.myCells + g.yourCells;
  int bestHeuristic, thisHeuristic;

  // swap the best n cells that are killing my own into the first n positions
  // in the moves array with the ones presently there
  for (int i = 0; i < SACRIFICE_OPTIONS; i++) {
    bestHeuristic = -MAX_CELLS;
    thisHeuristic = -MAX_CELLS;
    for (int j = i; j < mIdx; j++) {
      if (moves[j].targetId == g.myId) {
        thisHeuristic = moves[j].b.heuristicValue;
        if (thisHeuristic > bestHeuristic) {
          swap(moves[i], moves[j]);
          bestHeuristic = thisHeuristic;
        }
      }
    }
  }

  // for each combination of the best sacrifice targets, create a birth move
  // targeting each currently dead cell
  for (int s1 = 0; s1 < SACRIFICE_OPTIONS - 1; s1++) {
    for (int s2 = s1 + 1; s2 < SACRIFICE_OPTIONS; s2++) {
      for (int i = 0; i < MAX_CELLS; i++) {
        if (state[i] == '.') {
          move m;
          m.type = 'b';
          m.targetIdx = i;
          m.sac1Idx = moves[s1].targetIdx;
          m.sac2Idx = moves[s2].targetIdx;

          copyState(g.b.state, m.b.state);
          m.state[i] = g.myId;
          m.state[m.sac1Idx] = '.';
          m.state[m.sac2Idx] = '.';

          calculateNextState(m.b, LOOKAHEAD);
          calculateHeuristic(m.b, g.myId);

          moves[mIdx++] = m;
        }
      }
    }
  }
}

void _buildPassMove(const game &g, move moves[], int numMoves)
{
  move m;
  m.type = 'p';

  copyState(g.b.state, m.b.state);

  calculateNextState(m.b, LOOKAHEAD);
  calculateHeuristic(m.b, g.myId);

  moves[numMoves - 1] = m;
}

void _projectOpponentMoves(const game &g, move moves[])
{
}

move _selectMove(move moves[])
{
}
