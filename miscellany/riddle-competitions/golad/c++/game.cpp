#include "game.h"

using namespace std;

stringstream token;
char botId;
char state[16][18];
int round, timebank, myLiveCells, theirLiveCells;

void game()
{
  string line, command;

  while (getline(cin, line))
  {
    token.clear();
    token.str(line);
    token >> command;

    if (command == "action")
      processAction();
    if (command == "update")
      processUpdate();
    if (command == "settings")
      processSettings();
  }
}

void processAction()
{
  string type, time;
  token >> type;
  token >> time;

  if (type == "move") {
    timebank = stoi(time);
    makeMove();
  } else
    cerr << "action type: " << type << " not expected\n";
}

void processUpdate()
{
  string target, field, value;
  token >> target;
  token >> field;
  token >> value;

  if (target == "game") {
    if (field == "round")
      round = stoi(value);
    if (field == "field")
      parseState(value);
  }
  if (target == "player0" or target == "player1") {
    if (field == "living_cells") {
      if (target[6] == botId)
        myLiveCells = stoi(value);
      else
        theirLiveCells = stoi(value);
    }
    if (field != "node")
      cerr << "update playerX field: " << field << " not expected\n";
  } else
    cerr << "update target: " << target << " not expected\n";
}

void processSettings()
{
  string field, value;
  token >> field;
  token >> value;

  if (field == "player_names") {
    if (value != "player0,player1")
      cerr << "settings player_names value: " << value << " not expected\n";
  }
  if (field == "your_bot") {
    if (value != "player0" and value != "player1")
      cerr << "settings your_bot value: " << value << " not expected\n";
  }
  if (field == "timebank") {
    if (value == "10000")
      timebank = stoi(value);
    else
      cerr << "settings timebank value: " << value << " not expected\n";
  }
  if (field == "time_per_move") {
    if (value != "100")
      cerr << "settings time_per_move value: " << value << " not expected\n";
  }
  if (field == "field_width") {
    if (value != "18")
      cerr << "settings field_width value: " << value << " not expected\n";
  }
  if (field == "field_height") {
    if (value != "16")
      cerr << "settings field_height value: " << value << " not expected\n";
  }
  if (field == "max_rounds") {
    if (value != "100")
      cerr << "settings max_rounds value: " << value << " not expected\n";
  }
  if (field == "your_botid") {
    if (value == "0" or value == "1")
      botId = value[0];
    else
      cerr << "settings your_botid value: " << value << " not expected\n";
  } else
    cerr << "settings field: " << field << " not expected\n";
}

void parseState(const string value)
{
  int row = 0;
  int col = 0;
  for (const char& c : value) {
    if (c != '.') {
      state[row][col] = c;
      if (col == 17) {
        col = 0;
        row++;
      } else {
        col++;
      }
    }
  }
}

void makeMove()
{
  int numMoves = 1 + (myLiveCells + theirLiveCells) + (6 * (288 - myLiveCells - theirLiveCells));
  node nodes[numMoves];
  addPassNodes(nodes);
  addKillNodes(nodes);
  int bestKillMoveIdxs[4];
  findBestKillNodes(nodes, bestKillMoveIdxs);
  addBirthNodes(nodes, bestKillMoveIdxs);
  // TODO: find best move, make move, api
}

void addPassNodes(node nodes[])
{
  node n;
  n.type = 'p';
  copyState(n.state);
  calculateNextState(n);
  calculateHeuristic(n);
  nodes[0] = n;
}

void addKillNodes(node nodes[])
{
  int i = 0;
  for (int c = 0; c < 19; c++) {
    for (int r = 0; r < 17; r++) {
      if (state[r][c] != '.') {
        node n;
        n.type = 'k';
        copyState(n.state);
        n.state[r][c] = '.';
        calculateNextState(n);
        calculateHeuristic(n);
        nodes[++i] = n;
      }
    }
  }
}

void findBestKillNodes(const node nodes[], int bestKillMoves[])
{
  int bestNode1[2];
  bestNode1[0] = 0;
  bestNode1[1] = 0;
  int bestNode2[2];
  bestNode2[0] = 0;
  bestNode2[1] = 0;
  int bestNode3[2];
  bestNode3[0] = 0;
  bestNode3[1] = 0;
  int bestNode4[2];
  bestNode4[0] = 0;
  bestNode4[1] = 0;

  for (int i = 0; i < 288; i++) {
    node n  = nodes[i];
    if (n.type == 'k' and n.heuristicValue > bestNode4[0]) {
      if (n.heuristicValue > bestNode3[0]) {
        bestNode4[0] = bestNode3[0];
        bestNode4[1] = bestNode3[1];
        if (n.heuristicValue > bestNode2[0]) {
        bestNode3[0] = bestNode2[0];
        bestNode3[1] = bestNode2[1];
          if (n.heuristicValue > bestNode1[0]) {
            bestNode2[0] = bestNode1[0];
            bestNode2[1] = bestNode1[1];
            bestNode1[0] = n.heuristicValue;
            bestNode1[1] = i;
          } else {
            bestNode2[0] = n.heuristicValue;
            bestNode2[1] = i;
          }
        } else {
          bestNode3[0] = n.heuristicValue;
          bestNode3[1] = i;
        }
      } else {
        bestNode4[0] = n.heuristicValue;
        bestNode4[1] = i;
      }
    }
  }
}

void addBirthNodes(node nodes[], const int bestKillMoves[])
{
}

void copyState(char target[][18])
{
  for (int c = 0; c < 19; c++) {
    for (int r = 0; r < 17; r++) {
      target[r][c] = state[r][c];
    }
  }
}

void calculateNextState(node n)
{
  int neighbours0[16][18];
  int neighbours1[16][18];

  for (int c = 0; c < 19; c++) {
    for (int r = 0; r < 17; r++) {
      if (n.state[r][c] == '0') {
        if (c > 0) {
          neighbours0[r][c - 1]++;
          if (r > 0)
            neighbours0[r - 1][c - 1]++;
          if (r < 15)
            neighbours0[r + 1][c - 1]++;
        }
        if (c < 17) {
          neighbours0[r][c + 1]++;
          if (r > 0)
            neighbours0[r - 1][c + 1]++;
          if (r < 15)
            neighbours0[r + 1][c + 1]++;
        }
        if (r > 0)
          neighbours0[r - 1][c]++;
        if (r < 15)
          neighbours0[r + 1][c]++;
      }
      if (n.state[r][c] == '1') {
        if (c > 0) {
          neighbours1[r][c - 1]++;
          if (r > 0)
            neighbours1[r - 1][c - 1]++;
          if (r < 15)
            neighbours1[r + 1][c - 1]++;
        }
        if (c < 17) {
          neighbours1[r][c + 1]++;
          if (r > 0)
            neighbours1[r - 1][c + 1]++;
          if (r < 15)
            neighbours1[r + 1][c + 1]++;
        }
        if (r > 0)
          neighbours1[r - 1][c]++;
        if (r < 15)
          neighbours1[r + 1][c]++;
      }
    }
  }

  int neighbours;
  for (int c = 0; c < 19; c++) {
    for (int r = 0; r < 17; r++) {
      neighbours = neighbours0[r][c] + neighbours1[r][c];
      if (n.state[r][c] == '.' and neighbours == 3) {
        if (neighbours0[r][c] > neighbours1[r][c])
          n.state[r][c] = '0';
        else
          n.state[r][c] = '1';
      } else if (n.state[r][c] != '.' and (neighbours == 2 or neighbours == 3))
        n.state[r][c] = '.';
    }
  }
}

void calculateHeuristic(node n)
{
  int cellCount0 = 0;
  int cellCount1 = 0;

  for (int c = 0; c < 19; c++) {
    for (int r = 0; r < 17; r++) {
      if (n.state[r][c] == '0')
        cellCount0++;
      if (n.state[r][c] == '1')
        cellCount1++;
    }
  }

  if (botId == '0')
    n.heuristicValue = cellCount0 - cellCount1;
  if (botId == '1')
    n.heuristicValue = cellCount1 - cellCount0;
}
