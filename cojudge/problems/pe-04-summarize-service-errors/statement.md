The operations dashboard needs request and server-error counts for each service.

Implement `summarize_logs(logs)`. Return a dictionary keyed by service name. Each value contains:

- `requests`: the number of rows for that service.
- `errors`: the number of those rows with status 500 or more.

Count duplicate rows. Compare service names exactly. Empty logs return an empty dictionary.

**Constraints:**

- `0 <= len(logs) <= 10000`.
- `service` is a nonempty ASCII string with at most 100 characters.
- `status` is an integer from 100 through 599. Every row has both fields.
- Do not change input objects or their nested values. Each call starts with fresh state.
