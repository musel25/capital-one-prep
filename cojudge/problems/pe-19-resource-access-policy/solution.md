## How it works

The function is a list of rules in a fixed order. Deny rules come first, then allow rules, and the default is deny. This "deny by default" design is the safe way to write permissions.

## Common mistakes

- Ignoring `suspended` for admins.
- Letting a public resource allow `write` or `delete`.
- Allowing any member instead of only the owner.

## Solution

```python
def can_access(user, resource, action):
    if action not in ("read", "write", "delete"):
        return False
    if user["suspended"]:
        return False
    if user["role"] == "admin":
        return True
    if action == "read" and resource["public"]:
        return True
    return user["role"] == "member" and user["id"] == resource["owner_id"]
```
