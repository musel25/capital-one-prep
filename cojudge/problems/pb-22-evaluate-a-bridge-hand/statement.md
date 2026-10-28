# 22. Evaluate a bridge hand

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/evaluate-a-bridge-hand/)

**Inputs and required behavior for this version:**

A valid hand is a sequence of 13 distinct Card objects from the supplied deck. Each Card contains a Suit member and a Rank member. Non-sequences raise TypeError. Sequences with a length other than 13, or any non-Card element, raise ValueError. The hand stores a snapshot; later changes to the input sequence do not change it. String output sorts suits in SHDC order and ranks in AKQJT98765432 order, and omits void suits. All seven evaluation properties are read-only and follow the stated point and losing-trick rules. Duplicate cards and malformed Card fields are outside this exercise; additional validation for them is not required.

<details>
<summary>Original bite description</summary>

In this bite you will implement a `BridgeHand` class representing a collection of 13 playing cards randomly chosen from a 52-card [French deck](https://en.wikipedia.org/wiki/French_playing_cards).

Each card features a suit (spades, hearts, diamonds or clubs) and a rank

(Ace, King, Queen, Jack and then 10 to 2). Both suits and ranks are ordered as

indicated. Data structures for `Suit`, `Rank`, and `Card` have been provided to you.

### Methods

The `__init__` constructor for your class should expect a sequence of `Card` objects. Attempts to use non-sequential types should raise a `TypeError` exception, and sequences containing values of types other than `Card` - or holding fewer or more than 13 elements - should raise `ValueError`.

Your class will also need to implement a `__str__` method returning a textual representation of the hand, sorted by suit and rank, eg: **S:AK32 H:QJT4 D:9654 C:3**. Note that the **10** rank should be represented as a capital **T**.

Ensure that spades, hearts, diamonds and clubs follow each other in that order, skipping over voids (eg, no cards in that suit).

### Properties

Additionally, your class must implement the following read-only properties:

 - `hcp`: high card points. Count 4 points for each Ace, 3 for each King, 2 for each Queen and 1 for each Jack.

 - `doubletons`: number of suits containing only two cards.

 - `singletons`: number of suits containing just one card.

 - `voids`: number of suits containing zero cards (that is, no cards in that suit).

 - `ssp`: short suit points. Count 1 point for each doubleton, 2 for each singleton, and 3 for each void.

 - `total_points`: sum of HCP and SSP.

 - `ltc`: losing trick count. Considering only the top three cards in each suit, LTC is determined by examining each suit and assuming that an Ace will never be a loser, nor will a King in a 2+ card suit, nor a Queen in a 3+ card suit; accordingly:

  - a void = 0 losing tricks.

  - a singleton other than an A = 1 losing trick.

  - a doubleton AK = 0; Ax or Kx = 1; Qx or xx = 2 losing tricks.

  - a three card suit AKQ = 0; AKx, AQx or KQx = 1 losing trick.

  - a three card suit Axx, Kxx or Qxx = 2; xxx = 3 losing tricks.

### Examples

S:AK8 H:JT94 D:A2 C:KQ74  hcp=17, doubletons=1, singletons=0, voids=0, ssp=1, total points=18, ltc=6
S:9 H:KJT94 D:432 C:AJ742  hcp=9, doubletons=0, singletons=1, voids=0, ssp=2, total points=11, ltc=8
H:AKQJT94 D:4 C:KQJ72  hcp=16, doubletons=0, singletons=1, voids=1, ssp=5, total points=21, ltc=2

---

Hope you will enjoy this bite, and perhaps be inspired to learn more about Bridge, easily the finest card game ever created!

</details>

**Notes for this version:** The second example hand in the description has 14 cards (`H:KJT94`). The tests use `S:9 H:KJT9 D:432 C:AJ742`, which has 13 cards and the same values.

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `bridgehand`. **Run** checks the first three tests. **Submit** runs all
50. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
