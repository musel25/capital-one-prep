A service must parse feature flags from environment variables.

Given `value` and a boolean `default`, return the parsed flag. If `value` is `None`, return `default`. Otherwise, remove surrounding spaces, tabs, carriage returns, and newlines. Compare without letter case. `true`, `1`, `yes`, and `on` mean `True`. `false`, `0`, `no`, and `off` mean `False`. Return `None` for every other string, including an empty string.

**Constraints:**

- `value` is `None` or an ASCII string with at most 100 characters.
- `default` is a boolean.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `parse_flag`. **Run** checks the examples. **Submit** checks all 14 cases.
