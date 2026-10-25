# Stage 2 — Replayed and conflicting IDs

Keep stage 1 behavior and extend the same summarize function.
An identical event may be delivered again: count it only once.
Dictionary key order does not affect equality. If an ID reappears with ANY different
field value, raise ValueError. Event IDs are global within one call.
Preserve input on success and error. Do not keep state between calls.

Example: p1/A/1000, p2/B/500, an exact replay of p1 yields {"A":1000,"B":500}.
Reusing p1 with amount=900 or merchant=B raises ValueError.

Explain why "ID was seen, so skip" alone is insufficient.
Run `uv run pytest -q tests/test_stage1.py tests/test_stage2.py`.
