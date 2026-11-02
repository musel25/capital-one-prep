## Learn

`if` runs some lines **only when** something is true.

```python
temperature = int(input())
if temperature > 30:
    print("Drink water!")
print("Have a nice day")
```

- The line after `if` ends with `:`.
- The lines inside the `if` start with 4 spaces.
- `print("Have a nice day")` has no spaces, so it always runs.

Compare signs: `>` bigger, `<` smaller, `>=` bigger or equal, `<=` smaller or equal.

## Your task

Read a number. If it is **bigger than 100**, show `Big number!`.
Then always show `Done`.

| Input | Your program shows |
| --- | --- |
| `150` | `Big number!` and then `Done` |
| `5` | `Done` |
| `100` | `Done` (100 is not bigger than 100) |
