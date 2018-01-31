#include "golad.h"

/* PUBLIC FUNCTIONS */
void calculateNextState(board &b, int lookahead)
{
  for (int l = 0; l < lookahead; l++) {
    // in our first pass, we build up arrays of counts of neighbours
    int neighbours0[MAX_CELLS];
    int neighbours1[MAX_CELLS];
    for (int i = 0; i < MAX_CELLS; i++) {
      neighbours0[i] = 0;
      neighbours1[i] = 0;
    }

    // calculating the next state takes a substantial amount of skynets
    // computation, so this is all unrolled, optimising for speed
    for (int i = 0; i < MAX_CELLS; i++) {
      if (b.state[i] == '0') {
        if (i % COLS > 0) {              // not on left edge
          neighbours0[i - 1]++;          // add to left cell neighbour
          if (i >= COLS)                 // not on top edge
            neighbours0[i - COLS - 1]++; // add to top left cell neighbour
          if (i <= MAX_CELLS - COLS - 1) // not on bottom edge
            neighbours0[i + COLS - 1]++; // add to bottom left cell neighbour
        }
        if (i % COLS < COLS - 1) {       // not on right edge
          neighbours0[i + 1]++;          // add to right cell neighbour
          if (i >= COLS)                 // not on top edge
            neighbours0[i - COLS + 1]++; // add to top right cell neighbour
          if (i <= MAX_CELLS - COLS - 1) // not on bottom edge
            neighbours0[i + COLS + 1]++; // add to bottom right cell neighbour
        }
        if (i >= COLS)                   // not on top edge
          neighbours0[i - COLS]++;       // add to top neighbour
        if (i <= MAX_CELLS - COLS - 1)   // not on bottom edge
          neighbours0[i - COLS]++;       // add to bottom neighbour
      } else if (b.state[i] == '1') {
        if (i % COLS > 0) {              // not on left edge
          neighbours1[i - 1]++;          // add to left cell neighbour
          if (i >= COLS)                 // not on top edge
            neighbours1[i - COLS - 1]++; // add to top left cell neighbour
          if (i <= MAX_CELLS - COLS - 1) // not on bottom edge
            neighbours1[i + COLS - 1]++; // add to bottom left cell neighbour
        }
        if (i % COLS < COLS - 1) {       // not on right edge
          neighbours1[i + 1]++;          // add to right cell neighbour
          if (i >= COLS)                 // not on top edge
            neighbours1[i - COLS + 1]++; // add to top right cell neighbour
          if (i <= MAX_CELLS - COLS - 1) // not on bottom edge
            neighbours1[i + COLS + 1]++; // add to bottom right cell neighbour
        }
        if (i >= COLS)                   // not on top edge
          neighbours1[i - COLS]++;       // add to top neighbour
        if (i <= MAX_CELLS - COLS - 1)   // not on bottom edge
          neighbours1[i - COLS]++;       // add to bottom neighbour
      }
    }

    // in our second pass, we use the neighbours todetermine the next cell state
    int neighbours;
    for (int i = 0; i < MAX_CELLS; i++) {
      neighbours = neighbours0[i] + neighbours1[i];
      if (b.state[i] == '.' and neighbours == 3) {                           // dead, will grow new cell
        b.state[i] = (neighbours0[i] > neighbours1[i]) ? '0' : '1';          // majority parent wins
      } else if (b.state[i] != '.' and (neighbours < 2 or neighbours > 3)) { // alive, will die
        b.state[i] = '.';                                                    // ded
      }
    }
  }
}

// TODO: consider the number of opponent cells alive to increase aggression when they are low
void calculateHeuristic(board &b, char myId)
{
  char yourId = (myId == '0')? '1' : '0';

  int myCellCount = 0;
  int yourCellCount = 0;

  for (int r = 0; r < ROWS; r++) {
    for (int c = 0; c < COLS; c++) {
      if (b.state[r * COLS + c] == myId) {
        myCellCount++;
      } else if (b.state[r * COLS + c] == yourId) {
        yourCellCount++;
      }
    }
  }

  // Shortcuts;
  //  - if we are out of cells, avoid at all costs; or
  //  - if they have no cells, choose at any cost
  if (myCellCount == 0) {
    b.heuristicValue = -MAX_CELLS;
  } else if (yourCellCount == 0) {
    b.heuristicValue = MAX_CELLS;
  } else {
    b.heuristicValue = myCellCount - yourCellCount;
  }
}
