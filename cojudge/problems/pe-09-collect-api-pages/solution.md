## Reference solution

```python
def collect_pages(pages, start):
    items = []
    seen_ids = set()
    visited = set()
    token = start
    while token is not None:
        if token in visited:
            return {"items": items, "error": "cycle"}
        if token not in pages:
            return {"items": items, "error": "missing_page"}
        visited.add(token)
        page = pages[token]
        for item in page["items"]:
            if item not in seen_ids:
                seen_ids.add(item)
                items.append(item)
        token = page["next"]
    return {"items": items, "error": None}
```
