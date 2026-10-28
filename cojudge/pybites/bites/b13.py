"""Bite: Enrich a class with dunder methods (recreated tests and template)."""

SPEC = {
    "title": "Enrich a class with dunder methods",
    "module": "account",
    "contract": "Names are strings, including an empty string. start_balance is an int, defaults to zero, "
                "and can be negative. Add and subtract accept exact int values, including zero and negative values. "
                "Reject bool and all other amount types with TypeError before changing the account. "
                "Each operation appends one signed transaction. No return value is required. "
                "Balance is the starting balance plus all transactions. Length counts transactions. "
                "Iteration and integer indexing use transaction order, including negative indices and IndexError "
                "outside the list. Compare Account instances by balance only. The string format is 'NAME account - balance: INT'. "
                "Other constructor types, comparison types, and index types are outside this exercise.",
    "template": '''class Account:

    def __init__(self, name, start_balance=0):
        self.name = name
        self.start_balance = start_balance
        self._transactions = []

    @property
    def balance(self):
        return self.start_balance + sum(self._transactions)

    # add dunder methods below
''',
    "tests": '''import pytest

from account import Account


@pytest.fixture()
def bob():
    account = Account('bob', 10)
    account + 5
    account - 3
    account + 20
    return account


@pytest.fixture()
def tim():
    return Account('tim', 25)


def test_balance(bob, tim):
    assert bob.balance == 32
    assert tim.balance == 25


def test_len(bob, tim):
    assert len(bob) == 3
    assert len(tim) == 0


def test_comparison(bob, tim):
    assert bob > tim
    assert tim < bob
    assert bob >= tim
    assert tim <= bob
    assert not bob == tim
    tim + 7
    assert bob == tim
    assert bob >= tim and bob <= tim


def test_indexing(bob):
    assert bob[0] == 5
    assert bob[1] == -3
    assert bob[-1] == 20
    with pytest.raises(IndexError):
        bob[3]


def test_iteration(bob, tim):
    assert list(bob) == [5, -3, 20]
    assert list(tim) == []
    assert [t for t in bob if t > 0] == [5, 20]


@pytest.mark.parametrize("bad", ["10", 1.5, [1], None])
def test_add_sub_incompatible_types(tim, bad):
    with pytest.raises(TypeError):
        tim + bad
    with pytest.raises(TypeError):
        tim - bad
    assert tim.balance == 25
    assert len(tim) == 0


def test_str(bob, tim):
    assert str(bob) == 'bob account - balance: 32'
    assert str(tim) == 'tim account - balance: 25'
    tim - 30
    assert str(tim) == 'tim account - balance: -5'


def test_default_empty_account():
    account = Account('')
    assert account.balance == 0
    assert len(account) == 0
    assert list(account) == []
    assert str(account) == ' account - balance: 0'
    with pytest.raises(IndexError):
        account[0]
    with pytest.raises(IndexError):
        account[-1]


def test_zero_and_negative_amounts_are_transactions():
    account = Account('signed', -5)
    account + 0
    account + -3
    account - -8
    assert account.balance == 0
    assert len(account) == 3
    assert list(account) == [0, -3, 8]
    assert list(account) == [0, -3, 8]
    assert account[-3] == 0
    with pytest.raises(IndexError):
        account[-4]


@pytest.mark.parametrize('amount', [True, False])
def test_boolean_amounts_do_not_change_account(amount):
    account = Account('bool')
    with pytest.raises(TypeError):
        account + amount
    with pytest.raises(TypeError):
        account - amount
    assert list(account) == []
    assert account.balance == 0


def test_accounts_have_separate_transactions():
    first, second = Account('first'), Account('second')
    first + 4
    assert second.balance == 0
    assert len(second) == 0
    assert first > second
    second - 1
    assert first.balance == 4
    assert second < first
''',
    "mutations": [
        {"name": 'accept_boolean_amounts', "old": 'if type(amount) is not int:', "new": 'if not isinstance(amount, int):'},
        {"name": 'ignore_zero_transactions', "old": 'self._transactions.append(amount)', "new": 'if amount:\n            self._transactions.append(amount)'},
        {"name": 'subtract_absolute_amount', "old": 'self._transactions.append(-amount)', "new": 'self._transactions.append(-abs(amount))'},
        {"name": 'balance_ignores_start', "old": 'return self.start_balance + sum(self._transactions)', "new": 'return sum(self._transactions)'},
    ],
    "reference": '''from functools import total_ordering


@total_ordering
class Account:

    def __init__(self, name, start_balance=0):
        self.name = name
        self.start_balance = start_balance
        self._transactions = []

    @property
    def balance(self):
        return self.start_balance + sum(self._transactions)

    def __len__(self):
        return len(self._transactions)

    def __eq__(self, other):
        return self.balance == other.balance

    def __lt__(self, other):
        return self.balance < other.balance

    def __getitem__(self, index):
        return self._transactions[index]

    def __iter__(self):
        return iter(self._transactions)

    def _check(self, amount):
        if type(amount) is not int:
            raise TypeError("amount must be an int")

    def __add__(self, amount):
        self._check(amount)
        self._transactions.append(amount)

    def __sub__(self, amount):
        self._check(amount)
        self._transactions.append(-amount)

    def __str__(self):
        return f"{self.name} account - balance: {self.balance}"
''',
}
