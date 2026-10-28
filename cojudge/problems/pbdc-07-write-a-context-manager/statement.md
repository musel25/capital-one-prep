# 07. Write a context manager

Complete the supplied `Account` class as a context manager. Amounts are integers.
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
