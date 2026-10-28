# 04. Write a numbers validation decorator

Implement `validate_int_args(func)`.

Check each positional argument from left to right before you call the wrapped
function. Raise `TypeError` for a non-integer. Raise `ValueError` for a negative
integer. Zero is valid. In this course, `bool` is not a valid integer.

Do not validate keyword arguments. Forward them unchanged. Call the wrapped
function once after successful validation. Return its result. Preserve its
name, docstring and annotations. Propagate its exceptions.

```python
@validate_int_args
def total(*values, label='sum'):
    return label, sum(values)

total(0, 2, 3, label='count')  # ('count', 5)
total(-1)                    # raises ValueError
total(True)                  # raises TypeError
```
