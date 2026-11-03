## How it works

Filter by the cursor, sort, and slice. The cursor is the last ID on the page, but only when more records exist. So the client knows when to stop.

## Common mistakes

- Including the record whose ID equals the cursor. The cursor means "after this ID".
- Returning a cursor after the final page. The client then asks for an empty page.
- Sorting IDs as text, so `10` comes before `2`.

## Solution

```python
def paginate_records(records, after_id, limit):
    eligible = [row for row in records if after_id is None or row["id"] > after_id]
    eligible.sort(key=lambda row: row["id"])
    items = eligible[:limit]
    next_cursor = items[-1]["id"] if len(eligible) > len(items) else None
    return {"items": items, "next_cursor": next_cursor}
```
