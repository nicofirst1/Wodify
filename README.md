# Intro
Do you find yourself staring at a computer for most of your time?
Do you feel more tired by the day?
After that last pizza you just rolled from the kitchen to the bedroom?

Here I am to help!
I am a simple and easy program which will remind you to do some workout once in a while.
Just download me and start me with:

`python main.py`

And you'll fit again in no time.

## How does it work?
Wodify goes by the philosophy of 'random is better'.
When entering an exercise you will have two specify three things:
- A name for the workout.
- Time range _[min,max]_ : two integers slit by a comma which will represent the random range where to take the waiting time from. 
For example if you enter [5,10] you will reminded to exercise every __X__ minutes where _X_ is in range [5,10].
- Repetition range _[min,max]_: s ame principle as before, this will be the number of repetitions to execute for your workout.

## Additional Infos

- To enable sound on Mac\Linux you should install "sox"
`sudo port install sox`

- Set the TUTORIAL flag to 'true' in the Parameters class to start the tutorial

- Change settings in the Parameter class.