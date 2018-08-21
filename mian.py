import re
import threading
import time

from Job import Job
from WOD import WOD
from utils import slowprint_with_delay, slowprint_with_input

TUTORIAL = False


def tutotrial():
    print_delay = 0.0004
    final_delay = 1
    wod = WOD()
    slowprint_with_delay("", print_delay, final_delay)

    slowprint_with_delay("Welcome to Wodify!", print_delay, final_delay)
    slowprint_with_delay("Are you a student spending the vast majority of the time in front of a screen?", print_delay,
                         final_delay)
    slowprint_with_delay("The last time you saw a gym was summer 2012?", print_delay, final_delay)
    slowprint_with_delay("Fear no more my tiny fat friend, since I'm here!", print_delay, final_delay)
    yn = slowprint_with_input("Do you want to go through the tutorial? [y/n]", print_delay)

    if yn.lower() == "y":
        slowprint_with_delay("That's the spirit", print_delay, final_delay)
    else:
        slowprint_with_delay("As if your opinion matters...", print_delay, final_delay)

    slowprint_with_delay("So, to begin with I'll read your message when, and only when, you see the '>' symbol ",
                         print_delay, final_delay)
    slowprint_with_delay("If you don't see it press 'enter'", print_delay, final_delay + 0.5)
    slowprint_with_delay("Go on... press it", print_delay, final_delay + 1)
    slowprint_with_delay("Not working?\nThat's because it's the tutorial you dumb fat ass, focus", print_delay,
                         final_delay)
    slowprint_with_delay(
        "Any how, there are various commands you can use, first of all 'h' or 'help' for helpful infos", print_delay,
        final_delay)
    slowprint_with_delay("Try it (this time for real)", print_delay, final_delay)
    wod.start()
    while not wod.lock.locked():
        pass
    while wod.lock.locked():
        pass
    wod.stop = True

    slowprint_with_delay("\nCool right?", print_delay, final_delay)
    slowprint_with_delay("To add a job you have to fill in some infos", print_delay, final_delay)
    slowprint_with_delay("The first one will be the name of it...", print_delay, final_delay)
    name = slowprint_with_input("Try something like 'pushups'", print_delay)

    if name.lower() != "pushups":
        slowprint_with_delay(f"We have a smart ass here...\nFine '{name} will be", print_delay, final_delay)
    else:
        slowprint_with_delay("Good job", print_delay, final_delay)

    slowprint_with_delay("Now we need a time frequency\nThis will be the range (in minutes) for the random timer.\n"
                         "Every time a new random value in range wll be estimated and you will be reminded to do your exercises\n"
                         "Be careful to respect the formatting, I'm a lazy program... I don't want to try/catch everything you throw at me.\n"
                         "Remeber the format is always:\n"
                         "min,max", print_delay, final_delay + 1)
    freq = slowprint_with_input("Now insert the time frequency", print_delay)

    format_re = re.compile("\d+,\d+")

    if re.fullmatch(format_re, freq) is None:
        slowprint_with_delay(
            "Seriously?\nYou know what, I just put you in an while loop...\nYou can do whatever you want here,"
            " be as stupid as you want.\nThe only thing that changes is the time you loose.\nAh...right... "
            "your time is as worthless as you...\nSorry",
            print_delay, final_delay)
        slowness = 0.1
        while re.fullmatch(format_re, freq) is None:
            slowprint_with_delay("Common! You can do it little guy!", print_delay + slowness, final_delay + slowness)
            freq = slowprint_with_input("Now insert the time frequency", print_delay + slowness)
            slowness += 0.1
    else:
        slowprint_with_delay("Nice! You are smarter than you look! (must be that nerdy face of yours)", print_delay,
                             final_delay)

        rep = slowprint_with_input(
            f"Now do the same for the number of repetitions. This wll be the number of time you do {name}", print_delay)

    if re.fullmatch(format_re, rep) is None:
        slowprint_with_delay("Again?! You know what\n Enjoy the count down", print_delay, final_delay)

        while re.fullmatch(format_re, rep) is None:
            count_down = 10
            while count_down > 0:
                print(f"{count_down}\r", end="")
                count_down -= 1
                time.sleep(1)

            slowprint_with_delay("Lets try again..", print_delay, final_delay)
            rep = slowprint_with_input(f"Insert the number of repetitions", print_delay)

    else:
        slowprint_with_delay("Good job! I'll give you a banana when you're done with this", print_delay, final_delay)

    stop = threading.Event()
    ex = Job(name, freq, rep, stop)
    ex.start()
    wod.worker_classes.append({"ex": ex, "stop": stop})


if TUTORIAL:
    tutotrial()

wod = WOD()
wod.start()

