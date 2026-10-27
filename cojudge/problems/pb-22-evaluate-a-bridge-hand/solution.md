## Reference solution

```python
from collections import namedtuple
from collections.abc import Sequence
from enum import Enum

Suit = Enum("Suit", list("SHDC"))
Rank = Enum("Rank", list("AKQJT98765432"))
Card = namedtuple("Card", ["suit", "rank"])

HCP = {Rank.A: 4, Rank.K: 3, Rank.Q: 2, Rank.J: 1}
SSP = {2: 1, 1: 2, 0: 3}  # cards in a suit -> short suit points


class BridgeHand:
    def __init__(self, cards):
        if not isinstance(cards, Sequence):
            raise TypeError("cards must be a sequence")
        if len(cards) != 13 or not all(isinstance(card, Card) for card in cards):
            raise ValueError("a hand has 13 Card objects")
        self._suits = {suit: sorted((c.rank for c in cards if c.suit == suit), key=lambda r: r.value)
                       for suit in Suit}

    def __str__(self):
        return " ".join(f"{suit.name}:{''.join(rank.name for rank in ranks)}"
                        for suit, ranks in self._suits.items() if ranks)

    def _count(self, length):
        return sum(len(ranks) == length for ranks in self._suits.values())

    @property
    def hcp(self):
        return sum(HCP.get(rank, 0) for ranks in self._suits.values() for rank in ranks)

    @property
    def doubletons(self):
        return self._count(2)

    @property
    def singletons(self):
        return self._count(1)

    @property
    def voids(self):
        return self._count(0)

    @property
    def ssp(self):
        return sum(SSP[n] * self._count(n) for n in SSP)

    @property
    def total_points(self):
        return self.hcp + self.ssp

    @property
    def ltc(self):
        losers = 0
        for ranks in self._suits.values():
            considered = min(len(ranks), 3)
            honors = [Rank.A, Rank.K, Rank.Q][:considered]
            losers += considered - sum(rank in ranks for rank in honors)
        return losers
```
