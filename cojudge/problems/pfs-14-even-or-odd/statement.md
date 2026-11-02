## Learn

`else` runs when the `if` is **not** true. Exactly one of the two parts runs.

`%` gives the remainder after dividing. `7 % 2` is `1`. `8 % 2` is `0`.
Two equal signs `==` ask "is it equal?". One `=` puts a value in a variable.

```python
n = int(input())
if n % 3 == 0:
    print("fits in groups of 3")
else:
    print("does not fit")
```

## Your task

Read a whole number. Show `even` or `odd` after it.

| Input | Your program shows |
| --- | --- |
| `4` | `4 is even` |
| `7` | `7 is odd` |
| `0` | `0 is even` |
