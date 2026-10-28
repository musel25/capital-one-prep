Our API client must stop on broken page chains and retain the IDs it already received.

Implement `collect_pages(pages, start)`. Follow `next` tokens from `start` until `None`. Return `{'items': [...], 'error': None}` on success.

Keep each ID once, in first-seen order. Compare tokens exactly. Stop before reading a missing or previously visited token:

- A missing token returns error `'missing_page'`.
- A repeated token returns error `'cycle'`.

Keep all IDs collected before an error. A `None` start returns empty items and no error. Ignore pages outside the followed chain.

**Constraints:**

- All page records contain items and next with the stated types.
- Tokens are nonempty ASCII strings; null is the only end marker.
- IDs are integers greater than or equal to zero; booleans are not IDs.
- `pages` maps tokens to objects with an `items` list and a `next` token or `None`; `start` is a token or `None`.
- Do not change input objects or their nested values. Each call starts with fresh state.
