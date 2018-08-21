import random
import threading
import time

from utils import time_print, play_sound, other_todo


class Job(threading.Thread):

    def __init__(self, name, freq, rep, stop):
        super().__init__()
        self.name = name
        self.freq = self.get_number(freq)
        self.rep = self.get_number(rep)
        self.stop = stop

        self.start_time = time.time()

        self.total = 0

    def progress(self):
        to_print = f"You did {self.total} {self.name} in {time_print(time.time()-self.start_time)}"
        return to_print



    def change_vals(self, name, freq, rep):
        if name:
            self.name = name

        if freq:
            self.freq = self.get_number(freq)

        if rep:
            self.rep = self.get_number(rep)

    def get_number(self, string):
        try:
            l, u = string.split(",")
            l = int(l)
            u = int(u)
        except Exception as e:
            print(e)
            l = -1
            u = -1
        return (l, u)

    def run(self):

        print(f"Starting {self.name}\n")

        while not self.stop.is_set():

            random_wait = random.randint(self.freq[0], self.freq[1]) * 60
            while not self.stop.wait(timeout=random_wait):
                random_rep = random.randint(self.rep[0], self.rep[1])
                print(other_todo(random_rep,self.name))
                play_sound()
                self.total += random_rep
                break

        print(f"{self.summary()}\nStopped\n\n")

    def summary(self):
        to_print = f"Exercise : {self.name}\nFrequency : {self.freq}\nRepetitions : {self.rep}"
        return to_print
