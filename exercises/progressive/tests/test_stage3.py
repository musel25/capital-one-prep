from copy import deepcopy
import pytest
from solution import summarize

P = {'id': 'p1', 'type': 'purchase', 'merchant': 'A', 'amount': 1000}


def test_partial_refunds_exact_limit_and_replay_preserve_zero_merchant():
    refund = {'id': 'r1', 'type': 'refund', 'purchase_id': 'p1', 'amount': 300}
    rest = {'id': 'r2', 'type': 'refund', 'purchase_id': 'p1', 'amount': 700}
    events = [dict(P), refund, rest, dict(refund)]
    before = deepcopy(events)
    assert summarize(events) == {'A': 0}
    assert events == before


@pytest.mark.parametrize('events', [
    [P, {'id': 'r', 'type': 'refund', 'purchase_id': 'p1', 'amount': 1001}],
    [P, {'id': 'r1', 'type': 'refund', 'purchase_id': 'p1', 'amount': 600},
        {'id': 'r2', 'type': 'refund', 'purchase_id': 'p1', 'amount': 401}],
    [{'id': 'r', 'type': 'refund', 'purchase_id': 'p1', 'amount': 1}, P],
    [P, {'id': 'r', 'type': 'refund', 'purchase_id': 'missing', 'amount': 1}],
    [P, {'id': 'p1', 'type': 'refund', 'purchase_id': 'p1', 'amount': 1}],
])
def test_invalid_refund_or_reused_id_raises_without_mutation(events):
    before = deepcopy(events)
    with pytest.raises(ValueError):
        summarize(events)
    assert events == before
