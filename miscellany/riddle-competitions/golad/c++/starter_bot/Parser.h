#ifndef PARSER_h
#define PARSER_h

#include <cstdint>
#include <iostream>
#include <sstream>
#include "Bot.h"
#include "Enums.h"
using namespace std;

class Parser
{
public:
  Parser(Bot &bot);
  void Parse();

private:
  Bot bot;
  int width = 0;
  int height = 0;
  void ProcessCommand();
  void ProcessAction();
  void ProcessUpdate();
  void ProcessSettings();
  string NextCmd();
  stringstream cmdLine;
};

#endif
