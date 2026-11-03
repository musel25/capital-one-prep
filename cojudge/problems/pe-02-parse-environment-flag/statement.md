**The ticket.** A service reads feature flags from environment variables, for example `NEW_CHECKOUT=yes`.

**Why it matters.** Environment variables are always text. `bool("false")` is `True`, because every nonempty string is truthy. A service that uses `bool(value)` turns on a feature by mistake.

### Your task

Write `parse_flag(value, default)`. Return `True`, `False`, or `None`.

1. If `value` is `None` (the variable is not set), return `default`.
2. Otherwise, remove whitespace at both ends and change the text to lowercase.
3. `true`, `1`, `yes`, and `on` return `True`.
4. `false`, `0`, `no`, and `off` return `False`.
5. Every other text, also an empty string, returns `None` (invalid).

**Constraints:**

- `value` is `None` or a string with at most 100 ASCII characters.
- `default` is `True` or `False`.
