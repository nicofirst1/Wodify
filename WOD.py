import os
import queue
import random
import threading
import re
import time

from Job import Job
from utils import slowprint, slowprint_with_input, slowprint_with_delay



format_re = re.compile("\d+,\d+")


class WOD(threading.Thread):

    def __init__(self):

        super().__init__()
        self.worker_classes=[]
        self.print_delay=0.02
        self.final_delay=0.8

        self.cmd_actions = {
            'add': self.add,'show':self.show_all,
            'change':self.change, 'stop all':self.stop_all,
            'stop':self.stop_specific, 'h':self.help,
            'help':self.help, 'progress': self.progress}

        self.stop=False
        self.lock= threading.Lock()
        self.queue = queue.Queue()


    def delayed_print(self, msg, print_delay=0, final_delay=0):

        if not final_delay:
            final_delay=self.final_delay
        if not print_delay:
            print_delay=self.print_delay

        slowprint_with_delay(msg,print_delay,final_delay)

    def console(self):
        while 1:
            input()  # Afther pressing Enter you'll be in "input mode"
            with self.lock:
                cmd = input('> ')

            self.queue.put(cmd)
            if cmd == 'quit':
                self.delayed_print("bie bie")
                break

    def show_all(self):
        """Show all jobs (running or not)"""
        with self.lock:
            if len(self.worker_classes)==0:
                self.delayed_print("No job currently running")
            for idx in range(len(self.worker_classes)):
                self.delayed_print(f"Id : {idx}\n{self.worker_classes[idx]['ex'].summary()}\n")


    def check_formatting(self, str):

        if re.fullmatch(format_re, str) is None:
            self.delayed_print("Invalid formatting dumbass")
            return False

        return True

    def add(self):
        """Add a job"""
        with self.lock:

            input("Press enter to continue")
            name = slowprint_with_input("What's the name of the exercise?", self.print_delay)
            frequency = slowprint_with_input("With what time frequency? (min,max)", self.print_delay)
            if not self.check_formatting(frequency):return
            rep = slowprint_with_input('How many repetitions? (min,max)', self.print_delay)
            if not self.check_formatting(rep):return

            good=slowprint_with_input(f"Is this good?\nname: {name}\nfrequency: {frequency}\nrepetitions: {rep}", self.print_delay)


            if "n" in good.lower() or "no" in good.lower():
                self.delayed_print("Too bad...")
                return

            stop=threading.Event()
            job=Job(name, frequency, rep, stop)
            job.start()
            self.worker_classes.append({"job":job,"stop":stop})

    def stop_all(self):
        """Stop every running job """

        for dict in self.worker_classes:
            stop=dict['stop']
            stop.set()


    def stop_specific(self):
        """Stop a given job"""
        with self.lock:

            self.show_all()
            idx=slowprint_with_input("Which id do you want to stop? (-1) for none", self.print_delay)

            try:
                idx=int(idx)
                if idx==-1:
                    return

                self.worker_classes[idx]['stop'].set()
                self.worker_classes[idx]['job'].start()
            except IndexError or ValueError as e:
                self.delayed_print(f"You just caused an error...\n{e}")



    def change(self):
        """Change the parameters of a specific job """

        with self.lock:

            self.show_all()
            idx=slowprint_with_input("Which id do you want to change? (-1) for none", self.print_delay)
            idx=int(idx)
            if idx==-1:
                return

            job=self.worker_classes[idx]
            name=slowprint_with_input("Enter new name (empty unchanged)", self.print_delay)
            frequency=slowprint_with_input("Enter new frequency (empty unchanged)", self.print_delay)
            rep=slowprint_with_input("Enter new repetitions (empty unchanged)", self.print_delay)

            job.change_vals(name,frequency,rep)
            print("New values changed")

        # other actions

    def invalid_input(self):
        with self.lock:
            to_print="Unknown command\n" \
                     "Type 'h' for help"
            slowprint(to_print, self.print_delay)

    def help(self):
        """Print this help screen"""

        with self.lock:
            for k,v in self.cmd_actions.items():
                slowprint(f"-{k} : {v.__doc__}", self.print_delay)

    def progress(self):
        """Print the progress you achieved in time"""

        for dict in self.worker_classes:
            slowprint_with_delay(dict['job'].progress(), self.print_delay, self.final_delay)

    def run(self):

        self.delayed_print("Program started... press 'enter'")

        dj = threading.Thread(target=self.console)
        dj.start()

        while not self.stop:
            cmd = self.queue.get()
            if cmd == 'quit':
                break
            action = self.cmd_actions.get(cmd, self.invalid_input)
            action()


