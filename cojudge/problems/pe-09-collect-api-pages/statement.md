Our API client must stop on broken page chains and retain the IDs it already received.

Implement `collect_pages(pages, start)`. `pages` maps nonempty ASCII tokens to objects with an `items` list of nonnegative integer IDs and a `next` token or null. `start` is a token or null. Follow `next` until null. Return `{'items': [...], 'error': null}` on success. Keep each ID once, in first-seen order. If a token is absent from `pages`, stop before reading it and return error `'missing_page'`. If a token was already visited, stop before reading it again and return error `'cycle'`. Keep all IDs collected before either error. A null start returns empty items and a null error. Ignore pages outside the followed chain. Compare tokens exactly. Do not change the input.

**Constraints:**

- All page records contain items and next with the stated types.
- Tokens are nonempty ASCII strings; null is the only end marker.
- IDs are integers greater than or equal to zero; booleans are not IDs.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `collect_pages`. **Run** checks the examples. **Submit** checks all 16 cases.
