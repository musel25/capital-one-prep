"""Bite: Write a context manager. Original free template and tests, plus added tests."""
import json
from pathlib import Path

_PAGE = json.loads((Path(__file__).parents[1] / "source-pages.json").read_text())[13]

SPEC = {
    "title": "Write a context manager",
    "module": "account",
    "contract": "Use integer amounts with the supplied Account class. No new amount validation is required. "
                "A with block returns the same account. At block exit, check the final balance. "
                "If it is negative, discard every transaction added in that block and keep all earlier transactions. "
                "Otherwise keep the whole block, including when its balance was temporarily negative. "
                "Apply this rule on normal exit and on an exception. Never suppress exceptions. "
                "Zero is allowed. Outside a block, the balance can be negative. "
                "Use single, non-nested blocks; repeated blocks and separate accounts are supported. "
                "Nested blocks and direct changes to account internals are outside this exercise.",
    "original": True,
    "template": _PAGE["template"],
    "tests": _PAGE["tests"].rstrip() + '''


# Added for this course.

def test_enter_returns_the_account(account):
    with account as acc:
        assert acc is account


def test_block_that_stays_positive_is_kept(account):
    account + 5
    with account as acc:
        acc - 5
    assert account.balance == 0


def test_rollback_only_undoes_the_block(account):
    account + 20
    with account as acc:
        acc - 5
    with account as acc:
        acc + 1
        acc - 100
        acc + 50
    assert account.balance == 15


def test_exception_in_block_is_not_hidden(account):
    account + 1
    with pytest.raises(ZeroDivisionError):
        with account as acc:
            acc - 1
            1 / 0


def test_empty_block_keeps_balance(account):
    account + 7
    with account:
        pass
    assert account.balance == 7


def test_only_final_balance_triggers_rollback(account):
    account + 5
    with account as acc:
        acc - 10
        acc + 6
    assert account.balance == 1


@pytest.mark.parametrize('withdrawal, expected', [(3, 2), (8, 5)])
def test_exception_uses_final_balance_rule(account, withdrawal, expected):
    account + 5
    with pytest.raises(ValueError):
        with account as acc:
            acc - withdrawal
            raise ValueError('stop')
    assert account.balance == expected


def test_two_accounts_do_not_share_rollback_state():
    first, second = Account(), Account()
    first + 5
    second + 10
    with first as acc:
        acc - 6
    with second as acc:
        acc - 3
    assert first.balance == 5
    assert second.balance == 7
''',
    "mutations": [
        {"name": 'rollback_zero_balance', "old": 'if self.balance < 0:', "new": 'if self.balance <= 0:'},
        {"name": 'rollback_every_exception', "old": 'if self.balance < 0:', "new": 'if exc_type is not None or self.balance < 0:'},
        {"name": 'clear_previous_transactions', "old": 'del self._transactions[self._snapshot:]', "new": 'self._transactions.clear()'},
        {"name": 'suppress_exceptions', "old": 'return False', "new": 'return True'},
    ],
    "reference": _PAGE["template"].split("    # add 2 dunder")[0].rstrip() + '''

    def __enter__(self):
        self._snapshot = len(self._transactions)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.balance < 0:
            del self._transactions[self._snapshot:]
        return False
''',
}
