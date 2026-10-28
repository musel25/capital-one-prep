In this Bite you calculate the total amount of points earned with Ninja Belts by accessing the given `ninja_belts` dict.

You learn how to access *score* and *ninjas* (= amount of belt owners) from no less than a [`namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple) (if you're new to them, [check out the basic `Point` example in the docs](https://docs.python.org/3/library/collections.html#collections.namedtuple)).

Why a namedtuple, you did not even mention a tuple yet?!

Good point, well in our Bites we might actually use them even more so let's get to know them here (if you have a free evening read up on the [`collections` module](https://docs.python.org/3/library/collections.html) as well and thank us later).

The function returns the total score `int`. You learn to write generic code because we test for an updated `ninja_belts` dict as well, see the TESTS tab.

**Constraints:**

- Scores and owner counts are nonnegative integers.
