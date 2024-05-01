#include "Parser.h"
using namespace std;

Parser::Parser(Bot &bot) : bot(bot)
{
}

string Parser::NextCmd()
{
  string k;
  // getline(cmdLine, k, ' ');
  cmdLine >> k;
  return k;
}

void Parser::Parse()
{
  string line;
  while (getline(cin, line))
  {
    cmdLine.clear();
    cmdLine.str(line);
    // Process command
    string cmd = NextCmd();
    if (cmd == "action")
      ProcessAction();
    else if (cmd == "update")
      ProcessUpdate();
    else if (cmd == "settings")
      ProcessSettings();
  }
}

void Parser::ProcessAction()
{
  string cmd = NextCmd();
  if (cmd == "move")
    bot.Move(stoi(NextCmd()));
}

void Parser::ProcessUpdate()
{
  string updateType = NextCmd();
  if (updateType == "game")
  {
    string cmd = NextCmd();
    if (cmd == "round")
    {
      bot.SetRound(stoi(NextCmd()));
    }
    else if (cmd == "field")
    {
      if (bot.GetBoard() == NULL) {
        bot.SetBoard(new Board(bot.GetFieldWidth(), bot.GetFieldHeight()));
      }
      stringstream stream(NextCmd());
      bot.GetBoard()->UpdateBoard(stream);
    }
  } else {
    // updateType is a player_name
    string playerName = updateType;
    string cmd = NextCmd();
    if (cmd == "living_cells")
    {
      int livingCellCount = stoi(NextCmd());
      if (bot.GetYourBotName() == playerName)
      {
        bot.SetMyLivingCellCount(livingCellCount);
      } else {
        bot.SetEnemyLivingCellCount(livingCellCount);
      }
    }
  }
}

void Parser::ProcessSettings()
{
  string cmd = NextCmd();
  if (cmd == "timebank")
    bot.SetTimebank(stoi(NextCmd()));
  else if (cmd == "time_per_move")
    bot.SetTimePerMove(stoi(NextCmd()));
  else if (cmd == "player_names")
  {
    stringstream args(NextCmd());
    string player1, player2;
    getline(args, player1, ',');
    getline(args, player2, ',');
    bot.SetPlayerNames(player1, player1);
  }
  else if (cmd == "your_bot")
    bot.SetYourBotName(NextCmd());
  else if (cmd == "your_botid")
  {
    int id = stoi(NextCmd());
    bot.SetYourBotId((id == 0) ? P0 : P1);
  }
  else if (cmd == "field_width")
  {
    width = stoi(NextCmd());
    bot.SetFieldWidth(width);
  }
  else if (cmd == "field_height")
  {
    height = stoi(NextCmd());
    bot.SetFieldHeight(height);
  }
  else if (cmd == "max_rounds")
  {
    bot.SetMaxRounds(stoi(NextCmd()));
  }
}
