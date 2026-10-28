In this Bite you are going to write a 15-way Rock Paper Scissors game (this challenge first appeared as part of our [100 Days of Code in Python course](https://talkpython.fm/100days)).

(source: [http://www.umop.com/rps15.htm](http://www.umop.com/rps15.htm))

The way you read this graphic is if an arrow points from one item to another, that pointed-to item is defeated. For example:

- Paper defeats rock (paper points to rock)
- Devil defeats human (devil points to human)

It turns out to be error prone and generally very unfun to work this out from the graphic. So we created a `csv` score sheet representing these relationships.

Complete the `get_winner` function following the docstring. We recommend parsing it into a dictionary/mapping of *players -> beats whom* (key, value) pairs (helper function `_create_defeat_mapping`). This will make it easier to determine the winner given any pair of (player1, player2) pairs.

The tests (see *TESTS* tab) will verify valid input to `get_winner`, all *Tie* scenarios and (more interestingly) all 105 outcomes using the original *[RPS-15 speak](http://www.umop.com/rps15.htm)*.

Good luck and have fun!

This version returns `winner defeats loser` or `Tie`, using the supplied local CSV.

**Constraints:**

- Accept exact lower-case gesture names; invalid values raise `ValueError`, including invalid ties.
- `_create_defeat_mapping` returns winner-to-set-of-losers mappings from the supplied CSV.
