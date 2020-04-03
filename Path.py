import os
import threading


def join(path1, path2):
    return os.path.join(path1, path2)


class Paths:

    def __init__(self):

        current_path = os.getcwd()

        self.lock = threading.Lock()

        self.RESOURCES = join(current_path, "Resources")
        self.saved_jobs = join(self.RESOURCES, "saved_jobs")
        self.progresses = join(self.RESOURCES, "progresses.txt")

        # make resources dir if it does not exists
        if not os.path.exists(self.RESOURCES):
            os.makedirs(self.RESOURCES)

        # same thing with saved jobs
        if not os.path.exists(self.saved_jobs):
            os.makedirs(self.saved_jobs)

        # same with progresses
        if not os.path.exists(self.progresses):
            f = open(self.progresses, 'w')
            f.close()

    def get_saved_jobs(self):
        onlyfiles = [f for f in os.listdir(self.saved_jobs) if os.path.isfile(join(self.saved_jobs, f))]
        return onlyfiles

    def generate_res_dirs(self):
        if not os.path.exists(self.saved_jobs):
            os.makedirs(self.saved_jobs)

    def save_progress(self, what, how_many):

        with self.lock:
            with open(self.progresses, "a+") as file:
                to_write = f"{datetime.datetime.now()}:{what},{how_many}\n"
                file.write(to_write)

    def get_progresses(self):

        with self.lock:
            with open(self.progresses, "r+") as file:
                lines = file.readlines()

        return lines
