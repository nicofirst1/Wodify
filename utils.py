import datetime
import os
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



def slow_print_input_ingore_enter(msg,delay):
    slowprint(msg,delay)
    res=input("> ")
    while res=="":
        res=input()
    return res

def play_sound(duration=1, freq=500, repeat=1):
    """
    Play a sound
    :param duration: duration in seconds
    :param freq: frequence of the sound
    :return:
    """

    for i in range(repeat):
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))


