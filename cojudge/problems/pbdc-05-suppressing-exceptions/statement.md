# 05. Suppressing exceptions

Implement `sum_numbers(numbers)`. Use `contextlib.suppress` to skip values that raise
`TypeError` or `ValueError` during `int(value)`. Add each successful conversion.
Let other exceptions propagate. Accept any iterable without changing it.
An empty iterable returns `0`. Floats truncate toward zero.

Example: `sum_numbers(["10", None, "bad", -2.9, "+3"])` returns `11`.
