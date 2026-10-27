## Approach

`__init__` validates count, uniqueness, and each card, then stores a private copy.
One helper, `_ranks(suit)`, sorts a suit high to low, and every property builds on it or on
another property, so each rule appears once. `opening` checks its rules in the stated order;
`max` over `"SHDC"` returns the first suit among equal lengths. The opening rules are a
simplified practice system, not a complete bidding system.

## Reference classes

```python
SUITS = "SHDC"
RANKS = "23456789TJQKA"
POINTS = {"A": 4, "K": 3, "Q": 2, "J": 1}
BALANCED = {"4-3-3-3", "4-4-3-2", "5-3-3-2"}


class Hand:
    def __init__(self, cards: list[str]):
        if len(cards) != 13 or len(set(cards)) != 13:
            raise ValueError("a hand has 13 different cards")
        for card in cards:
            if not isinstance(card, str) or len(card) != 2 or card[0] not in SUITS or card[1] not in RANKS:
                raise ValueError(f"invalid card: {card!r}")
        self._cards = list(cards)

    def _ranks(self, suit: str) -> list[str]:
        return sorted((card[1] for card in self._cards if card[0] == suit), key=RANKS.index, reverse=True)

    @property
    def hcp(self) -> int:
        return sum(POINTS.get(card[1], 0) for card in self._cards)

    @property
    def lengths(self) -> dict[str, int]:
        return {suit: len(self._ranks(suit)) for suit in SUITS}

    @property
    def shape(self) -> str:
        return "-".join(str(n) for n in sorted(self.lengths.values(), reverse=True))

    @property
    def balanced(self) -> bool:
        return self.shape in BALANCED

    @property
    def losers(self) -> int:
        total = 0
        for suit in SUITS:
            ranks = self._ranks(suit)
            considered = min(len(ranks), 3)
            total += considered - sum(1 for honor in "AKQ"[:considered] if honor in ranks)
        return total

    def __str__(self) -> str:
        return " | ".join(f"{suit}: {''.join(self._ranks(suit)) or '-'}" for suit in SUITS)

    def opening(self) -> str:
        points = self.hcp
        if points >= 22:
            return "2C"
        if self.balanced and 15 <= points <= 17:
            return "1NT"
        if self.balanced and 20 <= points <= 21:
            return "2NT"
        if points >= 12:
            lengths = self.lengths
            return "1" + max(SUITS, key=lambda suit: lengths[suit])
        return "pass"
```
