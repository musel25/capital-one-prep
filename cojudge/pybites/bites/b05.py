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

SPEC["contract"] = (
    "Each call receives one finite int or float score, excluding bool. Scores may "
    "be negative or zero. Return the largest score received by this instance, "
    "including the current call. The first score is the initial record. Equal "
    "scores leave the record unchanged. Instances keep independent records. "
    "Other types, NaN and infinities are outside the contract; no validation "
    "is required for them."
)
SPEC["tests"] += '''


def test_zero_record_is_not_replaced_by_a_negative_score():
    record = RecordScore()
    assert record(0) == 0
    assert record(-1) == 0
    assert record(0) == 0


def test_fractional_scores_and_ties():
    record = RecordScore()
    assert record(-0.5) == -0.5
    assert record(0.25) == 0.25
    assert record(0.125) == 0.25
    assert record(0.25) == 0.25
    assert record(1) == 1


def test_arbitrarily_large_integer_scores():
    record = RecordScore()
    assert record(-(10 ** 100)) == -(10 ** 100)
    assert record(10 ** 100) == 10 ** 100
    assert record(1) == 10 ** 100
'''
SPEC["mutations"] = [
    {"name": "initial record is zero", "old": "self._max = None", "new": "self._max = 0"},
    {"name": "treat zero as uninitialized", "old": "self._max is None", "new": "not self._max"},
    {"name": "keep minimum score", "old": "score > self._max", "new": "score < self._max"},
    {"name": "truncate fractional scores", "old": "self._max = score", "new": "self._max = int(score)"},
]
