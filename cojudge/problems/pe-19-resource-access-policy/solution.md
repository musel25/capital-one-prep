## Reference solution

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
