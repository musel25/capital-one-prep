# Stage 1 — Aggregate purchases

Implement `summarize(events) -> dict[str, int]`. Process events in list order.
Each event has exactly these fields: id (nonempty string), type ("purchase"),
merchant (nonempty string), amount (positive integer cents, not bool).
Types/required fields are guaranteed by this exercise; do not build an API validator.
IDs are unique in this stage. Return total cents by merchant; empty input returns {}.
Preserve the input list and its dictionaries. Each call is independent.

Example: purchases p1/A/1000, p2/B/500, p3/A/200 yield {"A":1200,"B":500}.
Dictionary key order is not graded. Explain the meaning of each dictionary you use
and the time/space complexity. Add a same-merchant and an empty-input test.

Run `uv run pytest -q tests/test_stage1.py`. Explain this result before stage 2.
