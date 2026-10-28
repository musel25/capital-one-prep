A service must parse feature flags from environment variables.

Implement `parse_flag(value, default)`. Return `default` when `value` is `None`.

Otherwise, remove surrounding spaces, tabs, carriage returns, and newlines. Compare without letter case:

- `true`, `1`, `yes`, and `on` return `True`.
- `false`, `0`, `no`, and `off` return `False`.
- Every other string, including an empty string, returns `None`.

**Constraints:**

- `value` is `None` or an ASCII string with at most 100 characters.
- `default` is a boolean.
- Do not change input objects or their nested values. Each call starts with fresh state.
