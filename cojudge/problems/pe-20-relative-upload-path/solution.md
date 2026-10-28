## Reference solution

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
