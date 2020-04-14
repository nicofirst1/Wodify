from datetime import datetime
import queue
import re
import threading

from Group import Group, load_json_group
from Job import Job, load_json_job
from utils import slowprint, slowprint_with_input, slowprint_with_delay, parameters, Path_class, \
    count_how_may, dump_json_job

format_re = re.compile("\d+,\d+")


class WOD(threading.Thread):
    """
    Main class managing different jobs and console input
    """

    def __init__(self):

        super().__init__()
        self.job_list = []

        # implemented commands
        self.cmd_actions = {
            'add': self.add, 'show': self.show_all,
            'change': self.change, 'stop': self.stop_specific,
            'h': self.help,
            'help': self.help, 'progress': self.progress,
            'save': self.save_job, 'load': self.load_job,
            'addg': self.create_group, 'rung': self.run_group,}

        self.stop = False
        self.lock = threading.Lock()
        self.queue = queue.Queue()

    ##############################
    #        MAIN STUFF
    ##############################

    def run(self):
        """
        Run the main program
        :return:
        """

        self.delayed_print("Program started... press 'help' to view commands")

        # while not stopped
        while not self.stop:

            # ask for lock and get input
            with self.lock:
                cmd = input('> ')

            # if command is quit then break
            if cmd == 'quit':
                self.delayed_print("bie bie")
                break
            # check action and execute
            action = self.cmd_actions.get(cmd, self.invalid_input)
            action()

    def invalid_input(self):
        """
        invalid input action
        :return:
        """
        with self.lock:
            to_print = "Unknown command\n" \
                       "Type 'h' for help"
            slowprint(to_print, parameters.print_delay)

    ##############################
    #           UTILS
    ##############################

    def delayed_print(self, msg, print_delay=0, final_delay=0):
        """
        Delayed print to make things look cool
        :param msg: str, msg to be printed
        :param print_delay: float, delay when printing
        :param final_delay: float, delay after printing
        :return:
        """

        if not final_delay:
            final_delay = parameters.print_delay_sentence
        if not print_delay:
            print_delay = parameters.print_delay

        slowprint_with_delay(msg, print_delay, final_delay)

    def check_formatting(self, user_input):
        """
        Check for input format correctness
        :param user_input: str, the input
        :return: bool
        """

        if re.fullmatch(format_re, user_input) is None:
            self.delayed_print("Invalid formatting dumbass, canceling...")
            return False

        return True

    def get_indexed_elem(self, idx, jobs):
        """
        Return the index of an element
        :param idx: str, user input for the wanted idx
        :param jobs: list, list of jobs
        :return: None if something went wrong, or a job
        """
        try:
            idx = int(idx)
        except ValueError:
            self.delayed_print("That's not a number, silly tuna")
            return None

        if idx == -1:
            return None
        try:
            job = jobs[idx]
        except IndexError:
            self.delayed_print("Did you hit your head when you were little?")
            return None

        return job

    ##############################
    #           COMMANDS
    ##############################

    def help(self):
        """Print this help screen"""

        with self.lock:
            # for every command
            for k, v in self.cmd_actions.items():
                slowprint(f"-{k} : {v.__doc__}", parameters.print_delay)

    def progress(self):
        """Print the progress you achieved in time"""

        with self.lock:
            yn = slowprint_with_input(
                "You can either choose 'global' (for today) or 'local' (for this run).",
                parameters.print_delay)

            if yn == "global":
                self.global_progress()

            elif yn == "local":
                self.delayed_print("During this run you did:")
                for job in self.job_list:
                    self.delayed_print(job.progress())

            else:
                self.delayed_print("You didn't type either... How can you live like this?")

    def change(self):
        """Change the parameters of a specific job """

        # print all jobs
        self.show_all()

        with self.lock:
            idx = slowprint_with_input(
                "Which id do you want to change?\nYou can either choose one or multiple (0,1,2...).\nUse -1 for none.",
                parameters.print_delay)

            jobs = []
            idx+=","
            # if there are multiple jobs to change
            if "," in idx:
                for elem in idx.split(","):
                    to_change = self.get_indexed_elem(elem, self.job_list)

                    if to_change is None: continue

                    jobs.append(to_change)


            self.delayed_print("You can leave the current value by pressing 'Enter")
            # for every job that needs to be changed
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

            job.stop.set()
            self.job_list.remove(job)

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

            # save new workout
            to_dump = {'name': name, 'freq': frequency, 'rep': rep}
            dump_json_job(to_dump)

            job = Job(name, frequency, rep)
            job.start()
            self.job_list.append(job)

    def save_job(self):
        """Save an exercise so it can be reloaded next time"""

        self.show_all()

        with self.lock:

            idx = slowprint_with_input(
                "Which id do you want to save?\nYou can type 'all' to save them all or 'none' for none",
                parameters.print_delay)

            if idx == "all":
                self.save_all()
                return

            if idx == "none":
                return

            job = self.get_indexed_elem(idx, self.job_list)

            if job is None: return

            to_dump = {'name': job.name, 'freq': job.freq, 'rep': job.rep}
            dump_json_job(to_dump)

            slowprint_with_input(f"{job.name} have been saved", parameters.print_delay)

    def save_all(self):
        """Save every exercise in the list"""

        for job in self.job_list:
            to_dump = {'name': job.name, 'freq': job.freq, 'rep': job.rep}
            dump_json_job(to_dump)
            slowprint_with_input(f"{job.name} have been saved", parameters.print_delay)

    def load_job(self):
        """Load one or more exercises from the ones saved and starts it immediately"""

        saved, paths = Path_class.get_saved_jobs()

        for idx in range(len(saved)):
            self.delayed_print(f"id {idx} : {saved[idx]}")

        idx = slowprint_with_input(
            "Which id do you want to load?\nYou can either choose one or multiple (0,1,2...).\nUse -1 for none and 'all' to load everything.",
            parameters.print_delay)

        if idx == "all":
            for j in paths:
                new_job = load_json_job(j)

                self.job_list.append(new_job)
                new_job.start()

        elif "," in idx:
            for elem in idx.split(","):
                to_load = self.get_indexed_elem(elem, paths)
                new_job = load_json_job(to_load)

                self.job_list.append(new_job)
                new_job.start()
        else:
            to_load = self.get_indexed_elem(idx, paths)
            if to_load is None:
                return

            new_job = load_json_job(to_load)

            self.job_list.append(new_job)
            new_job.start()

    def global_progress(self):
        """Check out your global progresses"""

        today = []

        prgs=Path_class.get_progresses()
        # filter by today date
        prgs=[elem.split(" ",1)[1] for elem in prgs if datetime.today().date().__str__() in elem]

        # estimate total time taken
        dur=[prgs[0].rsplit(":",1)[0],prgs[-1].rsplit(":",1)[0]]
        dur=[elem.split(".")[0] for elem in dur]
        dur=datetime.strptime(dur[1],"%H:%M:%S")-datetime.strptime(dur[0],"%H:%M:%S")

        # get repetitions
        prgs=[elem.rsplit(":",1)[1] for elem in prgs ]
        prgs=[elem.split(",") for elem in prgs]

        rep_dict={}
        for k,v in prgs:

            if k not in rep_dict.keys():
                rep_dict[k]=0

            rep_dict[k]+=int(v)


        self.delayed_print(f"Today your workout lasted {dur}\nYou did:")


        for k, v in rep_dict.items():
            self.delayed_print(f"- {v} {k}")

    def create_group(self):
        """Add workouts together to create a group"""

        with self.lock:

            # get desired name
            name = slowprint_with_input("What's the name of the group?", parameters.print_delay)

            # load all jobs
            saved, paths = Path_class.get_saved_jobs()

            # show them to user
            for idx in range(len(saved)):
                self.delayed_print(f"id {idx} : {saved[idx]}")

            # wait for answer
            answ = slowprint_with_input(
                "Which exercise do you want to add?\nYou can either choose one or multiple (0,1,2...).\n",
                parameters.print_delay)

            # get desired jobs
            jobs = []
            if "," in answ:
                for elem in answ.split(","):
                    to_load = self.get_indexed_elem(elem, paths)
                    jobs.append(to_load)

            # create and save group
            group = Group(name, jobs)
            group.save()

            # ask for run
            answ = slowprint_with_input(
                "Do you want to start the group? [yn]",
                parameters.print_delay)

            if answ in ['y', "yes"]:
                group.start()
                self.job_list += group.jobs

    def run_group(self):
        """Load and run a saved group"""

        names, paths = Path_class.get_saved_groups()

        for idx in range(len(names)):
            self.delayed_print(f"id {idx} : {names[idx]}")

        # wait for answer
        answ = slowprint_with_input(
            "Group you want to load?\nYou can either choose one or multiple (0,1,2...).\n",
            parameters.print_delay)

        # get desired jobs
        groups = []
        if "," in answ:
            for elem in answ.split(","):
                to_load = self.get_indexed_elem(elem, paths)
                new_group = load_json_job(to_load)

                groups.append(new_group)
        else:

            to_load = self.get_indexed_elem(answ, paths)
            new_group = load_json_group(to_load)
            groups.append(new_group)


        for g in groups:
            self.job_list+=g.jobs
            g.start()