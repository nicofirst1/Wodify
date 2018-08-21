import sys
import time


def slowprint(msg, delay ):
  for c in msg + '\n':
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(delay)


def slowprint_with_input(msg, delay ):
    slowprint(msg, delay)
    return input()