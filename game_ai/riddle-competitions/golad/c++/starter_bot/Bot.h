#ifndef BOT_h
#define BOT_h

#include <iostream>
#include <stdio.h>
#include <vector>
#include <algorithm>
#include "Board.h"
#include "Enums.h"
#include "Coordinate.h"

using namespace std;

class Bot
{
private:
  Player playerId;
  int width, height;
  int maxRounds;
  Board *board;
  int myLivingCellCount, enemyLivingCellCount;
  string playerName;

protected:

public:
  Bot();

  // Action
  virtual void Kill(Coordinate target);
  virtual void Birth(Coordinate target, Coordinate sacrifice1, Coordinate sacrifice2);
  virtual void Move(int time);

  // Update
  virtual void SetRound(int time);
  virtual Board* GetBoard();
  virtual void SetBoard(Board *board);

  // Settings
  virtual void SetTimebank(int time);
  virtual void SetTimePerMove(int time);

  virtual void SetYourBotName(string name);
  virtual string GetYourBotName();

  virtual void SetYourBotId(Player playerId);

  virtual int GetFieldWidth();
  virtual void SetFieldWidth(int width);

  virtual int GetFieldHeight();
  virtual void SetFieldHeight(int height);

  virtual void SetPlayerNames(string player1, string player2);

  virtual int GetMaxRounds();
  virtual void SetMaxRounds(int maxRounds);

  virtual void SetMyLivingCellCount(int livingCellCount);
  virtual int GetMyLivingCellCount();

  virtual void SetEnemyLivingCellCount(int livingCellCount);
  virtual int GetEnemyLivingCellCount();

  virtual vector<string>* GetAvailableMoveTypes();

  template <class T>
  T RandomElementFromVector(vector<T>* input);
};

#endif
