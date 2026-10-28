# 10. Manipulate string decorator

Write `strip_range(start, end)` in `string_decorator`.

Decorate a function that returns a string. Replace the characters at the selected
indices with periods. Use the indices in Python's `range(start, end)`: include
`start` and exclude `end`. Ignore indices beyond the string. Keep the original
length and all other characters. Both bounds are nonnegative integers. An empty
or reversed range changes nothing. An empty string stays empty. Treat Unicode
characters as ordinary Python string elements.

For example, a function that returns `"Hello world"`, decorated with
`@strip_range(3, 5)`, returns `"Hel.. world"`.

Call the function once for each invocation. Forward all positional and keyword
arguments and propagate its errors. Preserve its name, docstring, module,
annotations, and `__wrapped__` link. Decorators must also work when stacked.
