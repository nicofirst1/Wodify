import datetime
import os
import random
import sys
import time
import pickle
from Parameters import Parameters, Paths

parameters = Parameters()
paths=Paths()

def slowprint(msg, delay):
    for c in msg + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)


def slowprint_with_input(msg, delay):
    slowprint("\n" + msg, delay)
    return input("> ")


def slowprint_with_delay(msg, print_delay, final_delay):
    slowprint(msg, print_delay)
    time.sleep(final_delay)


def time_print(time_in_seconds):
    return str(datetime.timedelta(seconds=time_in_seconds))


def slow_print_input_ingore_enter(msg, delay):
    slowprint(msg, delay)
    res = input("> ")
    while res == "":
        res = input()
    return res




def play_sound():
    """
    Play a sound
    :param duration: duration in seconds
    :param freq: frequence of the sound
    :return:
    """
    duration = parameters.beep_duration
    freq = parameters.beep_frequency
    repeat = parameters.beep_repetitions

    for i in range(repeat):
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))


def other_todo(how_many, what):

    todo_list=[
        "Come on fatty! Another %d %s to do!",
        "More coming! %d %s",
        "Let's try with %d %s",
        "Tired yet? Go on with %d %s",
        "You're never to tired for %d %s"
    ]

    str=random.choice(todo_list)%(how_many,what)
    return str



def dump_pkl(job):

    file_path=os.path.join(paths.saved_jobs,job['name'])+".pkl"

    with open(file_path,"wb") as file:
        pickle.dump(job, file,pickle.HIGHEST_PROTOCOL)


def load_pkl(file_path):

    with open(file_path,"rb") as file:
        return pickle.load(file)