# 01. Create a sandwich decorator

Implement `sandwich(func)`.

The decorated function prints the upper bread slice first. It then calls the
wrapped function. After a successful call, it prints the lower bread slice.
Use the supplied constants. Forward all positional and keyword arguments.
Return the wrapped result. Preserve the function name, docstring and annotations.
Let exceptions from the wrapped function reach the caller. The lower slice is
optional when the wrapped function raises.

Example: a decorated function that prints `cheese` produces:

```text
=== Upper bread slice ===
cheese
=== Lower bread slice ===
```
