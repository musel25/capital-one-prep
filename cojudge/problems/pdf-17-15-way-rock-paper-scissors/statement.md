# 17. 15-way rock paper scissors

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/15-way-rock-paper-scissors/)

Implement `_create_defeat_mapping(csv_text=SCORES)` and `get_winner(player1, player2)`. `SCORES` is a local CSV with columns `winner,loser`. Each row is a directed defeat edge from the original RPS15 graph: the winner defeats the loser. The helper returns a new dictionary mapping each listed winner to a set of its losers. Duplicate rows do not duplicate losers. A header-only CSV returns an empty dictionary. The CSV uses valid gesture names. `get_winner` accepts only strings that exactly match the lower-case names in `GESTURES`; do not strip whitespace or change case. Invalid values, including non-strings, raise ValueError. Validate both inputs before checking for a tie. Equal valid gestures return the string `Tie`. Otherwise return the lower-case text `<winner> defeats <loser>`, regardless of which argument wins. The graph has 15 gestures and 105 distinct unordered matchups. Use `_create_defeat_mapping` in `get_winner` to parse the supplied CSV and determine its outcomes.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The premium CSV, docstring, and original RPS15 phrase tests are unavailable. The local CSV preserves all 105 defeat relationships from [David C. Lovelace’s RPS15 graph](https://www.umop.com/rps15.htm). Output is simplified to "winner defeats loser"; it does not reproduce the original action phrases.

<details>
<summary>Original public description</summary>

In this Bite you are going to write a 15-way Rock Paper Scissors game (this challenge first appeared as part of our [100 Days of Code in Python course](https://talkpython.fm/100days)).

(source: [http://www.umop.com/rps15.htm](http://www.umop.com/rps15.htm))

The way you read this graphic is if an arrow points from one item to another, that pointed-to item is defeated. For example:

- Paper defeats rock (paper points to rock)
- Devil defeats human (devil points to human)

It turns out to be error prone and generally very unfun to work this out from the graphic. So we created a `csv` score sheet representing these relationships.

Complete the `get_winner` function following the docstring. We recommend parsing it into a dictionary/mapping of *players -> beats whom* (key, value) pairs (helper function `_create_defeat_mapping`). This will make it easier to determine the winner given any pair of (player1, player2) pairs.

The tests (see *TESTS* tab) will verify valid input to `get_winner`, all *Tie* scenarios and (more interestingly) all 105 outcomes using the original *[RPS-15 speak](http://www.umop.com/rps15.htm)*.

Good luck and have fun!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`rps15`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
