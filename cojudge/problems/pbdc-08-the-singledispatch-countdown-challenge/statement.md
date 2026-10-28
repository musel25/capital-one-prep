# 08. The singledispatch countdown challenge

Implement `count_down(value)` with `functools.singledispatch`. Print its rendered
text. Remove the final character and repeat until the text is empty. Return `None`.

Use these local rules:
- Accept nonnegative integers, finite nonnegative floats, and strings.
- For a list or tuple, join the rendered items in their input order.
- For a dictionary, join its keys in insertion order. Ignore its values.
- For a set, sort its items by `str` before joining them.
- Container items must be nonnegative integers or strings. Reject nested containers.
- Raise `ValueError` for unsupported types, booleans, or invalid values before printing.
- Do not change the input. Empty text and empty containers print nothing.

Example: `count_down(12.34)` prints:
```text
12.34
12.3
12.
12
1
```
`count_down([12, "ab"])` starts with `12ab`, then prints `12a`, `12`, and `1`.
