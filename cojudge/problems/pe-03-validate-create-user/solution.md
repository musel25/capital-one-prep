## Reference solution

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
