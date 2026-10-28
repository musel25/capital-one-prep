The records endpoint must return stable pages when its source records arrive out of order.

Implement `paginate_records(records, after_id, limit)`. Return `{'items': [...], 'next_cursor': ...}`.

Sort records by numeric `id` in ascending order. If `after_id` is not `None`, keep only IDs strictly greater than it. The cursor need not match a record. Return at most `limit` eligible records and retain every field.

Set `next_cursor` to the last returned ID only if more eligible records remain. Otherwise use `None`, including for empty results and exactly full final pages.

**Constraints:**

- 0–200 records; limit is an integer from 1 through 50.
- IDs are unique positive integers; after_id is null or a non-negative integer.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Records are unsorted JSON objects. Fields other than `id` can contain any JSON value.
- Do not change input objects or their nested values. Each call starts with fresh state.
