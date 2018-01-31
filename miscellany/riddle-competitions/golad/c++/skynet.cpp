#include "skynet.h"
#include "api.h"

/* FORWARD DECLARATIONS */

/* PUBLIC FUNCTIONS */
void crushEnemies()
{
  game g;
  listenForInput(g, _act);
}

/* PRIVATE FUNCTIONS */
void _act(game &g)
{
  move moves[_numMovesFor(g.myCellCount + g.yourCellCount)];

  _buildMoves(g, moves);

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

void _buildMoves(const game &g, move moves[])
{
  // TODO: placeholder
  _buildKillMoves(g, moves);
  _buildBirthMoves();
  _buildPassMove();
}

void _buildKillMoves(const game &g, move moves[])
{
}

void _projectOpponentMoves(const game &g, move moves[])
{
}

move _selectMove(move moves[])
{
}
