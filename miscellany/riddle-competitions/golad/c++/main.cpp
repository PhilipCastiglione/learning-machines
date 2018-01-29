// TODO: author, licence, README
// TODO: refactor
// TODO: make logging dependent on execution parameter
// TODO: fix bugs
// TODO: decide parameters
// TODO: handle less than n kill targets for sacrifice
// TODO: use time, get smarter
// TODO: test suite
// TODO: improve heuristic
// TODO: use array templates for 2d array
// TODO: refactor multi-dim array to ignore/singledim array for SPEEEEEEEED
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
