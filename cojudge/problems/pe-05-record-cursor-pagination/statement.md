The records endpoint must return stable pages when its source records arrive out of order.

Implement paginate_records(records, after_id, limit). records is an unsorted list of JSON objects with unique positive integer id fields. Other fields can contain any JSON value. after_id is null or a non-negative integer; it need not match a record. Sort records by numeric id in ascending order. If after_id is not null, keep only IDs strictly greater than it. Return {'items': [...], 'next_cursor': ...}, with at most limit eligible records. next_cursor is the last returned ID only when more eligible records remain. Otherwise it is null, including for empty results and exactly full final pages. Retain every field of each selected record. Do not change the input list or records. Each call is independent.

**Constraints:**

- 0–200 records; limit is an integer from 1 through 50.
- IDs are unique positive integers; after_id is null or a non-negative integer.
- Inputs satisfy the contract. No input validation, storage or network access is required.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `paginate_records`. **Run** checks the examples. **Submit** checks all 15 cases.
