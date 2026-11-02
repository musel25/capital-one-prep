## Learn

You can compare text with `==`. The text must be **exactly** the same.
`"Cat" == "cat"` is false, because of the big C.

```python
answer = input()
if answer == "yes":
    print("Great!")
else:
    print("Oh no")
```

## Your task

The secret password is `banana`. Read a word.
Show `Welcome!` if it is the password. Otherwise show `Wrong password`.

| Input | Your program shows |
| --- | --- |
| `banana` | `Welcome!` |
| `apple` | `Wrong password` |
| `Banana` | `Wrong password` |
