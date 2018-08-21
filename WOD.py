import os
import queue
import random
import threading


class WOD:

    def __init__(self):

        self.worker_classes=[]

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
        for idx in range(len(self.worker_classes)):
            print(f"Id : {idx}\n{self.worker_classes[idx]['ex'].summary()}\n")


    def add(self,lock):
        with lock:

            name = input('> Inser the name of the exercise\n')
            frequency = input('> Insert the time frequency (min,max) in minutes\n')
            rep = input('> Insert the (min,msx) repetitions\n')
            good=input(f"> Is this good?\nname: {name}\nfreq: {frequency}\nrep: {rep}\n")


            if "n" in good.lower() or "no" in good.lower():
                return

            stop=threading.Event()
            ex=Exercise(name,frequency,rep,stop)
            ex.start()
            self.worker_classes.append({"ex":ex,"ev":stop})

    def stop_all(self,lock):

        for _, stop in self.worker_classes:
            stop.clear()



    def change(self, lock):

        with lock:

            self.show_all(lock)
            idx=input("> Which id do you want to change? (-1) for none\n")
            idx=int(idx)
            if idx==-1:
                return

            ex=self.worker_classes[idx]
            name=input("> Enter new name (empty unchanged)\n")
            frequency=input("> Enter new frequency (empty unchanged)\n")
            rep=input("> Enter new repetitions (empty unchanged)\n")

            ex.change_vals(name,frequency,rep)
            print("New values changed")

        # other actions

    def invalid_input(self,lock):
        with lock:
            print('--> Unknown command')

    def start(self):
        cmd_actions = {'add': self.add,'show':self.show_all,'change':self.change}
        cmd_queue = queue.Queue()
        stdout_lock = threading.Lock()

        dj = threading.Thread(target=self.console, args=(cmd_queue, stdout_lock))
        dj.start()

        while 1:
            cmd = cmd_queue.get()
            if cmd == 'quit':
                break
            action = cmd_actions.get(cmd, self.invalid_input)
            action(stdout_lock)



class Exercise(threading.Thread):

    def __init__(self, name, freq, rep, stop):
        super().__init__()
        self.name=name
        self.freq= self.get_number(freq)
        self.rep=self.get_number(rep)
        self.stop=stop


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

        while not self.stop:

            random_wait=random.randint(self.freq[0],self.freq[1])*60
            while not self.stop.wait(timeout=random_wait):
                random_rep=random.randint(self.rep[0],self.rep[1])
                self.play_soud(repeat=2)
                print(f"You must do {random_rep} {self.name}")
                break


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