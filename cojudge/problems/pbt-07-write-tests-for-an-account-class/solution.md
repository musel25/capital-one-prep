## Reference tests

```python
import pytest
from account import Account

def test_initial_and_representation():
    default = Account('Ada')
    assert default.balance == 0
    assert len(default) == 0
    account = Account('Bob', 10)
    assert account.owner == 'Bob'
    assert account.amount == 10
    assert str(account) == 'Account of Bob with starting amount: 10'
    assert repr(account) == "Account('Bob', 10)"

def test_transactions():
    account = Account('Ada', 10)
    account.add_transaction(5)
    account.add_transaction(-3)
    account.add_transaction(0)
    assert account.balance == 12
    assert len(account) == 3
    assert list(account) == [5, -3, 0]
    assert account[-1] == 0
    assert account[:2] == [5, -3]
    with pytest.raises(IndexError):
        _ = account[3]
    assert Account('Other').balance == 0

@pytest.mark.parametrize('value', [True, 1.5, '2', None])
def test_invalid_amounts(value):
    with pytest.raises(TypeError, match='integer'):
        Account('Ada', value)
    with pytest.raises(TypeError, match='integer'):
        Account('Ada').add_transaction(value)

def test_comparisons():
    first, second = Account('A', 3), Account('B', 8)
    first.add_transaction(5)
    assert first == second
    assert not first < second
    second.add_transaction(1)
    assert first < second
    assert first != object()
    with pytest.raises(TypeError):
        _ = first < object()
```
