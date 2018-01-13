#include "game.h"

using namespace std;

stringstream token;
char botId;
string state;
int round, timebank;


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
    else if (command == "update")
      processUpdate();
    else if (command == "settings")
      processSettings();
  }
}

void processAction()
{
  string type, time;
  token >> type;
  token >> time;

  if (type == "move")
  {
    timebank = stoi(time);

    cout << "pass" << "\n"; // TODO: this is a suboptimal strategy
  }
  else
    cerr << "action type: " << type << " not expected\n";
}

void processUpdate()
{
  string target, value;
  token >> target;
  token >> value;

  if (target == "round")
    round = stoi(value);
  else if (target == "field")
    state = value; // TODO: parse the state before assigning
  else
    cerr << "update target: " << target << " not expected\n";
}

void processSettings()
{
  string field, value;
  token >> field;
  token >> value;

  if (field == "player_names")
  {
    if (value != "player0,player1")
      cerr << "settings player_names value: " << value << " not expected\n";
  }
  else if (field == "your_bot")
  {
    if (value != "player0" and value != "player1")
      cerr << "settings your_bot value: " << value << " not expected\n";
  }
  else if (field == "timebank")
  {
    if (value == "10000")
      timebank = stoi(value);
    else
      cerr << "settings timebank value: " << value << " not expected\n";
  }
  else if (field == "time_per_move")
  {
    if (value != "100")
      cerr << "settings time_per_move value: " << value << " not expected\n";
  }
  else if (field == "field_width")
  {
    if (value != "18")
      cerr << "settings field_width value: " << value << " not expected\n";
  }
  else if (field == "field_height")
  {
    if (value != "16")
      cerr << "settings field_height value: " << value << " not expected\n";
  }
  else if (field == "max_rounds")
  {
    if (value != "100")
      cerr << "settings max_rounds value: " << value << " not expected\n";
  }
  else if (field == "your_botid")
  {
    if (value == "0" or value == "1")
      botId = value[0];
    else
      cerr << "settings your_botid value: " << value << " not expected\n";
  }
  else
    cerr << "settings field: " << field << " not expected\n";
}
