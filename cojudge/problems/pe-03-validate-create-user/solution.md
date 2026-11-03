## How it works

Check each field on its own and append its name when it fails. Because you check the fields in a fixed order, the list is always in the order `name`, `email`, `age`.

## Common mistakes

- Using `isinstance(age, int)`, which accepts `True`.
- Rejecting a valid age of `0` with `if not age`.
- Stopping after the first error. The client needs all errors.

## Solution

```python
def validate_user(payload):
    errors = []
    name = payload.get("name")
    if not isinstance(name, str) or not name.strip(" \t\r\n"):
        errors.append("name")
    email = payload.get("email")
    valid_email = isinstance(email, str) and email.count("@") == 1
    if valid_email:
        local, domain = email.split("@")
        valid_email = bool(local and domain) and not any(c in " \t\r\n" for c in email)
    if not valid_email:
        errors.append("email")
    if "age" in payload and (type(payload["age"]) is not int or payload["age"] < 0):
        errors.append("age")
    return errors
```
