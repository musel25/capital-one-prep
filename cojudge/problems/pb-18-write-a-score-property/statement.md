# 18. Write a score property

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/write-a-score-property/)

**Inputs and required behavior for this version:**

The constructor takes a nonnegative int score, with bool excluded. It stores the score without a message or an earned belt. Assignment accepts only int values, with bool excluded, and must not lower the current score. Invalid assignments raise ValueError without state changes or output. Equal scores are allowed. Each valid assignment prints one message. Award the highest reached belt when it differs from the last earned belt. Scores above 1000 retain red. Invalid constructor values are outside this exercise; constructor validation is not required.

<details>
<summary>Original bite description</summary>

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

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `ninjabelt`. **Run** checks the first three tests. **Submit** runs all
32. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
