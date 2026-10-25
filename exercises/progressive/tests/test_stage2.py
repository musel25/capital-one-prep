from copy import deepcopy
import pytest
from solution import summarize


def test_replay_is_counted_once_even_with_different_key_order():
    first = {'id': 'p1', 'type': 'purchase', 'merchant': 'A', 'amount': 1000}
    replay = {'amount': 1000, 'merchant': 'A', 'type': 'purchase', 'id': 'p1'}
    assert summarize([first, replay, first]) == {'A': 1000}


@pytest.mark.parametrize('field,value', [('amount', 999), ('merchant', 'B')])
def test_conflicting_id_raises_without_mutating_input(field, value):
    first = {'id': 'p1', 'type': 'purchase', 'merchant': 'A', 'amount': 1000}
    changed = dict(first, **{field: value})
    events = [first, changed]
    before = deepcopy(events)
    with pytest.raises(ValueError):
        summarize(events)
    assert events == before
