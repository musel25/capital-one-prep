**The ticket.** The records endpoint returns records in pages. The client sends the last ID it saw, and the endpoint returns the next page.

**Why it matters.** If the order is not stable, or the cursor is wrong, clients skip or repeat records. The bug is hard to see because each page looks correct.

### Your task

Write `paginate_records(records, after_id, limit)`. Return `{'items': [...], 'next_cursor': ...}`.

1. If `after_id` is not `None`, keep only the records with `id > after_id`. The cursor does not need to be an existing ID.
2. Sort the records by `id`, smallest first.
3. Take at most `limit` records. Keep all their fields.
4. If more records remain after this page, `next_cursor` is the `id` of the last record on the page. Otherwise it is `None`.

**Constraints:**

- 0–200 records. `id` values are unique positive integers. Records can have other fields.
- `after_id` is `None` or an integer of 0 or more. `limit` is 1–50.
