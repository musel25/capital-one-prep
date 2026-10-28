# 06. Capture stdout

Implement `get_len_help_text(builtin)`. Accept only `types.BuiltinFunctionType`
objects, such as `len`, `max`, `pow`, or `[].append`. Raise `ValueError` for other
objects, including classes and ordinary Python functions.

Call `help(builtin)`. Capture its standard output and return the number of
characters. Leave standard output restored after the call, including when
`help` raises an exception. Propagate that exception.

Example: if `help(len)` writes `"Length help\n"`, return `12` and print nothing.
The actual length can change with the Python version.
