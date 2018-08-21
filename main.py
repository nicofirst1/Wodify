import re
import time

from WOD import WOD
from utils import slowprint_with_delay, play_sound, slow_print_input_ingore_enter, parameters

TUTORIAL = False


def tutotrial():
    print_delay = parameters.print_delay
    final_delay = parameters.print_delay_sentence

    wod = WOD()
    slowprint_with_delay("", print_delay, final_delay)

    slowprint_with_delay("Welcome to Wodify!", print_delay, final_delay)
    slowprint_with_delay("Are you a student spending the vast majority of your time in front of a screen?", print_delay,
                         final_delay)
    slowprint_with_delay("The last time you saw a gym was summer 2012?", print_delay, final_delay)
    slowprint_with_delay("Fear no more my tiny fat friend, since I'm here!", print_delay, final_delay)
    yn = slow_print_input_ingore_enter("Do you want to go through the tutorial? [y/n]", print_delay)

    if yn.lower() == "y":
        slowprint_with_delay("That's the spirit", print_delay, final_delay)
    else:
        slowprint_with_delay("As if your opinion matters...", print_delay, final_delay)

    slowprint_with_delay(
        "First, you must know that I'll read your message when, and only when, you see the '>' symbol at the start of the sentence",
        print_delay, final_delay)
    slowprint_with_delay("If you don't see it press 'enter'", print_delay, final_delay + 0.5)
    slowprint_with_delay("Go on... press it", print_delay, final_delay + 1)
    slowprint_with_delay("Not working?\nThat's because it's the tutorial you dumb fat ass, focus", print_delay,
                         final_delay)
    slowprint_with_delay(
        "Anyhow, there are various commands you can use, first of all 'h' or 'help' for helpful infos", print_delay,
        final_delay)
    slowprint_with_delay("Try it (this time for real)", print_delay, final_delay)

    h = slow_print_input_ingore_enter("", print_delay)

    if h.strip() != "h" and h.strip() != "help":
        slowprint_with_delay("Oh no, I didn't know you were retarded...", print_delay, final_delay)
        slowprint_with_delay("I'm ...", print_delay, final_delay)
        slowprint_with_delay("I'm sorry about that", print_delay, final_delay)
        slowprint_with_delay("Here, let me help", print_delay, final_delay)
        slowprint_with_delay("> h", print_delay + 0.5, final_delay)

    wod.help()

    slowprint_with_delay("\nCool right?", print_delay, final_delay)
    slowprint_with_delay("To add a job you have to fill in some infos", print_delay, final_delay)
    slowprint_with_delay("The first one will be the name of it...", print_delay, final_delay)
    name = slow_print_input_ingore_enter("Try something like 'pushups'", print_delay)

    if name.lower() != "pushups":
        slowprint_with_delay(f"We have a smart ass here...\nFine '{name} will be", print_delay, final_delay)
    else:
        slowprint_with_delay("Good job", print_delay, final_delay)

    slowprint_with_delay("Now we need a time frequency\nThis will be the range (in minutes) for the random timer.\n"
                         "Every time a new random value in range wll be estimated and you will be reminded to do your exercises\n"
                         "Be careful to respect the formatting, I'm a lazy program... I don't want to try/catch everything you throw at me.\n"
                         "Remeber the format is always:\n"
                         "min,max", print_delay, final_delay + 1)
    freq = slow_print_input_ingore_enter("Now insert the time frequency", print_delay)

    format_re = re.compile("\d+,\d+")

    if re.fullmatch(format_re, freq) is None:
        slowprint_with_delay(
            "Seriously?\nYou know what, I just put you in an while loop...\nYou can do whatever you want here,"
            " be as stupid as you want.\nThe only thing that changes is the time you loose.\nAh...right... "
            "your time is as worthless as you...\n",
            print_delay, final_delay)
        slowness = 0.1
        while re.fullmatch(format_re, freq) is None:
            slowprint_with_delay("Common! You can do it little guy!", print_delay + slowness, final_delay + slowness)
            freq = slow_print_input_ingore_enter("Now insert the time frequency", print_delay + slowness)
            slowness += 0.1
    else:
        slowprint_with_delay("Nice! You are smarter than you look! (must be that nerdy face of yours)", print_delay,
                             final_delay)

    rep = slow_print_input_ingore_enter(
        f"Now do the same for the number of repetitions. This wll be the number of time you do {name}", print_delay)

    if re.fullmatch(format_re, rep) is None:
        slowprint_with_delay("...\nYou know what\nEnjoy the count down", print_delay, final_delay)

        while re.fullmatch(format_re, rep) is None:
            count_down = 10
            while count_down > 0:
                print(f"{count_down}")
                count_down -= 1
                time.sleep(1)

            slowprint_with_delay("Lets try again..", print_delay, final_delay)
            rep = slow_print_input_ingore_enter(f"Insert the number of repetitions", print_delay)

    else:
        slowprint_with_delay("Good job! I'll give you a banana when you're done with this", print_delay, final_delay)

    slowprint_with_delay("So now the timer has started and it will soon go off (increase the speakers volume)",
                         print_delay, final_delay)
    slowprint_with_delay("...", print_delay, final_delay)

    slowprint_with_delay(".....", print_delay, final_delay)

    slowprint_with_delay("........", print_delay, final_delay)
    slowprint_with_delay("Never mind, let's speed up time", print_delay, final_delay)
    slowprint_with_delay(f"You must do {rep} {name}", print_delay, final_delay)
    play_sound()
    slowprint_with_delay("Scared?", print_delay, final_delay)
    slowprint_with_delay("I bet you are, you little pussy.", print_delay, final_delay)
    slowprint_with_delay("Finally you can configure some parameters in the 'Parameters.py' if you want", print_delay, final_delay)
    slowprint_with_delay("Any this is it, at least for the basic stuff.", print_delay, final_delay)
    slowprint_with_delay("If you're in doubt about something use 'help' or just look at the source code.", print_delay,
                         final_delay)
    slowprint_with_delay("Oh yes, one last thing.", print_delay, final_delay)
    slowprint_with_delay(
        "I now you like me, and I like you too, but for your sanity I strongly advise you to turn the tutorial off for the next run.",
        print_delay, final_delay)
    slowprint_with_delay("In the main.py file there is a big TUTORIAL variable you should set to false.", print_delay,
                         final_delay)
    slowprint_with_delay("Is up to you.", print_delay, final_delay)
    slowprint_with_delay("See you little bitch", print_delay, final_delay)
    slowprint_with_delay("<3\n", print_delay, final_delay)


if TUTORIAL:
    tutotrial()

wod = WOD()
wod.start()
