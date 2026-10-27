"""Bite: Write a context manager. Original free template and tests, plus added tests."""
import json
from pathlib import Path

_PAGE = json.loads((Path(__file__).parents[1] / "source-pages.json").read_text())[13]

SPEC = {
    "title": "Write a context manager",
    "module": "account",
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
''',
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
