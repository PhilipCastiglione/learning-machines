#include "test.h"
#include "game.h"

#include <assert.h>

using namespace std;

char testState[16][18];

void test()
{
  cout << "Beginning tests.\n";

  testParseState();
  cout << "fn parseState passed all tests.\n";

  node n;

  testCalculateHeuristic(n);
  cout << "fn calculateHeuristic passed all tests.\n";

  testCalculateNextState(n);
  cout << "fn calculateNextState passed all tests.\n";

  cout << "Finished tests with no failures. Yay.\n";
}

void testParseState()
{
  // build expected state
  char es[16][18];
  es[0][0] = '.'; es[0][1] = '.'; es[0][2] = '.'; es[0][3] = '.'; es[0][4] = '.'; es[0][5] = '0'; es[0][6] = '0'; es[0][7] = '.'; es[0][8] = '.'; es[0][9] = '.'; es[0][10] = '.'; es[0][11] = '.'; es[0][12] = '.'; es[0][13] = '1'; es[0][14] = '.'; es[0][15] = '1'; es[0][16] = '.'; es[0][17] = '.'; es[1][0] = '.'; es[1][1] = '.'; es[1][2] = '.'; es[1][3] = '.'; es[1][4] = '.'; es[1][5] = '.'; es[1][6] = '0'; es[1][7] = '0'; es[1][8] = '.'; es[1][9] = '0'; es[1][10] = '.'; es[1][11] = '.'; es[1][12] = '.'; es[1][13] = '.'; es[1][14] = '.'; es[1][15] = '1'; es[1][16] = '.'; es[1][17] = '.'; es[2][0] = '.'; es[2][1] = '.'; es[2][2] = '1'; es[2][3] = '.'; es[2][4] = '.'; es[2][5] = '.'; es[2][6] = '.'; es[2][7] = '.'; es[2][8] = '.'; es[2][9] = '.'; es[2][10] = '.'; es[2][11] = '0'; es[2][12] = '.'; es[2][13] = '.'; es[2][14] = '1'; es[2][15] = '1'; es[2][16] = '1'; es[2][17] = '.'; es[3][0] = '1'; es[3][1] = '.'; es[3][2] = '.'; es[3][3] = '.'; es[3][4] = '1'; es[3][5] = '.'; es[3][6] = '1'; es[3][7] = '1'; es[3][8] = '.'; es[3][9] = '.'; es[3][10] = '.'; es[3][11] = '.'; es[3][12] = '.'; es[3][13] = '.'; es[3][14] = '0'; es[3][15] = '.'; es[3][16] = '1'; es[3][17] = '.'; es[4][0] = '1'; es[4][1] = '.'; es[4][2] = '.'; es[4][3] = '.'; es[4][4] = '.'; es[4][5] = '.'; es[4][6] = '1'; es[4][7] = '.'; es[4][8] = '.'; es[4][9] = '.'; es[4][10] = '1'; es[4][11] = '.'; es[4][12] = '1'; es[4][13] = '0'; es[4][14] = '1'; es[4][15] = '.'; es[4][16] = '.'; es[4][17] = '0'; es[5][0] = '.'; es[5][1] = '0'; es[5][2] = '.'; es[5][3] = '.'; es[5][4] = '0'; es[5][5] = '.'; es[5][6] = '.'; es[5][7] = '.'; es[5][8] = '1'; es[5][9] = '.'; es[5][10] = '.'; es[5][11] = '.'; es[5][12] = '1'; es[5][13] = '.'; es[5][14] = '.'; es[5][15] = '.'; es[5][16] = '1'; es[5][17] = '.'; es[6][0] = '1'; es[6][1] = '.'; es[6][2] = '.'; es[6][3] = '0'; es[6][4] = '0'; es[6][5] = '.'; es[6][6] = '0'; es[6][7] = '.'; es[6][8] = '.'; es[6][9] = '.'; es[6][10] = '.'; es[6][11] = '.'; es[6][12] = '.'; es[6][13] = '.'; es[6][14] = '.'; es[6][15] = '.'; es[6][16] = '.'; es[6][17] = '.'; es[7][0] = '.'; es[7][1] = '.'; es[7][2] = '.'; es[7][3] = '.'; es[7][4] = '1'; es[7][5] = '1'; es[7][6] = '0'; es[7][7] = '0'; es[7][8] = '0'; es[7][9] = '.'; es[7][10] = '.'; es[7][11] = '.'; es[7][12] = '.'; es[7][13] = '0'; es[7][14] = '.'; es[7][15] = '.'; es[7][16] = '.'; es[7][17] = '0'; es[8][0] = '.'; es[8][1] = '0'; es[8][2] = '.'; es[8][3] = '.'; es[8][4] = '.'; es[8][5] = '1'; es[8][6] = '.'; es[8][7] = '.'; es[8][8] = '0'; es[8][9] = '.'; es[8][10] = '1'; es[8][11] = '1'; es[8][12] = '.'; es[8][13] = '.'; es[8][14] = '.'; es[8][15] = '1'; es[8][16] = '0'; es[8][17] = '.'; es[9][0] = '0'; es[9][1] = '.'; es[9][2] = '.'; es[9][3] = '.'; es[9][4] = '0'; es[9][5] = '.'; es[9][6] = '.'; es[9][7] = '1'; es[9][8] = '.'; es[9][9] = '.'; es[9][10] = '0'; es[9][11] = '0'; es[9][12] = '.'; es[9][13] = '.'; es[9][14] = '1'; es[9][15] = '.'; es[9][16] = '.'; es[9][17] = '.'; es[10][0] = '.'; es[10][1] = '.'; es[10][2] = '.'; es[10][3] = '.'; es[10][4] = '.'; es[10][5] = '.'; es[10][6] = '1'; es[10][7] = '1'; es[10][8] = '.'; es[10][9] = '1'; es[10][10] = '0'; es[10][11] = '0'; es[10][12] = '.'; es[10][13] = '.'; es[10][14] = '.'; es[10][15] = '.'; es[10][16] = '.'; es[10][17] = '.'; es[11][0] = '.'; es[11][1] = '.'; es[11][2] = '.'; es[11][3] = '.'; es[11][4] = '.'; es[11][5] = '.'; es[11][6] = '.'; es[11][7] = '.'; es[11][8] = '.'; es[11][9] = '.'; es[11][10] = '1'; es[11][11] = '.'; es[11][12] = '1'; es[11][13] = '.'; es[11][14] = '.'; es[11][15] = '0'; es[11][16] = '.'; es[11][17] = '.'; es[12][0] = '.'; es[12][1] = '.'; es[12][2] = '.'; es[12][3] = '0'; es[12][4] = '.'; es[12][5] = '.'; es[12][6] = '.'; es[12][7] = '.'; es[12][8] = '.'; es[12][9] = '.'; es[12][10] = '.'; es[12][11] = '.'; es[12][12] = '.'; es[12][13] = '1'; es[12][14] = '.'; es[12][15] = '.'; es[12][16] = '.'; es[12][17] = '0'; es[13][0] = '.'; es[13][1] = '0'; es[13][2] = '1'; es[13][3] = '0'; es[13][4] = '.'; es[13][5] = '0'; es[13][6] = '.'; es[13][7] = '.'; es[13][8] = '0'; es[13][9] = '0'; es[13][10] = '.'; es[13][11] = '.'; es[13][12] = '.'; es[13][13] = '1'; es[13][14] = '.'; es[13][15] = '1'; es[13][16] = '.'; es[13][17] = '1'; es[14][0] = '.'; es[14][1] = '1'; es[14][2] = '.'; es[14][3] = '.'; es[14][4] = '.'; es[14][5] = '.'; es[14][6] = '.'; es[14][7] = '.'; es[14][8] = '0'; es[14][9] = '0'; es[14][10] = '0'; es[14][11] = '.'; es[14][12] = '.'; es[14][13] = '.'; es[14][14] = '.'; es[14][15] = '0'; es[14][16] = '.'; es[14][17] = '.'; es[15][0] = '.'; es[15][1] = '.'; es[15][2] = '.'; es[15][3] = '.'; es[15][4] = '1'; es[15][5] = '.'; es[15][6] = '.'; es[15][7] = '.'; es[15][8] = '.'; es[15][9] = '.'; es[15][10] = '.'; es[15][11] = '.'; es[15][12] = '.'; es[15][13] = '0'; es[15][14] = '.'; es[15][15] = '.'; es[15][16] = '0'; es[15][17] = '.';

  string inputState = ".,.,.,.,.,0,0,.,.,.,.,.,.,1,.,1,.,.,.,.,.,.,.,.,0,0,.,0,.,.,.,.,.,1,.,.,.,.,1,.,.,.,.,.,.,.,.,0,.,.,1,1,1,.,1,.,.,.,1,.,1,1,.,.,.,.,.,.,0,.,1,.,1,.,.,.,.,.,1,.,.,.,1,.,1,0,1,.,.,0,.,0,.,.,0,.,.,.,1,.,.,.,1,.,.,.,1,.,1,.,.,0,0,.,0,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,1,1,0,0,0,.,.,.,.,0,.,.,.,0,.,0,.,.,.,1,.,.,0,.,1,1,.,.,.,1,0,.,0,.,.,.,0,.,.,1,.,.,0,0,.,.,1,.,.,.,.,.,.,.,.,.,1,1,.,1,0,0,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,1,.,1,.,.,0,.,.,.,.,.,0,.,.,.,.,.,.,.,.,.,1,.,.,.,0,.,0,1,0,.,0,.,.,0,0,.,.,.,1,.,1,.,1,.,1,.,.,.,.,.,.,0,0,0,.,.,.,.,0,.,.,.,.,.,.,1,.,.,.,.,.,.,.,.,0,.,.,0,.";

  parseState(inputState);
  copyState(testState);

  // test testState against expected state
  for (int c = 0; c < 18; c++) {
    for (int r = 0; r < 16; r++) {
      assert(testState[r][c] == es[r][c]);
    }
  }
}

void testCalculateHeuristic(node &n)
{
  // heuristic calculation depends on which player we are
  setBotId('1');

  copyState(n.state);
  calculateHeuristic(n);

  // the input state we copied in earlier has a heuristic value of 1
  assert(n.heuristicValue == -1);
}

void testCalculateNextState(node &n)
{
  // push the expected next state into the global state var in game, then ns
  string nextState = ".,.,.,.,.,0,0,0,.,.,.,.,.,.,1,.,.,.,.,.,.,.,.,0,0,0,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,1,.,.,0,.,.,.,.,.,1,.,1,.,.,1,.,.,.,1,1,1,.,.,.,1,0,.,.,.,1,1,1,1,.,.,.,.,1,.,.,.,.,1,1,.,1,.,1,0,1,0,.,0,0,.,.,1,.,.,.,1,1,.,.,.,.,.,.,.,.,0,.,.,0,.,0,.,.,.,.,.,.,.,.,.,.,.,.,0,.,.,.,.,0,0,.,.,.,.,.,.,0,.,.,.,.,.,.,.,.,.,0,.,1,1,0,.,1,1,0,.,.,.,.,.,.,1,.,1,.,.,.,.,0,.,.,1,.,.,.,.,.,.,.,.,1,1,1,1,.,.,0,.,.,.,.,.,.,.,.,.,.,.,.,.,.,1,1,.,1,.,.,.,.,.,.,.,.,0,0,.,.,.,.,0,.,.,1,1,.,.,.,.,.,0,.,0,0,.,.,.,0,.,0,.,.,.,.,.,.,.,.,1,.,1,0,.,.,.,0,.,0,.,.,.,.,0,.,.,.,.,.,.,.,.,.,.,.,0,.,.,.,.,.,.,.,.";
  parseState(nextState);
  char ns[16][18];
  copyState(ns);

  calculateNextState(n);

  // test the new node state against expected next state
  for (int c = 0; c < 18; c++) {
    for (int r = 0; r < 16; r++) {
      assert(n.state[r][c] == ns[r][c]);
    }
  }
}
