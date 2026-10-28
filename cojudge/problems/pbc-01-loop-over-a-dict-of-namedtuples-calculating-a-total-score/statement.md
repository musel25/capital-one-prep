# 01. Loop over a dict of namedtuples calculating a total score

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/loop-over-a-dict-of-namedtuples-calculating-a-total-score/)

Implement `get_total_points(belts=ninja_belts)`. Each value is a `BeltStats(score, ninjas)` namedtuple. Return the sum of score multiplied by the number of ninjas. Scores and counts are nonnegative integers. An empty dictionary returns 0. Do not change the input.

**Source and offline changes:** This version keeps the original free template and tests, with added boundary tests.

<details>
<summary>Original public description</summary>

In this Bite you calculate the total amount of points earned with Ninja Belts by accessing the given `ninja_belts` dict.

You learn how to access *score* and *ninjas* (= amount of belt owners) from no less than a [`namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple) (if you're new to them, [check out the basic `Point` example in the docs](https://docs.python.org/3/library/collections.html#collections.namedtuple)).

Why a namedtuple, you did not even mention a tuple yet?!

Good point, well in our Bites we might actually use them even more so let's get to know them here (if you have a free evening read up on the [`collections` module](https://docs.python.org/3/library/collections.html) as well and thank us later).

The function returns the total score `int`. You learn to write generic code because we test for an updated `ninja_belts` dict as well, see the TESTS tab.

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`belts`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
