// TODO: author, licence, README
// TODO: handle less than 4 kill targets for sacrifice
// TODO: use time, get smarter
// TODO: define omptisation variables as constants
// TODO: choose best n moves to calculate opponents moves for
// TODO: improve heuristic
#include "test.h"
#include "game.h"

int main(int argc, char *argv[])
{
  if (argc == 1) {
    game();
  } else {
    test();
  }

  return 0;
}
