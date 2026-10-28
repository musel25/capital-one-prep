Write a [context manager](https://docs.python.org/3/reference/datamodel.html#context-managers) to roll back a transaction on the given `Account` class.

There are two *special (aka *dunder*) methods* you need to define to create a context manager (there is also a convenient decorator - see Write a performance monitoring context manager).

The purpose of the context manager is to roll back any transaction that will make the balance go below 0 (debt != cool).

The rollback should follow [the *Unit of Work *pattern](https://www.cosmicpython.com/book/chapter_06_uow.html), meaning all transactions within a `with` block should be either fully applied or fully discarded, just like a database transaction.

The rest of the class is already defined so you can focus on the context manager part.

See the tests for more detail. Good luck and keep calm and code in Python!

**Constraints:**

- Use integer amounts and non-nested context blocks. Check the final balance on every block exit; keep exceptions visible.
