# 09. Write your own data class

[Course list](/?course=pybites-oop) · Pybites Intermediate · [Original bite](https://pybitesplatform.com/bites/write-your-own-data-class/)

**Inputs and required behavior for this version:**

Use an int number and str title and level. Empty strings and zero or negative numbers are allowed. Do not validate these values. Apply str.capitalize() to title once at construction. The default level is 'Beginner'. Use a mutable, ordered dataclass with fields number, title, level. Equality and ordering compare all three fields in that order. Other input types are outside this exercise.

<details>
<summary>Original bite description</summary>

As you might have noticed we are now on Python 3.7 so time for a Bite on *data classes* which were introduced with [PEP 557](https://www.python.org/dev/peps/pep-0557/).

What are they? Raymond Hettinger summarized it nicely [in his great talk](https://www.youtube.com/watch?v=T-TwcmT6Rcw): *a mutible named tuple with defaults*.

One advantage is the code it saves you typing so they might become an essential part of your Python toolkit!

In this Bite we have you write a data class called `Bite` that managed 3 attributes: *number*, *title*, and *level*. Their types are `int`, `str` and `str` respectively.

There are 3 more requirements:

1. *title* needs to be capitalized upon instantiation (you get a hint in the tests for this one :) - make sure to read the tests for additonal specs, including some of the differences between `data class`es and `namedtuple`s!)
1. *level* takes a default argument of *Beginner*.
1. A collection of Bite instances needs to be orderable (using `sort` / `sorted` - this is not by default but configurable ...)

Good luck and keep up with the language, exciting new things are getting added!
On that note feel free to make us more Bite requests via our Bites homepage (you'll find a form per Bite level at the bottom of the page ...)

For more resources on *data classes* we recommned watching [Hettinger's talk](https://www.youtube.com/watch?v=T-TwcmT6Rcw) as well as reading through Anthony Shaw's [A brief tour of Python 3.7 data classes](https://hackernoon.com/a-brief-tour-of-python-3-7-data-classes-22ee5e046517). Have fun!

</details>

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `bite`. **Run** checks the first three tests. **Submit** runs all
13. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
