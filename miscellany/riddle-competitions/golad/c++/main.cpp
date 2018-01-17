// TODO: author, licence, README
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
