#include "golad.h"

/* PUBLIC FUNCTIONS */
void calculateNextState(move &m, int lookahead)
{
  for (int l = 0; l < lookahead; l++) {
    int neighbours0[16][18];
    int neighbours1[16][18];

    for (int r = 0; r < 16; r++) {
      for (int c = 0; c < 18; c++) {
        neighbours0[r][c] = 0;
        neighbours1[r][c] = 0;
      }
    }

    for (int r = 0; r < 16; r++) {
      for (int c = 0; c < 18; c++) {
        if (m.b.state[r][c] == '0') {
          if (c > 0) {
            neighbours0[r][c - 1]++;
            if (r > 0) neighbours0[r - 1][c - 1]++;
            if (r < 15) neighbours0[r + 1][c - 1]++;
          }
          if (c < 17) {
            neighbours0[r][c + 1]++;
            if (r > 0) neighbours0[r - 1][c + 1]++;
            if (r < 15) neighbours0[r + 1][c + 1]++;
          }
          if (r > 0) neighbours0[r - 1][c]++;
          if (r < 15) neighbours0[r + 1][c]++;
        }
        if (m.b.state[r][c] == '1') {
          if (c > 0) {
            neighbours1[r][c - 1]++;
            if (r > 0) neighbours1[r - 1][c - 1]++;
            if (r < 15) neighbours1[r + 1][c - 1]++;
          }
          if (c < 17) {
            neighbours1[r][c + 1]++;
            if (r > 0) neighbours1[r - 1][c + 1]++;
            if (r < 15) neighbours1[r + 1][c + 1]++;
          }
          if (r > 0) neighbours1[r - 1][c]++;
          if (r < 15) neighbours1[r + 1][c]++;
        }
      }
    }

    int neighbours;
    for (int r = 0; r < 16; r++) {
      for (int c = 0; c < 18; c++) {
        neighbours = neighbours0[r][c] + neighbours1[r][c];
        if (m.b.state[r][c] == '.' and neighbours == 3) {
          m.b.state[r][c] = (neighbours0[r][c] > neighbours1[r][c]) ? '0' : '1';
        } else if (m.b.state[r][c] != '.' and (neighbours < 2 or neighbours > 3)) {
          m.b.state[r][c] = '.';
        }
      }
    }
  }
}

// TODO: consider the number of opponent cells alive to increase aggression when they are low
void calculateHeuristic(move &m, char myId)
{
  char yourId = (myId == '0')? '1' : '0';

  int myCellCount = 0;
  int yourCellCount = 0;

  for (int r = 0; r < 16; r++) {
    for (int c = 0; c < 18; c++) {
      if (m.b.state[r][c] == myId) {
        myCellCount++;
      } else if (m.b.state[r][c] == yourId) {
        yourCellCount++;
      }
    }
  }

  // Shortcuts;
  //  - if we are out of cells, avoid at all costs; or
  //  - if they have no cells, choose at any cost
  if (myCellCount == 0) {
    m.b.heuristicValue = -MAX_HEURISTIC;
  } else if (yourCellCount == 0) {
    m.b.heuristicValue = MAX_HEURISTIC;
  } else {
    m.b.heuristicValue = myCellCount - yourCellCount;
  }
}
