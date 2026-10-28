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

**Constraints:**

- Counts are nonnegative integers. Add each person once. Pair at most `min(count, len(rankings) // 2)` people pairs.
