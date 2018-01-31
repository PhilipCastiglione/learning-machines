#ifndef TYPES_H_
#define TYPES_H_

#define ROWS 16
#define COLS 18
#define MAX_CELLS (ROWS * COLS)

/**
 * The board object contains a state representation and an associated value.
 */
struct board
{
  char state[MAX_CELLS];
  int heuristicValue;
};

/**
 * The game object contains information about the current game state.
 */
struct game
{
  board b;
  char myId;
  char yourId;
  int roundNum;
  int timebank;
  int myCellCount;
  int yourCellCount;
  int sacrificeCombinations; // TODO: this is questionable
};

/**
 * The move object represents a potential move and its attributes.
 */
struct move
{
  board b;
  char type;
  int targetIdx;
  char targetId;
  int sac1Idx;
  int sac2Idx;
};

#endif
