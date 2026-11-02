## Learn

`or` is true when **at least one** side is true.

```python
if fruit == "apple" or fruit == "pear":
    print("It grows on a tree")
```

Write the full comparison on both sides of `or`.
`fruit == "apple" or "pear"` does not work as you expect.

## Your task

Read a day of the week. It starts with a big letter, like `Monday`.

| Input | Your program shows |
| --- | --- |
| `Saturday` | `Weekend! Sleep in.` |
| `Sunday` | `Weekend! Sleep in.` |
| any other day | `School day. Wake up!` |
