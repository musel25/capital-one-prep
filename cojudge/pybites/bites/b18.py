"""Bite: Write a score property (recreated tests and template)."""

SPEC = {
    "title": "Write a score property",
    "module": "ninjabelt",
    "template": '''BELTS = {10: 'white', 50: 'yellow', 100: 'orange', 175: 'green',
         250: 'blue', 400: 'brown', 600: 'black', 800: 'paneled',
         1000: 'red'}


class NinjaBelt:

    def __init__(self, score=0):
        self._score = score
        self._last_earned_belt = None

    def _get_belt(self, new_score):
        """Might be a useful helper"""
        pass

    def _get_score(self):
        pass

    def _set_score(self, new_score):
        pass

    score = property(_get_score, _set_score)
''',
    "tests": '''import pytest

from ninjabelt import NinjaBelt


def test_initial_state():
    ninja = NinjaBelt()
    assert ninja.score == 0
    assert ninja._last_earned_belt is None


def test_only_integers():
    ninja = NinjaBelt()
    for bad in ('a', 1.5, [], None):
        with pytest.raises(ValueError):
            ninja.score = bad
    assert ninja.score == 0


def test_score_cannot_go_down():
    ninja = NinjaBelt()
    ninja.score = 20
    with pytest.raises(ValueError):
        ninja.score = 10
    assert ninja.score == 20


def test_new_scores_and_belts(capsys):
    ninja = NinjaBelt()
    ninja.score = 10
    assert capsys.readouterr().out.strip() == (
        'Congrats, you earned 10 points obtaining the PyBites Ninja White Belt')
    assert ninja._last_earned_belt == 'white'
    ninja.score = 49
    assert capsys.readouterr().out.strip() == 'Set new score to 49'
    assert ninja._last_earned_belt == 'white'
    ninja.score = 50
    assert capsys.readouterr().out.strip() == (
        'Congrats, you earned 50 points obtaining the PyBites Ninja Yellow Belt')
    assert ninja._last_earned_belt == 'yellow'
    ninja.score = 99
    assert capsys.readouterr().out.strip() == 'Set new score to 99'
    assert ninja.score == 99


def test_skipping_belts_gives_the_highest(capsys):
    ninja = NinjaBelt()
    ninja.score = 260
    assert capsys.readouterr().out.strip() == (
        'Congrats, you earned 260 points obtaining the PyBites Ninja Blue Belt')
    assert ninja._last_earned_belt == 'blue'
    ninja.score = 1000
    assert capsys.readouterr().out.strip() == (
        'Congrats, you earned 1000 points obtaining the PyBites Ninja Red Belt')


def test_below_first_belt(capsys):
    ninja = NinjaBelt()
    ninja.score = 9
    assert capsys.readouterr().out.strip() == 'Set new score to 9'
    assert ninja._last_earned_belt is None


def test_titlecased_belt_name(capsys):
    ninja = NinjaBelt(700)
    ninja.score = 800
    assert capsys.readouterr().out.strip() == (
        'Congrats, you earned 800 points obtaining the PyBites Ninja Paneled Belt')


def test_score_is_a_property():
    assert isinstance(NinjaBelt.__dict__['score'], property)
''',
    "reference": '''BELTS = {10: 'white', 50: 'yellow', 100: 'orange', 175: 'green',
         250: 'blue', 400: 'brown', 600: 'black', 800: 'paneled',
         1000: 'red'}


class NinjaBelt:

    def __init__(self, score=0):
        self._score = score
        self._last_earned_belt = None

    def _get_belt(self, new_score):
        """Might be a useful helper"""
        earned = [belt for points, belt in sorted(BELTS.items()) if new_score >= points]
        return earned[-1] if earned else None

    def _get_score(self):
        return self._score

    def _set_score(self, new_score):
        if type(new_score) is not int:
            raise ValueError("Score takes an int")
        if new_score < self._score:
            raise ValueError("Cannot lower score")
        self._score = new_score
        belt = self._get_belt(new_score)
        if belt is not None and belt != self._last_earned_belt:
            self._last_earned_belt = belt
            print(f"Congrats, you earned {new_score} points obtaining the PyBites Ninja {belt.title()} Belt")
        else:
            print(f"Set new score to {new_score}")

    score = property(_get_score, _set_score)
''',
}
