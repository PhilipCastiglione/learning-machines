#include <cstdint>
#include <sys/time.h>
#include "Parser.h"
#include "Bot.h"

int main()
{
  // Initialize random number generator
  struct timeval time;
  gettimeofday(&time, NULL);
  srand((time.tv_sec * 1000) + (time.tv_usec / 1000));

  Bot bot;
  Parser parser(bot);
  parser.Parse();
  return 0;
}
