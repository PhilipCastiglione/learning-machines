#include "game.h"

using namespace std;

stringstream token;

void game()
{
  string line, command;

  while (getline(cin, line))
  {
    cout << line << "\n"; // DEBUG

    token.clear();
    token.str(line);
    token >> command;

    cout << command << "\n"; // DEBUG

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
  string derp;
  token >> derp;
  cout << derp << "\n"; // DEBUG
}

void processUpdate()
{
  string derp;
  token >> derp;
  cout << derp << "\n"; // DEBUG
}

void processSettings()
{
  string derp;
  token >> derp;
  cout << derp << "\n"; // DEBUG
}

