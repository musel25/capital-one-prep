"""Bite: Evaluate a bridge hand (recreated tests and template)."""

_HEADER = '''from collections import namedtuple
from collections.abc import Sequence
from enum import Enum

Suit = Enum("Suit", list("SHDC"))
Rank = Enum("Rank", list("AKQJT98765432"))
Card = namedtuple("Card", ["suit", "rank"])

HCP = {Rank.A: 4, Rank.K: 3, Rank.Q: 2, Rank.J: 1}
SSP = {2: 1, 1: 2, 0: 3}  # cards in a suit -> short suit points
'''

SPEC = {
    "title": "Evaluate a bridge hand",
    "module": "bridgehand",
    "notes": "The second example hand in the description has 14 cards (`H:KJT94`). The tests use `S:9 H:KJT9 D:432 C:AJ742`, which has 13 cards and the same values.",
    "template": _HEADER + '''

class BridgeHand:
    def __init__(self, cards):
        """
        Process and store the sequence of Card objects passed in input.
        Raise TypeError if not a sequence
        Raise ValueError if any element of the sequence is not an instance
        of Card, or if the number of elements is not 13
        """
        pass

    def __str__(self):
        """
        Return a string representing this hand, in the following format:
        "S:AK3 H:T987 D:KJ98 C:QJ"
        List the suits in SHDC order, and the cards within each suit in
        AKQJT..2 order. Skip suits without cards (voids).
        """
        pass

    @property
    def hcp(self):
        """ Return the number of high card points contained in this hand """
        pass

    @property
    def doubletons(self):
        """ Return the number of doubletons contained in this hand """
        pass

    @property
    def singletons(self):
        """ Return the number of singletons contained in this hand """
        pass

    @property
    def voids(self):
        """ Return the number of voids (missing suits) contained in
            this hand
        """
        pass

    @property
    def ssp(self):
        """ Return the number of short suit points in this hand.
            Doubletons are worth one point, singletons two points,
            voids 3 points
        """
        pass

    @property
    def total_points(self):
        """ Return the total points (hcp and ssp) contained in this hand """
        pass

    @property
    def ltc(self):
        """ Return the losing trick count for this hand - see bite description
            for the procedure
        """
        pass
''',
    "tests": '''import pytest

from bridgehand import BridgeHand, Card, Rank, Suit


def make_hand(text):
    """'S:AK8 H:JT94 D:A2 C:KQ74' -> list of 13 Cards"""
    cards = []
    for part in text.split():
        suit, ranks = part.split(":")
        cards.extend(Card(Suit[suit], Rank[rank]) for rank in ranks)
    return cards


HANDS = [
    # hand, hcp, doubletons, singletons, voids, ssp, total_points, ltc
    ("S:AK8 H:JT94 D:A2 C:KQ74", 17, 1, 0, 0, 1, 18, 6),
    ("S:9 H:KJT9 D:432 C:AJ742", 9, 0, 1, 0, 2, 11, 8),  # the description shows 14 cards here
    ("H:AKQJT94 D:4 C:KQJ72", 16, 0, 1, 1, 5, 21, 2),
    ("S:QJ H:KQ D:AQ7 C:987643", 14, 2, 0, 0, 2, 16, 7),
    ("S:AKQJT98765432", 10, 0, 0, 3, 9, 19, 0),
]


@pytest.mark.parametrize("text, hcp, doubletons, singletons, voids, ssp, total, ltc", HANDS)
def test_evaluation(text, hcp, doubletons, singletons, voids, ssp, total, ltc):
    hand = BridgeHand(make_hand(text))
    assert hand.hcp == hcp
    assert hand.doubletons == doubletons
    assert hand.singletons == singletons
    assert hand.voids == voids
    assert hand.ssp == ssp
    assert hand.total_points == total
    assert hand.ltc == ltc


@pytest.mark.parametrize("text", [h[0] for h in HANDS])
def test_str_is_sorted(text):
    cards = make_hand(text)
    shuffled = cards[::2] + cards[1::2]
    assert str(BridgeHand(shuffled)) == text


def test_tuple_input():
    hand = BridgeHand(tuple(make_hand(HANDS[0][0])))
    assert hand.hcp == 17


@pytest.mark.parametrize("bad", [set(make_hand(HANDS[0][0])), 13, None,
                                 (card for card in make_hand(HANDS[0][0]))])
def test_not_a_sequence(bad):
    with pytest.raises(TypeError):
        BridgeHand(bad)


def test_wrong_number_of_cards():
    cards = make_hand(HANDS[0][0])
    with pytest.raises(ValueError):
        BridgeHand(cards[:12])
    with pytest.raises(ValueError):
        BridgeHand(cards + [Card(Suit.S, Rank["2"])])


def test_not_cards():
    cards = make_hand(HANDS[0][0])
    with pytest.raises(ValueError):
        BridgeHand(cards[:12] + [("S", "A")])
    with pytest.raises(ValueError):
        BridgeHand("SAKQJT98765432"[:13])


def test_read_only_properties():
    hand = BridgeHand(make_hand(HANDS[0][0]))
    for name in ("hcp", "doubletons", "singletons", "voids", "ssp", "total_points", "ltc"):
        assert isinstance(BridgeHand.__dict__[name], property)
        with pytest.raises(AttributeError):
            setattr(hand, name, 0)
''',
    "reference": _HEADER + '''

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
''',
}
