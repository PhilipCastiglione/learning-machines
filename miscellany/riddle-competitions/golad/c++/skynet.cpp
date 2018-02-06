#include "skynet.h"

/* FORWARD DECLARATIONS */
void _act(game &g);
int _numMovesFor(int cellCount);
void _buildMoves(const game &g, move moves[], int numMoves);
void _buildKillMoves(const game &g, move moves[]);
void _buildBirthMoves(const game &g, move moves[])
void _buildPassMove(const game &g, move moves[], int numMoves);
void _projectOpponentMoves(const game &g, move moves[]);
game gameAfterMove(const game &g, const move &m);
move _selectMove(move moves[]);

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
  sort(moves, moves + numMoves, moveCompare);
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
  // for each move we want to look at, create a game state as though that move
  // has been taken, then build out the next moves (from opponents perspective)
  for (int i = 0; i < OPPONENT_MOVES; i++) {
    game childGame = gameAfterMove(g, move[i]);

    int numMoves = _numMovesFor(childGame.myCellCount + childGame.yourCellCount);
    move childMoves[numMoves];

    _buildMoves(childGame, childMoves, numMoves);

    // update the heuristic to the heuristicValue from our perspective, of what
    // the opponent considered their best move
    calculateHeuristic(childMoves[0].b, g.myId);
    move[i].b.heuristicValue = childMoves[0].b.heuristicValue;
  }
}

game gameAfterMove(const game &g, const move &m)
{
    game childGame;
    childGame.b = m.b;
    childGame.myId = g.yourId;
    childGame.yourId = g.myId;
    childGame.myCellCount = 0;
    childGame.yourCellCount = 0;

    for (int c = 0; c < MAX_CELLS; c++) {
      if (childGame.b[c] == childGame.myId) {
        childGame.myCellCount++;
      } else if (childGame.b[c] == childGame.yourId) {
        childGame.yourCellCount++;
      }
    }

    return childGame;
}

move _selectMove(move moves[])
{
  sort(moves, moves + OPPONENT_MOVES, moveCompare);

  return moves[i];
}
