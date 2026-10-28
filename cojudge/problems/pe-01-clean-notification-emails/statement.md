The notification service receives duplicate email addresses from an import.

Implement `clean_emails(emails)`. Return cleaned addresses in first-seen order.

Remove surrounding spaces, tabs, carriage returns, and newlines. Convert letters to lowercase. Skip empty results and duplicates. Keep internal characters unchanged. Do not validate email syntax.

**Constraints:**

- `0 <= len(emails) <= 1000`.
- Each item is an ASCII string with at most 200 characters. Empty strings are allowed.
- Do not change input objects or their nested values. Each call starts with fresh state.
