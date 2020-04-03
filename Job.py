import random
import threading
import time

from utils import time_print, ubuntu_beep, other_todo, paths, parameters, windows_beep


class Job(threading.Thread):

    def __init__(self, name, freq, rep):
        super().__init__()
        self.name = name
        self.freq = self.get_number(freq)
        self.rep = self.get_number(rep)
        self.stop = threading.Event()

        self.start_time = time.time()

        self.total = 0

    def progress(self):
        to_print = f"{self.total} {self.name} in {time_print(time.time() - self.start_time)}"
        return to_print

    def change_vals(self, name, freq, rep):
        if name:
            self.name = name

        if freq:
            self.freq = self.get_number(freq)

        if rep:
            self.rep = self.get_number(rep)

    def get_number(self, obj):

        if isinstance(obj, tuple):
            if isinstance(obj[0], int):
                if isinstance(obj[1], int):
                    return obj

        try:
            l, u = obj.split(",")
            l = int(l)
            u = int(u)
        except Exception as e:
            print(e)
            l = -1
            u = -1
        return (l, u)

    def run(self):

        print(f"Starting {self.name}\n")

        # sleep before actually starting the process
        random_wait = random.randint(0, self.freq[0]) * 60
        time.sleep(random_wait)

        # while the stop timer is not set
        while not self.stop.is_set():

            # define a random wait time
            random_wait = random.randint(self.freq[0], self.freq[1]) * 60

            # wait
            while not self.stop.wait(timeout=random_wait):

                # define random repetitions
                random_rep = random.randint(self.rep[0], self.rep[1])
                # print it
                print(other_todo(random_rep, self.name))

                # beep
                if parameters.OS == "U" or parameters.OS == "M":
                    ubuntu_beep()

                elif parameters.OS == "W":
                    windows_beep()

                else:
                    raise Exception(f"What the fuck is {parameters.OS} OS?")

                # save progress
                paths.save_progress(self.name, random_rep)
                self.total += random_rep
                break

        print(f"{self.summary()}\nStopped\n\n")

    def summary(self):
        to_print = f"Exercise : {self.name}\nFrequency : {self.freq}\nRepetitions : {self.rep}"
        return to_print
