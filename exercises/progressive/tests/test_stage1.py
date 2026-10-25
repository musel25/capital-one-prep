from copy import deepcopy
from solution import summarize


def test_empty_and_grouped_purchases_preserve_input():
    events = [
        {'id': 'p1', 'type': 'purchase', 'merchant': 'A', 'amount': 1000},
        {'id': 'p2', 'type': 'purchase', 'merchant': 'B', 'amount': 500},
        {'id': 'p3', 'type': 'purchase', 'merchant': 'A', 'amount': 200},
    ]
    before = deepcopy(events)
    assert summarize(events) == {'A': 1200, 'B': 500}
    assert events == before
    assert summarize([]) == {}
    assert summarize(events) == {'A': 1200, 'B': 500}
