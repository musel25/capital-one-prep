"""Bite: Keep state in a class + make its instance callable (recreated tests and template)."""

SPEC = {
    "title": "Keep state in a class + make its instance callable",
    "module": "record",
    "template": '''class RecordScore():
    """Class to track a game's maximum score"""
''',
    "tests": '''from record import RecordScore


def test_record_score():
    record = RecordScore()
    assert record(10) == 10
    assert record(9) == 10
    assert record(11) == 11
    assert record(5) == 11


def test_negative_numbers():
    record = RecordScore()
    assert record(-5) == -5
    assert record(-10) == -5
    assert record(-2) == -2


def test_first_score_is_the_record():
    assert RecordScore()(-100) == -100
    assert RecordScore()(0) == 0


def test_instances_keep_their_own_record():
    one, two = RecordScore(), RecordScore()
    assert one(50) == 50
    assert two(3) == 3
    assert one(4) == 50
    assert two(2) == 3


def test_instance_is_callable():
    record = RecordScore()
    assert callable(record)
    assert "__call__" in RecordScore.__dict__
''',
    "reference": '''class RecordScore():
    """Class to track a game's maximum score"""

    def __init__(self):
        self._max = None

    def __call__(self, score):
        if self._max is None or score > self._max:
            self._max = score
        return self._max
''',
}
