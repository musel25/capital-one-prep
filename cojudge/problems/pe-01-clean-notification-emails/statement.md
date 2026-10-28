The notification service receives duplicate email addresses from an import.

Given a list of strings `emails`, return the cleaned addresses. Remove leading and trailing spaces, tabs, carriage returns, and newlines. Convert letters to lowercase. Skip empty results. Keep each cleaned address once, in its first input position. Do not validate email syntax or remove internal characters.

**Constraints:**

- `0 <= len(emails) <= 1000`.
- Each item is an ASCII string with at most 200 characters. Empty strings are allowed.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `clean_emails`. **Run** checks the examples. **Submit** checks all 12 cases.
