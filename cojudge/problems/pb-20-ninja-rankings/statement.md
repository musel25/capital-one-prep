# 20. Ninja rankings

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/ninja-rankings/)

PyBites is starting a campaign to try and pair up the highest ranking Ninjas with some of the lower ranking ones. Your task is to rank the given Ninjas according to their number of Bites.

We are going to delve into some *Object Oriented Programming* here because we want to retain state as we add more Ninjas to the `Ranking` class.

I have laid out the structure of the script for you. Your task is to flesh out the `Ninja` and `Rankings` classes.

The `Ninja` class will have the following features:

- string `name`
- integer `bites`
- support `<`, `>`, and `==`, based on `bites`
- print out in the following format: `[469] bob`

The `Rankings` class will have the following features:

- method `add()` that adds a Ninja object to the rankings
- method `dump()` that removes/dumps (and returns) the lowest ranking Ninja from Rankings
- method `highest()` returns the highest ranking `Ninja`, but it takes an optional `count` parameter indicating how many of the highest ranking Ninjas to return
- method `lowest()`, the same as highest but returns the lowest ranking Ninjas, also supports an optional `count` parameter
returns how many Ninjas are in Rankings when `len()` is called on it
- a `pair_up()` method that pairs up study partners: the highest with the lowest `Ninja` of the `ranking` instance, then the second highest with the second lowest `Ninja` of the `ranking` etc. It takes an optional count parameter indicating how many Ninjas to pair up (default = `3`).

Remember, that the standard library is your friend, best of luck!

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `ninjas`. **Run** checks the first three tests. **Submit** runs all
9. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
