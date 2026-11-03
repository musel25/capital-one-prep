**The ticket.** The request logger writes request data to the logs. It must remove passwords, tokens, and secrets first, at every level of the data.

**Why it matters.** Many people can read logs, and logs are kept for a long time. A password in a log is a security incident. Request data is often nested, so a secret can be at any depth.

### Your task

Write `redact_secrets(value)`. The input is any JSON value: a dictionary, a list, a string, a number, a boolean, or `None`. Return a new value.

1. In a dictionary, compare each key in lowercase. If it is exactly `password`, `token`, or `secret`, replace the whole value with `'[REDACTED]'`. Keep the key as it is written.
2. Process all other dictionary values and all list items in the same way, at every depth.
3. Return strings, numbers, booleans, and `None` unchanged. Only keys are checked: a string value `'password'` stays.
4. Match whole keys only. `password_hint`, `access_token`, and `' token'` are not secret keys.

**Constraints:**

- The data is at most 10 levels deep and has at most 1000 values. Keys are ASCII strings.
