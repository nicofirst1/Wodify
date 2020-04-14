# Intro
Do you find yourself staring at a computer for most of your time?

Do you feel tired every day?

Would you like to stay fit during this quarantine?

Here I am to help!

I am a simple and easy program which will remind you to do some workout once in a while.
Just clone the repo start me with:

`python main.py`


## How does it work?
Wodify goes by the philosophy of 'random is better'.

When adding a custom exercise you will have two specify three things:

- A name for the workout.
- A time range _[min,max]_ : two integers split by a comma which will represent the random range where to take the waiting time from. 
For example if you enter [5,10] you will reminded to exercise every __X__ minutes where _X_ is in range [5,10] minutes.
- Repetition range _[min,max]_: same principle as before, this will be the number of repetitions to execute for your workout.

A quick video tutorial is avaiable ![on youtube](https://www.youtube.com/watch?v=pbNjdDRvRw0).

## Additional Infos

- To enable sound on Mac\Linux you should install "sox"
`sudo port install sox`

- Set the TUTORIAL flag to 'true' in the Parameters class to start the tutorial

- Change settings in the Parameter class.