## How it works

First reject the characters that are never allowed. Then walk through the parts with a stack. `..` removes the last part, and a `..` with nothing to remove means the path leaves the folder.

## Common mistakes

- Accepting a path that starts with `/`.
- Ignoring a `..` that goes above the folder instead of rejecting the path.
- Treating every name that starts with `.` as special.

## Solution

```python
def resolve_upload_path(path):
    if path.startswith("/") or "\\" in path or "\x00" in path:
        return None
    parts = []
    for component in path.split("/"):
        if component in ("", "."):
            continue
        if component == "..":
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(component)
    return "/".join(parts) if parts else None
```
