# 04. Summarize service errors

The operations dashboard needs request and server-error counts for each service.

Given a list `logs`, return a dictionary keyed by service name. Each input row has `service` and `status`. Each output value has `requests`, the number of rows for that service, and `errors`, the number with status 500 or more. Count duplicate rows. Service names are case-sensitive. Return an empty dictionary for empty logs.

**Constraints:**

- `0 <= len(logs) <= 10000`.
- `service` is a nonempty ASCII string with at most 100 characters.
- `status` is an integer from 100 through 599. Every row has both fields.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `summarize_logs`. **Run** checks the examples. **Submit** checks all 12 cases.
