## Reference solution

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
