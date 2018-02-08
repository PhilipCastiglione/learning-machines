#include "skynet.h"

/* FORWARD DECLARATIONS */
void _act(game &g);
int _numMovesFor(int cellCount);
void _buildMoves(const game &g, gameMove moves[], int numMoves);
void _buildKillMoves(const game &g, gameMove moves[]);
void _buildBirthMoves(const game &g, gameMove moves[]);
void _buildPassMove(const game &g, gameMove moves[], int numMoves);
void _projectOpponentMoves(const game &g, gameMove moves[]);
game gameAfterMove(const game &g, const gameMove &m);
gameMove _selectMove(gameMove moves[]);

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
  gameMove moves[numMoves];

  _buildMoves(g, moves, numMoves);

  _projectOpponentMoves(g, moves);

  gameMove m = _selectMove(moves);

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

void _buildMoves(const game &g, gameMove moves[], int numMoves)
{
  _buildKillMoves(g, moves);
  _buildBirthMoves(g, moves);
  _buildPassMove(g, moves, numMoves);
  sort(moves, moves + numMoves, moveCompare);
}

void _buildKillMoves(const game &g, gameMove moves[])
{
  int mIdx = 0;
  for (int i = 0; i < MAX_CELLS; i++) {
    if (g.b.state[i] != '.') {
      gameMove m;
      m.type = 'k';
      m.targetId = g.b.state[i];
      m.targetIdx = i;

      copyState(g.b.state, m.b.state);
      m.b.state[i] = '.';

      calculateNextState(m.b, LOOKAHEAD);
      calculateHeuristic(m.b, g.myId);

      moves[mIdx++] = m;
    }
  }
}

void _buildBirthMoves(const game &g, gameMove moves[])
{
  int mIdx = g.myCellCount + g.yourCellCount;
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
        if (g.b.state[i] == '.') {
          gameMove m;
          m.type = 'b';
          m.targetIdx = i;
          m.sac1Idx = moves[s1].targetIdx;
          m.sac2Idx = moves[s2].targetIdx;

          copyState(g.b.state, m.b.state);
          m.b.state[i] = g.myId;
          m.b.state[m.sac1Idx] = '.';
          m.b.state[m.sac2Idx] = '.';

          calculateNextState(m.b, LOOKAHEAD);
          calculateHeuristic(m.b, g.myId);

          moves[mIdx++] = m;
        }
      }
    }
  }
}

void _buildPassMove(const game &g, gameMove moves[], int numMoves)
{
  gameMove m;
  m.type = 'p';

  copyState(g.b.state, m.b.state);

  calculateNextState(m.b, LOOKAHEAD);
  calculateHeuristic(m.b, g.myId);

  moves[numMoves - 1] = m;
}

void _projectOpponentMoves(const game &g, gameMove moves[])
{
  // for each move we want to look at, create a game state as though that move
  // has been taken, then build out the next moves (from opponents perspective)
  for (int i = 0; i < OPPONENT_MOVES; i++) {
    game childGame = gameAfterMove(g, moves[i]);

    int numMoves = _numMovesFor(childGame.myCellCount + childGame.yourCellCount);
    gameMove childMoves[numMoves];

    _buildMoves(childGame, childMoves, numMoves);

    // update the heuristic to the heuristicValue from our perspective, of what
    // the opponent considered their best move
    calculateHeuristic(childMoves[0].b, g.myId);
    moves[i].b.heuristicValue = childMoves[0].b.heuristicValue;
  }
}

game gameAfterMove(const game &g, const gameMove &m)
{
    game childGame;
    childGame.b = m.b;
    childGame.myId = g.yourId;
    childGame.yourId = g.myId;
    childGame.myCellCount = 0;
    childGame.yourCellCount = 0;

    for (int c = 0; c < MAX_CELLS; c++) {
      if (childGame.b.state[c] == childGame.myId) {
        childGame.myCellCount++;
      } else if (childGame.b.state[c] == childGame.yourId) {
        childGame.yourCellCount++;
      }
    }

    return childGame;
}

gameMove _selectMove(gameMove moves[])
{
  sort(moves, moves + OPPONENT_MOVES, moveCompare);

  return moves[0];
}
