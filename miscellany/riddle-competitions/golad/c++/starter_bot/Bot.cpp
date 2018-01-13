#include "Bot.h"
using namespace std;

Bot::Bot()
{
  this->board = NULL;
}

void Bot::Kill(Coordinate target)
{
  cout << "kill " << target.toString() << "\n";
}

void Bot::Birth(Coordinate target, Coordinate sacrifice1, Coordinate sacrifice2)
{
  cout << "birth " << target.toString() << " " << sacrifice1.toString() << " " << sacrifice2.toString() << "\n";
}

template <class T>
T Bot::RandomElementFromVector(vector<T>* input)
{
  random_shuffle(input->begin(), input->end());
  T temp = input->back();
  input->pop_back();
  return temp;
}

void Bot::Move(int time)
{
  // vector<string> availableMoveTypes = this->GetAvailableMoveTypes();
  // random_shuffle(availableMoveTypes.begin(), availableMoveTypes.end());
  // string moveType = availableMoveTypes.back();
  string moveType = RandomElementFromVector(this->GetAvailableMoveTypes());

  if (moveType == "birth") {
    // Get all dead cells
    vector<Coordinate>* deadCells = this->board->GetCells('.');
    vector<Coordinate>* myCells = this->board->GetCells(to_string(playerId).at(0));

    if (deadCells->size() == 0 || myCells->size() < 2) {
      cout << "pass\n";
      return;
    }

    // randomly choose a target dead cell and two of my own cells to sacrifice
    Coordinate target = RandomElementFromVector(deadCells);
    Coordinate sacrifice1 = RandomElementFromVector(myCells);
    Coordinate sacrifice2 = RandomElementFromVector(myCells);

    Birth(target, sacrifice1, sacrifice2);
    return;
  }

  if (moveType == "kill") {
    vector<Coordinate>* enemyCells = this->board->GetCells(to_string(playerId+1%2).at(0));
    Coordinate target = RandomElementFromVector(enemyCells);
    Kill(target);
    return;
  }

  cout << "pass\n";
}

void Bot::SetRound(int time){};

Board* Bot::GetBoard()
{
  return this->board;
}

void Bot::SetBoard(Board *board)
{
  this->board = board;
}

void Bot::SetTimebank(int time){};

void Bot::SetTimePerMove(int time){};

void Bot::SetYourBotName(string name)
{
  this->playerName = name;
}

string Bot::GetYourBotName()
{
  return this->playerName;
}

void Bot::SetYourBotId(Player playerId)
{
  this->playerId = playerId;
}

void Bot::SetFieldWidth(int width)
{
  this->width = width;
}

void Bot::SetFieldHeight(int height)
{
  this->height = height;
}

int Bot::GetFieldWidth()
{
  return this->width;
}

int Bot::GetFieldHeight()
{
  return this->height;
}

void Bot::SetPlayerNames(string player1, string player2){};

void Bot::SetMaxRounds(int maxRounds)
{
  this->maxRounds = maxRounds;
}

int Bot::GetMaxRounds()
{
  return this->maxRounds;
}

void Bot::SetMyLivingCellCount(int livingCellCount)
{
  this->myLivingCellCount = livingCellCount;
}

int Bot::GetMyLivingCellCount()
{
  return this->myLivingCellCount;
}

void Bot::SetEnemyLivingCellCount(int livingCellCount)
{
  this->enemyLivingCellCount = livingCellCount;
}

int Bot::GetEnemyLivingCellCount()
{
  return this->enemyLivingCellCount;
}

vector<string>* Bot::GetAvailableMoveTypes()
{
  vector<string>* availableMoves = new vector<string>;

  if (this->GetMyLivingCellCount() + this->GetEnemyLivingCellCount() > 0) {
    availableMoves->push_back("kill");
  }

  if (this->GetMyLivingCellCount() > 1) {
    availableMoves->push_back("birth");
  }

  return availableMoves;
}