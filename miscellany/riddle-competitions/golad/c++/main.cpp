// TODO: author, licence, README
// TODO: handle less than 4 kill targets for sacrifice
// TODO: use time, get smarter
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
