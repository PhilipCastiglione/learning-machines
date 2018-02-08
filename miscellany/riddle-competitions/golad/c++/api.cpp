#include "api.h"

using namespace std;

/* FORWARD DECLARATIONS */
void _processAction(stringstream &tokens, game &g, function<void (game &g)> act);
void _processUpdate(stringstream &tokens, game &g);
void _parseState(game &g, const string &value);
void _processSettings(stringstream &tokens, game &g);
string _coords(int cellIdx);

/* PUBLIC FUNCTIONS */
void listenForInput(game &g, function<void (game &g)> act)
{
  stringstream tokens;
  string line, command;

  while (getline(cin, line)) {
    tokens.clear();
    tokens.str(line);
    tokens >> command;

    if (command == "action")
      _processAction(tokens, g, act);
    if (command == "update")
      _processUpdate(tokens, g);
    if (command == "settings")
      _processSettings(tokens, g);
  }
}

void sendMove(const gameMove &m)
{
  if (m.type == 'p') {
    cout << "pass\n";
  } else if (m.type == 'k') {
    cout << "kill " << _coords(m.targetIdx) << "\n";
  } else if (m.type == 'b') {
    cout << "birth " << _coords(m.targetIdx) << " " << _coords(m.sac1Idx) << " " << _coords(m.sac2Idx) << "\n";
  }
}

/* PRIVATE FUNCTIONS */
void _processAction(stringstream &tokens, game &g, function<void (game &g)> act)
{
  string type, time;
  tokens >> type;
  tokens >> time;

  if (type == "move") {
    auto t = chrono::steady_clock::now();

    g.timebank = stoi(time);

    act(g);

    chrono::duration<double> diff = chrono::steady_clock::now() - t;
    cerr << diff.count() * 1000 << "ms used\n";
  } else
    cerr << "action type: " << type << " not expected\n";
}

void _processUpdate(stringstream &tokens, game &g)
{
  string target, field, value;
  tokens >> target;
  tokens >> field;
  tokens >> value;

  if (target == "game") {
    if (field == "round") {
      g.roundNum = stoi(value);
    } else if (field == "field") {
      _parseState(g, value);
    }
  } else if (target == "player0" or target == "player1") {
    if (field == "living_cells") {
      if (target[6] == g.myId) {
        g.myCellCount = stoi(value);
      } else {
        g.yourCellCount = stoi(value);
      }
    } else if (field != "move") {
      cerr << "update " << target << " field: " << field << " not expected\n";
    }
  } else {
    cerr << "update target: " << target << " not expected\n";
  }
}

void _parseState(game &g, const string &value)
{
  int i = 0;
  for (const char& c : value) {
    if (c != ',')
      g.b.state[i++] = c;
  }
}

void _processSettings(stringstream &tokens, game &g)
{
  string field, value;
  tokens >> field;
  tokens >> value;

  if (field == "player_names") {
    if (value != "player0,player1")
      cerr << "settings player_names value: " << value << " not expected\n";
  } else if (field == "your_bot") {
    if (value != "player0" and value != "player1")
      cerr << "settings your_bot value: " << value << " not expected\n";
  } else if (field == "timebank") {
    if (value == "10000") {
      g.timebank = stoi(value);
    } else {
      cerr << "settings timebank value: " << value << " not expected\n";
    }
  } else if (field == "time_per_move") {
    if (value != "100")
      cerr << "settings time_per_move value: " << value << " not expected\n";
  } else if (field == "field_width") {
    if (stoi(value) != COLS)
      cerr << "settings field_width value: " << value << " not expected\n";
  } else if (field == "field_height") {
    if (stoi(value) != ROWS)
      cerr << "settings field_height value: " << value << " not expected\n";
  } else if (field == "max_rounds") {
    if (value != "100")
      cerr << "settings max_rounds value: " << value << " not expected\n";
  } else if (field == "your_botid") {
    if (value == "0") {
      g.myId = '0';
      g.yourId = '1';
    } else if (value == "1") {
      g.myId = '1';
      g.yourId = '0';
    } else {
      cerr << "settings your_botid value: " << value << " not expected\n";
    }
  } else {
    cerr << "settings field: " << field << " not expected\n";
  }
}

string _coords(int cellIdx)
{
  stringstream ss;
  ss << (cellIdx % COLS) << "," << cellIdx / COLS;
  return ss.str();
}
