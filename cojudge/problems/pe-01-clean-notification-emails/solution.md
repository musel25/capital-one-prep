## How it works

Loop over the addresses once. Clean each address, then use a set to see if you already have it. The list keeps the first-seen order.

## Common mistakes

- Sorting the result. The order must stay as in the input.
- Checking for duplicates before you lowercase. Then `ADA@X` and `ada@x` both stay.
- Keeping empty entries such as `" "`.

## Solution

```python
def clean_emails(emails):
    out, seen = [], set()
    for email in emails:
        email = email.strip(" \t\r\n").lower()
        if email and email not in seen:
            seen.add(email)
            out.append(email)
    return out
```
