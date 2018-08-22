import datetime
import threading


class Parameters:


    # the slowness of the print time
    print_delay = 0.02

    # the time to wait after starting a new sentence
    print_delay_sentence = 1

    # the number of beeps
    beep_repetitions = 2
    # the duration of a single beep in seconds
    beep_duration = 1
    # the frequency of a beep
    beep_frequency = 400

    def __init__(self):
        a = 1






import os

class Paths:



    def __init__(self):

        current_path=os.getcwd()

        self.lock=threading.Lock()

        self.RESOURCES=os.path.join(current_path,"Resources")
        self.saved_jobs=os.path.join(self.RESOURCES,"saved_jobs")
        self.progresses=os.path.join(self.RESOURCES,"progresses.txt")

        try:
            open( self.progresses, 'r')
        except IOError:
            open( self.progresses, 'w')



    def get_saved_jobs(self):
        onlyfiles = [f for f in os.listdir(self.saved_jobs) if os.path.isfile(os.path.join(self.saved_jobs, f))]
        return onlyfiles

    def generate_res_dirs(self):
        if not os.path.exists(self.saved_jobs):
            os.makedirs(self.saved_jobs)


    def save_progress(self, what, how_many):

        with self.lock:

            with open(self.progresses,"a+") as file:
                to_write=f"{datetime.datetime.now()}:{what},{how_many}\n"
                file.write(to_write)


    def get_progresses(self):

        with self.lock:
            with open(self.progresses,"r+") as file:
                lines=file.readlines()

        return lines

