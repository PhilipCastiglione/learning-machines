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
    if (field == "round") {
      round = stoi(value);
    }
    if (field == "field") {
      parseState(value);
    }
  } else if (target == "player0" or target == "player1") {
    if (field == "living_cells") {
      if (target[6] == botId)
        myLiveCells = stoi(value);
      else
        theirLiveCells = stoi(value);
    } else if (field != "move")
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
  } else if (field == "your_bot") {
    if (value != "player0" and value != "player1")
      cerr << "settings your_bot value: " << value << " not expected\n";
  } else if (field == "timebank") {
    if (value == "10000")
      timebank = stoi(value);
    else
      cerr << "settings timebank value: " << value << " not expected\n";
  } else if (field == "time_per_move") {
    if (value != "100")
      cerr << "settings time_per_move value: " << value << " not expected\n";
  } else if (field == "field_width") {
    if (value != "18")
      cerr << "settings field_width value: " << value << " not expected\n";
  } else if (field == "field_height") {
    if (value != "16")
      cerr << "settings field_height value: " << value << " not expected\n";
  } else if (field == "max_rounds") {
    if (value != "100")
      cerr << "settings max_rounds value: " << value << " not expected\n";
  } else if (field == "your_botid") {
    if (value == "0" or value == "1")
      botId = value[0];
    else
      cerr << "settings your_botid value: " << value << " not expected\n";
  } else
    cerr << "settings field: " << field << " not expected\n";
}

void parseState(const string &value)
{
  int row = 0;
  int col = 0;
  for (const char& c : value) {
    if (c != ',') {
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
  node bestKillNodes[4];
  node nodes[numMoves];

  addPassNodes(nodes);
  addKillNodes(nodes);
  findBestKillNodes(nodes, bestKillNodes);
  addBirthNodes(nodes, bestKillNodes);

  node bestNode = findBestNode(nodes, numMoves);
  sendMove(bestNode);
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
  for (int c = 0; c < 18; c++) {
    for (int r = 0; r < 16; r++) {
      if (state[r][c] != '.') {
        node n;
        n.value = state[r][c];
        n.type = 'k';
        n.target = r * 18 + c;
        copyState(n.state);
        n.state[r][c] = '.';
        calculateNextState(n);
        calculateHeuristic(n);
        nodes[++i] = n;
      }
    }
  }
}

void findBestKillNodes(const node nodes[], node bestKillNodes[])
{
  node dummyNode;
  dummyNode.heuristicValue = -289;

  node bestNode1 = dummyNode;
  node bestNode2 = dummyNode;
  node bestNode3 = dummyNode;
  node bestNode4 = dummyNode;

  for (int i = 1; i < (1 + myLiveCells + theirLiveCells); i++) {
    node n = nodes[i];
    if (n.value == botId and n.heuristicValue > bestNode4.heuristicValue) {
      if (n.heuristicValue > bestNode3.heuristicValue) {
        bestNode4 = bestNode3;
        if (n.heuristicValue > bestNode2.heuristicValue) {
        bestNode3 = bestNode2;
          if (n.heuristicValue > bestNode1.heuristicValue) {
            bestNode2 = bestNode1;
            bestNode1 = n;
          } else {
            bestNode2 = n;
          }
        } else {
          bestNode3 = n;
        }
      } else {
        bestNode4 = n;
      }
    }
  }

  bestKillNodes[0] = bestNode1;
  bestKillNodes[1] = bestNode2;
  bestKillNodes[2] = bestNode3;
  bestKillNodes[3] = bestNode4;
}

void addBirthNodes(node nodes[], const node bestKillNodes[])
{
  int i = myLiveCells + theirLiveCells;
  for (int x = 0; x < 3; x++) {
    for (int y = x + 1; y < 4; y++) {
      for (int c = 0; c < 18; c++) {
        for (int r = 0; r < 16; r++) {
          if (state[r][c] == '.') {
            node n;
            n.type = 'b';
            n.target = r * 18 + c;
            n.sacrifice1 = bestKillNodes[x].target;
            n.sacrifice2 = bestKillNodes[y].target;
            copyState(n.state);
            n.state[r][c] = botId;
            n.state[n.sacrifice1 / 18][n.sacrifice1 % 18] = '.';
            n.state[n.sacrifice2 / 18][n.sacrifice2 % 18] = '.';
            calculateNextState(n);
            calculateHeuristic(n);
            nodes[++i] = n;
          }
        }
      }
    }
  }
}

node findBestNode(const node nodes[], int nodeCount)
{
  int topHeuristic = 0;
  int topHeuristicIdx = 0;
  for (int i = 0; i < nodeCount; i++) {
    if (nodes[i].heuristicValue > topHeuristic) {
      topHeuristic = nodes[topHeuristicIdx].heuristicValue;
      topHeuristicIdx = i;
    }
  }

  return nodes[topHeuristicIdx];
}

void sendMove(const node &n)
{
  if (n.type == 'p') {
    cout << "pass\n";
  } else if (n.type == 'k') {
    cout << "kill " << coords(n.target) << "\n";
  } else if (n.type == 'b') {
    cout << "birth " << coords(n.target) << " " << coords(n.sacrifice1) << " " << coords(n.sacrifice2) << "\n";
  }
}

string coords(int cellIdx)
{
  stringstream ss;
  ss << (cellIdx % 18) << "," << cellIdx / 18;
  return ss.str();
}

void copyState(char target[][18])
{
  for (int c = 0; c < 18; c++) {
    for (int r = 0; r < 16; r++) {
      target[r][c] = state[r][c];
    }
  }
}

void calculateNextState(node &n)
{
  int neighbours0[16][18];
  int neighbours1[16][18];

  for (int c = 0; c < 18; c++) {
    for (int r = 0; r < 16; r++) {
      neighbours0[r][c] = 0;
      neighbours1[r][c] = 0;
    }
  }

  for (int c = 0; c < 18; c++) {
    for (int r = 0; r < 16; r++) {
      if (n.state[r][c] == '0') {
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
      if (n.state[r][c] == '1') {
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
  for (int c = 0; c < 18; c++) {
    for (int r = 0; r < 16; r++) {
      neighbours = neighbours0[r][c] + neighbours1[r][c];
      if (n.state[r][c] == '.' and neighbours == 3) {
        n.state[r][c] = (neighbours0[r][c] > neighbours1[r][c]) ?  '0' : '1';
      } else if (n.state[r][c] != '.' and (neighbours < 2 or neighbours > 3)) {
        n.state[r][c] = '.';
      }
    }
  }
}

void calculateHeuristic(node &n)
{
  int cellCount0 = 0;
  int cellCount1 = 0;

  for (int c = 0; c < 18; c++) {
    for (int r = 0; r < 16; r++) {
      if (n.state[r][c] == '0') {
        cellCount0++;
      } else if (n.state[r][c] == '1') {
        cellCount1++;
      }
    }
  }

  if (botId == '0') {
    if (cellCount0 == 0) {
      n.heuristicValue = -288;
    } else if (cellCount1 == 0) {
      n.heuristicValue = 288;
    } else {
      n.heuristicValue = cellCount0 - cellCount1;
    }
  } else if (botId == '1') {
    if (cellCount1 == 0) {
      n.heuristicValue = -288;
    } else if (cellCount0 == 0) {
      n.heuristicValue = 288;
    } else {
      n.heuristicValue = cellCount1 - cellCount0;
    }
  }
}

/* DEBUG FUNCTIONS */
void setBotId(const char id)
{
  botId = id;
}
