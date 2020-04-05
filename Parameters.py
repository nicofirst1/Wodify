import sys


class Parameters:
    # tutorial
    TUTORIAL = True

    # the slowness of the print time
    print_delay = 0.02

    # the time to wait after starting a new sentence
    print_delay_sentence = 0.2

    # the number of beeps
    beep_repetitions = 1
    # the duration of a single beep in seconds
    beep_duration = 1
    # the frequency of a beep
    beep_frequency = 600

    platform = sys.platform

    # What OS are you using?
    # U -> ubuntu
    # W -> windows
    # M -> macOS

    if platform == "darwmin":
        OS = "M"
    elif platform == "win32":
        OS = "W"
    else:
        OS = "U"
