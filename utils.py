import datetime
import sys
import time



def slowprint(msg, delay ):
  for c in msg + '\n':
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(delay)


def slowprint_with_input(msg, delay ):
    slowprint("\n"+msg, delay)
    return input("> ")


def slowprint_with_delay(msg, print_delay, final_delay):
    slowprint(msg,print_delay)
    time.sleep(final_delay)

def time_print(time_in_seconds):
    return str(datetime.timedelta(seconds=time_in_seconds))




