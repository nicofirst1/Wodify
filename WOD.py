import queue
import re
import threading

from Job import Job
from utils import slowprint, slowprint_with_input, slowprint_with_delay, parameters

format_re = re.compile("\d+,\d+")


class WOD(threading.Thread):

    def __init__(self):

        super().__init__()
        self.job_list = []

        self.cmd_actions = {
            'add': self.add, 'show': self.show_all,
            'change': self.change, 'stop all': self.stop_all,
            'stop': self.stop_specific, 'h': self.help,
            'help': self.help, 'progress': self.progress}

        self.stop = False
        self.lock = threading.Lock()
        self.queue = queue.Queue()

    ##############################
    #        MAIN STUFF
    ##############################

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

    def console(self):
        while 1:
            input()  # Afther pressing Enter you'll be in "input mode"
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

        for dict in self.job_list:
            slowprint_with_delay(dict['job'].progress(), parameters.print_delay, parameters.print_delay_sentence)

    def change(self):
        """Change the parameters of a specific job """

        with self.lock:
            self.show_all()
            idx = slowprint_with_input("Which id do you want to change? (-1) for none", parameters.print_delay)
            idx = int(idx)
            if idx == -1:
                return

            job = self.job_list[idx]
            name = slowprint_with_input("Enter new name (empty unchanged)", parameters.print_delay)
            frequency = slowprint_with_input("Enter new frequency (empty unchanged)", parameters.print_delay)
            rep = slowprint_with_input("Enter new repetitions (empty unchanged)", parameters.print_delay)

            job.change_vals(name, frequency, rep)
            print("New values changed")

    def show_all(self):
        """Show all jobs (running or not)"""
        with self.lock:
            if len(self.job_list) == 0:
                self.delayed_print("No job currently running")
            for idx in range(len(self.job_list)):
                self.delayed_print(f"Id : {idx}\n{self.worker_classes[idx]['job'].summary()}\n")

    def stop_specific(self):
        """Stop a given job"""
        with self.lock:

            self.show_all()
            idx = slowprint_with_input("Which id do you want to stop? (-1) for none", parameters.print_delay)

            try:
                idx = int(idx)
                if idx == -1:
                    return

                self.job_list[idx]['stop'].set()
                self.job_list[idx]['job'].start()
            except IndexError or ValueError as e:
                self.delayed_print(f"You just caused an error...\n{e}")

    def stop_all(self):
        """Stop every running job """

        for dict in self.job_list:
            stop = dict['stop']
            stop.set()

        # other actions

    def add(self):
        """Add a job"""
        with self.lock:

            input("Press enter twice to continue")
            name = slowprint_with_input("What's the name of the exercise?", parameters.print_delay)
            frequency = slowprint_with_input("With what time frequency? (min,max)", parameters.print_delay)
            if not self.check_formatting(frequency): return
            rep = slowprint_with_input('How many repetitions? (min,max)', parameters.print_delay)
            if not self.check_formatting(rep): return

            good = slowprint_with_input(f"Is this good?\nname: {name}\nfrequency: {frequency}\nrepetitions: {rep}",
                                        parameters.print_delay)

            if "n" in good.lower() or "no" in good.lower():
                self.delayed_print("Too bad...")
                return

            stop = threading.Event()
            job = Job(name, frequency, rep, stop)
            job.start()
            self.job_list.append({"job": job, "stop": stop})
