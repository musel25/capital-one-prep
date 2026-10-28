## Reference solution

```python
def paginate_records(records, after_id, limit):
    eligible = [row for row in records if after_id is None or row["id"] > after_id]
    eligible.sort(key=lambda row: row["id"])
    items = eligible[:limit]
    next_cursor = items[-1]["id"] if len(eligible) > len(items) else None
    return {"items": items, "next_cursor": next_cursor}
```
