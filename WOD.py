import os
import queue
import random
import threading

from utils import slowprint, slowprint_with_input


class WOD:

    def __init__(self):

        self.worker_classes=[]
        self.delay=0.04
        self.cmd_actions = {'add': self.add,'show':self.show_all,'change':self.change, 'stop all':self.stop_all, 'stop':self.stop_specific, 'h':self.help}


    def console(self,q, lock):
        while 1:
            input()  # Afther pressing Enter you'll be in "input mode"
            with lock:
                cmd = input('> ')

            q.put(cmd)
            if cmd == 'quit':
                print("bie bie")
                break

    def show_all(self,lock):
        """Show all jobs (running or not)"""
        with lock:
            if len(self.worker_classes)==0:
                slowprint("No job currently running",self.delay)
            for idx in range(len(self.worker_classes)):
                slowprint(f"Id : {idx}\n{self.worker_classes[idx]['ex'].summary()}\n",self.delay)


    def add(self,lock):
        """Add a job"""
        with lock:

            name = slowprint_with_input("What's the name of the exercise",self.delay)
            frequency = slowprint_with_input("With what time frequency? (min,max)",self.delay)
            rep = slowprint_with_input('How many repetitions? (min,max)',self.delay)
            good=slowprint_with_input(f"Is this good?\nname: {name}\nfrequency: {frequency}\nrepetitions: {rep}",self.delay)


            if "n" in good.lower() or "no" in good.lower():
                slowprint("Too bad...",self.delay)
                return

            stop=threading.Event()
            ex=Exercise(name,frequency,rep,stop)
            ex.start()
            self.worker_classes.append({"ex":ex,"stop":stop})

    def stop_all(self,lock):
        """Stop every running job """

        for dict in self.worker_classes:
            stop=dict['stop']
            stop.set()


    def stop_specific(self,lock):
        """Stop a given job"""
        with lock:

            self.show_all(lock)
            idx=slowprint_with_input("Which id do you want to stop? (-1) for none",self.delay)
            idx=int(idx)
            if idx==-1:
                return

            self.worker_classes[idx]['stop'].set()
            self.worker_classes[idx]['ex'].start()


    def change(self, lock):
        """Change the parameters of a specific job """

        with lock:

            self.show_all(lock)
            idx=slowprint_with_input("Which id do you want to change? (-1) for none",self.delay)
            idx=int(idx)
            if idx==-1:
                return

            ex=self.worker_classes[idx]
            name=slowprint_with_input("Enter new name (empty unchanged)",self.delay)
            frequency=slowprint_with_input("Enter new frequency (empty unchanged)",self.delay)
            rep=slowprint_with_input("Enter new repetitions (empty unchanged)",self.delay)

            ex.change_vals(name,frequency,rep)
            print("New values changed")

        # other actions

    def invalid_input(self,lock):
        with lock:
            to_print="Unknown command\n" \
                     "Type 'h' for help"
            slowprint(to_print,self.delay)

    def help(self,lock):
        """Print this help screen"""

        with lock:
            for k,v in self.cmd_actions.items():
                slowprint(f"-{k} : {v.__doc__}",self.delay)

    def start(self):
        cmd_queue = queue.Queue()
        stdout_lock = threading.Lock()

        dj = threading.Thread(target=self.console, args=(cmd_queue, stdout_lock))
        dj.start()

        while 1:
            cmd = cmd_queue.get()
            if cmd == 'quit':
                break
            action = self.cmd_actions.get(cmd, self.invalid_input)
            action(stdout_lock)



class Exercise(threading.Thread):

    def __init__(self, name, freq, rep, stop):
        super().__init__()
        self.name=name
        self.freq= self.get_number(freq)
        self.rep=self.get_number(rep)
        self.stop=stop

        self.total=0


    def change_vals(self, name, freq, rep):
        if name:
            self.name = name

        if freq:
            self.freq = self.get_number(freq)

        if rep:
            self.rep = self.get_number(rep)

    def get_number(self, string):
        try:
            l,u=string.split(",")
            l=int(l)
            u=int(u)
        except Exception as e:
            print(e)
            l=-1
            u=-1
        return (l,u)



    def run(self):

        print(f"Starting\n{self.summary()}")

        while not self.stop.is_set():

            random_wait=random.randint(self.freq[0],self.freq[1])*60
            while not self.stop.wait(timeout=random_wait):
                random_rep=random.randint(self.rep[0],self.rep[1])
                self.play_soud(repeat=2)
                print(f"You must do {random_rep} {self.name}")
                self.total+=random_rep
                break

        print(f"{self.summary()}\nStopped\n\n")

    def summary(self):
        to_print=f"Exercise : {self.name}\nFrequency : {self.freq}\nRepetitions : {self.rep}"
        return to_print


    def play_soud(self,duration=1, freq=500, repeat=1):
        """
        Play a sound
        :param duration: duration in seconds
        :param freq: frequence of the sound
        :return:
        """

        for i in range(repeat):
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))




wod=WOD()
wod.start()