## Introduction:
LakeRubbishCollection is my work for Science Talent Search. It is a computer game (program (using the computer language Python)).

## Prepare to play:
- Install the latest python environment on your computer
refer to https://www.python.org/downloads/release

- Install the pygame dependencies.
```sh
$ pip install -U pygame
```

- Install GIT(version control) tool on your computer
refer to https://git-scm.com/downloads

- Download the game repository
```sh
$ git clone https://gitee.com/tyronexj/LakeRubbishCollection.git
```

- Start the game
```sh
$ cd LakeRubbishCollection
$ python LakeRubbishCollection.py
```

## Instructions:
There's too many rubbishes in the lake, which is harmful to either the ecosystem and the environment.
Your mission is to collect rubbish as much as possible in 30 seconds without interrupting the fishes,
which is bumping into them. Remember to keep an eye on the 'time left' section!

You will earn 5 points for collecting 1 rubbish.
Your character could be killed due to two things:
1: Killed due to timeout.
2: Killed by bumping into a fish (or more).
Try to avoid rubbish bumping into the fish, which will make the fish disappear. But be careful - 
you will also lose 1 point if 1 rubbish bumped into 1 fish!
The strategy to stop rubbishes bumping into fishes is to collect the rubbish BEFORE it bumps into 
a fish.
