"""Bite: No promo twice, keep state in a class (recreated tests and template)."""

SPEC = {
    "title": "No promo twice, keep state in a class",
    "module": "promo",
    "template": '''import random

BITES = {6: 'PyBites Die Hard',
         7: 'Parsing dates from logs',
         9: 'Palindromes',
         10: 'Practice exceptions',
         11: 'Enrich a class with dunder methods',
         12: 'Write a user validation function',
         13: 'Convert dict in namedtuple/json',
         14: 'Generate a table of n sequences',
         15: 'Enumerate 2 sequences',
         16: 'Special PyBites date generator',
         17: 'Form teams from a group of friends',
         18: 'Find the most common word',
         19: 'Write a simple property',
         20: 'Write a context manager',
         21: 'Query a nested data structure'}
BITES_DONE = {6, 10, 16, 18, 21}


class NoBitesAvailable(Exception):
    pass


class Promo:

    def __init__(self, bites=None, bites_done=None):
        if bites is None:
            bites = BITES
        if bites_done is None:
            bites_done = BITES_DONE
        self.all_bites = bites.copy()
        self.bites_done = bites_done.copy()

    def _pick_random_bite(self):
        pass

    def new_bite(self):
        pass
''',
    "tests": '''import random

import pytest

from promo import BITES, BITES_DONE, NoBitesAvailable, Promo


@pytest.fixture()
def promo():
    return Promo()


def test_promo_has_state(promo):
    assert promo.all_bites == BITES
    assert promo.bites_done == BITES_DONE


def test_pick_random_bite_returns_an_available_bite(promo):
    for _ in range(20):
        bite = promo._pick_random_bite()
        assert bite in BITES
        assert bite not in BITES_DONE


def test_pick_random_bite_does_not_change_state(promo):
    promo._pick_random_bite()
    promo._pick_random_bite()
    assert promo.bites_done == BITES_DONE


def test_new_bite_updates_bites_done(promo):
    bite = promo.new_bite()
    assert bite in BITES
    assert bite not in BITES_DONE
    assert promo.bites_done == BITES_DONE | {bite}


def test_no_bite_twice_then_exception(promo):
    available = set(BITES) - BITES_DONE
    picked = [promo.new_bite() for _ in range(len(available))]
    assert sorted(picked) == sorted(available)
    with pytest.raises(NoBitesAvailable):
        promo.new_bite()
    with pytest.raises(NoBitesAvailable):
        promo._pick_random_bite()


def test_uses_random():
    first_picks = set()
    for seed in range(30):
        random.seed(seed)
        first_picks.add(Promo().new_bite())
    assert len(first_picks) > 1


def test_instances_and_constants_are_independent():
    one, two = Promo(), Promo()
    bite = one.new_bite()
    assert bite not in two.bites_done
    assert bite not in BITES_DONE


def test_custom_bites():
    promo = Promo({1: 'a', 2: 'b'}, {1})
    assert promo.new_bite() == 2
    with pytest.raises(NoBitesAvailable):
        promo.new_bite()


def test_custom_exception():
    assert issubclass(NoBitesAvailable, Exception)
''',
    "reference": '''import random

BITES = {6: 'PyBites Die Hard',
         7: 'Parsing dates from logs',
         9: 'Palindromes',
         10: 'Practice exceptions',
         11: 'Enrich a class with dunder methods',
         12: 'Write a user validation function',
         13: 'Convert dict in namedtuple/json',
         14: 'Generate a table of n sequences',
         15: 'Enumerate 2 sequences',
         16: 'Special PyBites date generator',
         17: 'Form teams from a group of friends',
         18: 'Find the most common word',
         19: 'Write a simple property',
         20: 'Write a context manager',
         21: 'Query a nested data structure'}
BITES_DONE = {6, 10, 16, 18, 21}


class NoBitesAvailable(Exception):
    pass


class Promo:

    def __init__(self, bites=None, bites_done=None):
        if bites is None:
            bites = BITES
        if bites_done is None:
            bites_done = BITES_DONE
        self.all_bites = bites.copy()
        self.bites_done = bites_done.copy()

    def _pick_random_bite(self):
        available = sorted(set(self.all_bites) - self.bites_done)
        if not available:
            raise NoBitesAvailable("all Bites have been done")
        return random.choice(available)

    def new_bite(self):
        bite = self._pick_random_bite()
        self.bites_done.add(bite)
        return bite
''',
}

SPEC["contract"] = (
    "bites is a dict from integer IDs to title strings. bites_done is a set of "
    "IDs from that dict. Either argument can be None to use its supplied default. "
    "Empty containers are valid and must not select defaults. Copy the inputs. "
    "_pick_random_bite returns an available ID without changing state. new_bite "
    "uses that helper, adds the ID to bites_done and returns it. Both methods raise "
    "NoBitesAvailable when no IDs remain. IDs cannot repeat. No exact random order "
    "is required. Other types and done IDs outside the catalog are outside the "
    "contract; no validation is required for them."
)
SPEC["tests"] += '''


@pytest.mark.parametrize('bites, done', [({}, set()), ({1: 'one'}, {1})])
def test_initially_empty_availability(bites, done):
    promo = Promo(bites, done)
    for method in (promo._pick_random_bite, promo.new_bite):
        with pytest.raises(NoBitesAvailable):
            method()
    assert promo.all_bites == bites
    assert promo.bites_done == done


def test_empty_done_set_is_not_the_default():
    promo = Promo({6: 'six'}, set())
    assert promo._pick_random_bite() == 6
    assert promo.bites_done == set()
    assert promo.new_bite() == 6


def test_custom_input_containers_are_copied():
    bites, done = {1: 'one', 2: 'two'}, {1}
    promo = Promo(bites, done)
    bites[3] = 'three'
    done.add(2)
    assert promo.all_bites == {1: 'one', 2: 'two'}
    assert promo.bites_done == {1}
    assert promo.new_bite() == 2
    assert bites == {1: 'one', 2: 'two', 3: 'three'}


def test_new_bite_uses_the_selection_helper(monkeypatch):
    promo = Promo({1: 'one', 2: 'two'}, set())
    monkeypatch.setattr(promo, '_pick_random_bite', lambda: 2)
    assert promo.new_bite() == 2
    assert promo.bites_done == {2}
'''
SPEC["mutations"] = [
    {"name": "empty catalog selects defaults", "old": "if bites is None:", "new": "if not bites:"},
    {"name": "empty done set selects defaults", "old": "if bites_done is None:", "new": "if not bites_done:"},
    {"name": "retain caller catalog", "old": "self.all_bites = bites.copy()", "new": "self.all_bites = bites"},
    {"name": "retain caller done set", "old": "self.bites_done = bites_done.copy()", "new": "self.bites_done = bites_done"},
    {"name": "forget selected ID", "old": "self.bites_done.add(bite)", "new": "pass"},
    {"name": "skip selection helper", "old": "bite = self._pick_random_bite()", "new": "bite = min(set(self.all_bites) - self.bites_done)"},
]
