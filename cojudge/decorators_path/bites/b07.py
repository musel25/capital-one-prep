"""Original free Account exercise with the existing course's added guards."""
from cojudge.pybites.bites.b14 import SPEC as BASE_SPEC

SPEC = {
    **BASE_SPEC,
    "template": BASE_SPEC["template"].replace("\r\n", "\n"),
    "tests": BASE_SPEC["tests"].replace("\r\n", "\n"),
    "statement": """Complete the supplied `Account` class as a context manager. Amounts are integers.
`with account as acc` must return the same account.

At block exit, check the final balance. If it is negative, discard all
transactions added in that block. Keep earlier transactions. Otherwise, keep
the whole block, even if the balance was temporarily negative.

Apply this rule when the block raises an exception too. Let the exception
propagate. A balance of zero is allowed. Outside a block, a negative balance
is allowed. Support repeated blocks and separate accounts. Nested blocks and
direct changes to account internals are outside this exercise.

Example:
```python
account = Account()
account + 5
with account as acc:
    acc - 8
assert account.balance == 5
```
""",
    "reference": BASE_SPEC["reference"].replace("\r\n", "\n"),
    "examples": [{"input": "account + 5; with account as acc: acc - 8", "output": "account.balance == 5",
                  "explanation": "The final negative balance discards the block's withdrawal."}],
    "notes": "The template and original tests come from the free bite. Additional tests check the stated exit rules.",
    "original": True,
}
