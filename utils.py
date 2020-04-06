import datetime
import json
import os
import pickle
import random
import sys
import time

from Parameters import Parameters
from Path import Paths

parameters = Parameters
Path_class = Paths()



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


def ubuntu_beep():
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


def windows_beep():
    import winsound
    frequency = parameters.beep_frequency  # Set Frequency To 2500 Hertz
    duration = parameters.beep_duration * 1000  # Set Duration To 1000 ms == 1 second
    repeat = parameters.beep_repetitions

    for i in range(repeat):
        winsound.Beep(frequency, duration)


def other_todo(how_many, what):
    todo_list = [
        "Come on fatty! Another %d %s to do!",
        "More coming! %d %s",
        "Let's try with %d %s",
        "Tired yet? Go on with %d %s",
        "You're never too tired for %d %s"
    ]

    str = random.choice(todo_list) % (how_many, what)
    return str


def dump_json_job(job):
    file_path = os.path.join(Path_class.saved_jobs, job['name'].replace(" ", "_")) + ".json"

    with open(file_path, "w") as file:
        json.dump(job, file)

def dump_json_group(job):
    file_path = os.path.join(Path_class.saved_groups, job['name'].replace(" ", "_")) + ".json"

    with open(file_path, "w") as file:
        json.dump(job, file)


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def dump_pkl(job):
    file_path = os.path.join(Path_class.saved_jobs, job['name']) + ".pkl"

    with open(file_path, "wb") as file:
        pickle.dump(job, file, pickle.HIGHEST_PROTOCOL)


def load_pkl(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)


def count_how_may(job_list):
    jobs = [elem[0] for elem in job_list]
    jobs = set(jobs)

    res_dict = {}

    for j in jobs:
        quantity = sum([int(elem[1].strip("\n")) for elem in job_list if elem[0] == j])
        res_dict[j] = quantity

    return res_dict
