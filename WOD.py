import datetime
import os
import queue
import re
import threading

from Job import Job
from utils import slowprint, slowprint_with_input, slowprint_with_delay, parameters, paths, load_json, \
    count_how_may, dump_json

format_re = re.compile("\d+,\d+")


class WOD(threading.Thread):

    def __init__(self):

        super().__init__()
        self.job_list = []

        self.cmd_actions = {
            'add': self.add, 'show': self.show_all,
            'change': self.change, 'stop': self.stop_specific,
            'h': self.help,
            'help': self.help, 'progress': self.progress,
            'save': self.save_job, 'load': self.load_job, }

        self.stop = False
        self.lock = threading.Lock()
        self.queue = queue.Queue()

    ##############################
    #        MAIN STUFF
    ##############################

    def run(self):

        self.delayed_print("Program started... press 'enter'")

        # dj = threading.Thread(target=self.console)
        # dj.start()

        while not self.stop:
            with self.lock:
                cmd = input('> ')
            if cmd == 'quit':
                break
            action = self.cmd_actions.get(cmd, self.invalid_input)
            action()

    def console(self):
        while 1:
            with self.lock:
                cmd = input('> ')

            self.queue.put(cmd)
            if cmd == 'quit':
                self.delayed_print("bie bie")
                break

    def invalid_input(self):
        with self.lock:
            to_print = "Unknown command\n" \
                       "Type 'h' for help"
            slowprint(to_print, parameters.print_delay)

    ##############################
    #           UTILS
    ##############################
    def delayed_print(self, msg, print_delay=0, final_delay=0):

        if not final_delay:
            final_delay = parameters.print_delay_sentence
        if not print_delay:
            print_delay = parameters.print_delay

        slowprint_with_delay(msg, print_delay, final_delay)

    def check_formatting(self, str):

        if re.fullmatch(format_re, str) is None:
            self.delayed_print("Invalid formatting dumbass")
            return False

        return True

    def get_indexed_elem(self, idx, list):
        try:
            idx = int(idx)
        except ValueError as e:
            self.delayed_print("That's not a number, silly tuna")
            return None

        if idx == -1:
            return None
        try:
            job = list[idx]
        except IndexError as e:
            self.delayed_print("Did you hit your head when you were little?")
            return None

        return job

    ##############################
    #           COMMANDS
    ##############################

    def help(self):
        """Print this help screen"""

        with self.lock:
            for k, v in self.cmd_actions.items():
                slowprint(f"-{k} : {v.__doc__}", parameters.print_delay)

    def progress(self):
        """Print the progress you achieved in time"""

        with self.lock:
            yn = slowprint_with_input(
                "You can either choose 'global' or 'local' project...\nI won't tell you the difference",
                parameters.print_delay)

            if yn == "global":
                self.global_progress()

            elif yn == "local":
                self.delayed_print("During this run you did:")
                for job in self.job_list:
                    self.delayed_print(job.progress())

            else:
                self.delayed_print("Not even this... you are such a useless human being")

    def change(self):
        """Change the parameters of a specific job """

        self.show_all()

        with self.lock:
            idx = slowprint_with_input(
                "Which id do you want to change?\nYou can either choose one or multiple (0,1,2...).\nUse -1 for none.",
                parameters.print_delay)

            jobs = []
            if "," in idx:
                for elem in idx.split(","):
                    to_change = self.get_indexed_elem(elem, self.job_list)
                    jobs.append(to_change)
            else:
                to_change = self.get_indexed_elem(idx, self.job_list)
                if to_change is None: return
                jobs.append(to_change)

            self.delayed_print("You can leave the current value by pressing 'Enter")
            for job in jobs:
                name = slowprint_with_input(f"Enter new name (currently {job.name})", parameters.print_delay)
                frequency = slowprint_with_input(f"Enter new frequency (currently {job.freq})", parameters.print_delay)
                rep = slowprint_with_input(f"Enter new repetitions (currently {job.rep})", parameters.print_delay)
                job.change_vals(name, frequency, rep)
                print("New values changed")

    def show_all(self):
        """Show all jobs (running or not)"""
        with self.lock:
            if len(self.job_list) == 0:
                self.delayed_print("No job currently running")
            for idx in range(len(self.job_list)):
                self.delayed_print(f"Id : {idx}\n{self.job_list[idx].summary()}\n")

    def stop_specific(self):
        """Stop a given job"""

        self.show_all()

        with self.lock:

            idx = slowprint_with_input(
                "Which id do you want to stop? You can type 'all' to stop them all or -1 for none",
                parameters.print_delay)

            if idx == "all":
                self.stop_all()
                return

            job = self.get_indexed_elem(idx, self.job_list)

            if job is None: return

            self.job_list[idx].stop.set()
            self.job_list[idx].start()

    def start_all(self):
        """Start every previously stopped exercise"""

        for job in self.job_list:
            if job.stop.is_set():
                job.stop.clear()
                job.start()

    def stop_all(self):
        """Start every previously stopped exercise"""

        for job in self.job_list:
            if not job.stop.is_set():
                job.stop.set()

    def add(self):
        """Add a job"""
        with self.lock:

            name = slowprint_with_input("What's the name of the exercise?", parameters.print_delay)
            frequency = slowprint_with_input("With what time frequency in minutes? (min,max)", parameters.print_delay)
            if not self.check_formatting(frequency): return
            rep = slowprint_with_input('How many repetitions? (min,max)', parameters.print_delay)
            if not self.check_formatting(rep): return

            good = slowprint_with_input(f"Is this good?[y/n]\nname: {name}\nfrequency: {frequency}\nrepetitions: {rep}",
                                        parameters.print_delay)

            if "n" in good.lower() or "no" in good.lower():
                self.delayed_print("Too bad...")
                return

            job = Job(name, frequency, rep)
            job.start()
            self.job_list.append(job)

    def save_job(self):
        """Save an exercise so it can be reloaded next time"""

        self.show_all()

        with self.lock:

            idx = slowprint_with_input(
                "Which id do you want to save?\nYou can type 'all' to save them all or -1 for none",
                parameters.print_delay)

            if idx == "all":
                self.save_all()
                return

            job = self.get_indexed_elem(idx, self.job_list)

            if job is None: return

            to_dump = {'name': job.name, 'freq': job.freq, 'rep': job.rep}
            dump_json(to_dump)

            slowprint_with_input(f"{job.name} have been saved", parameters.print_delay)

    def save_all(self):
        """Save every exercise in the list"""

        for job in self.job_list:
            to_dump = {'name': job.name, 'freq': job.freq, 'rep': job.rep}
            dump_json(to_dump)
            slowprint_with_input(f"{job.name} have been saved", parameters.print_delay)

    def load_job(self):
        """Load one or more exercises from the ones saved and starts it immediately"""

        saved = paths.get_saved_jobs()

        for idx in range(len(saved)):
            self.delayed_print(f"id {idx} : {saved[idx]}")

        idx = slowprint_with_input(
            "Which id do you want to load?\nYou can either choose one or multiple (0,1,2...).\nUse -1 for none.",
            parameters.print_delay)

        if "," in idx:
            for elem in idx.split(","):
                to_load = self.get_indexed_elem(elem, saved)
                job = load_json(os.path.join(paths.saved_jobs, to_load))

                new_job = Job(job['name'], job['freq'], job['rep'])

                self.job_list.append(new_job)
                new_job.start()
        else:
            to_load = self.get_indexed_elem(idx, saved)
            job = load_json(os.path.join(paths.saved_jobs, to_load))

            new_job = Job(job['name'], job['freq'], job['rep'])

            self.job_list.append(new_job)
            new_job.start()

    def global_progress(self):
        """Check out your global progresses"""

        today = []

        for elem in paths.get_progresses():
            date = elem.rsplit(":", 1)[0].split()[0].split("-")
            y = int(date[0])
            m = int(date[1])
            d = int(date[2])
            date = datetime.datetime(y, m, d)
            if date.date() != datetime.datetime.today().date():
                continue
            what = elem.rsplit(":", 1)[1].split(",")
            today.append(what)

        results = count_how_may(today)

        for k, v in results.items():
            self.delayed_print(f"You did {v} {k} today!")
