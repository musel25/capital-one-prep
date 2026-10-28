After Write a property let's write a bit more advanced one.

In this Bite you are presented with a `NinjaBelt` class that keeps track of scores and Ninja Belts earned (a very real scenario). Some setup code has been provided like the `_score` and `_last_earned_belt` variables and the getter and setter methods that make up the property.

The goal is to write a property called `score` that does the following:

1. Make sure it can only be assigned an integer,
1. It can not be assigned a score lower than the current score,
1. It checks in `BELTS` if a new belt was earned (for example going from 49 to 50 you earn the *yellow belt*), if so it stores it in `self._last_earned_belt`.
1. For each new score print a message:
  - If a new badge was earned: "*Congrats, you earned {score} points obtaining the PyBites Ninja {rank} Belt" *(where *rank* is the name of the belt titlecased, e.g. *White*, *Yellow*, etc.)
  - Else just the new score: "*Set new score to {score}"*

See the TESTS tab for more info. Good luck, have fun and keep calm and code in Python!

**Constraints:**

- The initial score is a nonnegative integer. A `bool` is not a valid score.
