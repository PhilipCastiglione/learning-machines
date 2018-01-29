#include "game.h"

#define LOOKAHEAD 4
#define SACRIFICE_OPTIONS 5
#define OPPONENT_MOVES 5

using namespace std;

// globals
int sacrificeCombinations = factorial(SACRIFICE_OPTIONS) / (factorial(SACRIFICE_OPTIONS - 2) * factorial(2));
stringstream token;
char botId;
char state[16][18];
int roundNum, timebank, myLiveCells, theirLiveCells;

// this just for logging time TODO: remove
auto t = chrono::steady_clock::now();

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
    t = chrono::steady_clock::now(); // TODO: remove
    timebank = stoi(time);
    makeMove();
    chrono::duration<double> diff = chrono::steady_clock::now() - t; // TODO: remove
    cerr << diff.count() * 1000 << "ms used\n"; // TODO: remove
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
      roundNum = stoi(value);
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
  int numMoves = 1 + (myLiveCells + theirLiveCells) + (sacrificeCombinations * (288 - myLiveCells - theirLiveCells));

  // TODO: handle less then n of my cells alive for birthing calcs
  node nodes[numMoves];

  addKillNodes(nodes);

  node bestKillNodes[SACRIFICE_OPTIONS];
  findBestKillNodes(nodes, bestKillNodes);

  addPassNode(nodes);

  addBirthNodes(nodes, bestKillNodes);

  // TODO: for the best n nodes, calculate opponent moves and recalculate heuristic, then pick the best of those
  // sort then slice, then 2nd round heuristic, then sort then first
  sort(nodes, nodes + numMoves, nodeCompare);

  // node bestNode = findBestNode(nodes, numMoves);
  node bestNode = nodes[0];

  sendMove(bestNode);
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
        nodes[i++] = n;
      }
    }
  }
}

void findBestKillNodes(node nodes[], node bestKillNodes[])
{
  sort(nodes, nodes + myLiveCells + theirLiveCells, nodeCompare);

  int killNodeCount = 0;
  for (int i = 0; i < myLiveCells + theirLiveCells; i++) {
    node n = nodes[i];

    if (n.value == botId) {
      bestKillNodes[killNodeCount] = n;
      killNodeCount++;

      if (killNodeCount == SACRIFICE_OPTIONS) {
        break;
      }
    }
  }
}

void addPassNode(node nodes[])
{
  node n;
  n.type = 'p';
  copyState(n.state);
  calculateNextState(n);
  calculateHeuristic(n);
  nodes[myLiveCells + theirLiveCells] = n;
}

void addBirthNodes(node nodes[], const node bestKillNodes[])
{
  int i = myLiveCells + theirLiveCells + 1;
  for (int x = 0; x < SACRIFICE_OPTIONS - 1; x++) {
    for (int y = x + 1; y < SACRIFICE_OPTIONS; y++) {
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
            nodes[i++] = n;
          }
        }
      }
    }
  }
}

node findBestNode(const node nodes[], int nodeCount)
{
  int topHeuristic = -288;
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

void calculateNextState(node &n)
{
  for (int l = 0; l < LOOKAHEAD; l++) {
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
}

void calculateHeuristic(node &n)
{
  int cellCount0 = 0;
  int cellCount1 = 0;

  // TODO: consider the number of opponent cells alive to increase aggression when they are low
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

// utility functions
int factorial(int x, int result) {
  return (x == 1) ? result : factorial(x - 1, x * result);
}

string coords(int cellIdx)
{
  stringstream ss;
  ss << (cellIdx % 18) << "," << cellIdx / 18;
  return ss.str();
}

void copyState(const char source[][18], char target[][18])
{
  for (int r = 0; r < 16; r++) {
    for (int c = 0; c < 18; c++) {
      target[r][c] = source[r][c];
    }
  }
}

bool nodeCompare(node lhs, node rhs)
{
  // sort descending
  return lhs.heuristicValue > rhs.heuristicValue;
}

// debug functions
void setBotId(const char id)
{
  botId = id;
}
