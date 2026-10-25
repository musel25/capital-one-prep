# Stage 3 — Partial refunds

Keep both earlier stages. Events may now also be refunds with exactly:
id (nonempty string), type ("refund"), purchase_id (nonempty string),
amount (positive integer cents, not bool).
All field types are guaranteed; only the business-rule errors below need validation.

A refund subtracts from the original purchase's merchant total. Its purchase must
already have appeared earlier in this call. Unknown or forward references raise
ValueError. Cumulative refunds cannot exceed that purchase's amount; equality is
allowed. Preserve merchants whose totals reach zero.

Check replay/conflict BEFORE applying or validating a second copy of an event.
An identical refund replay does not subtract again, even after the purchase has
been fully refunded. Different content under an existing ID raises ValueError,
including reusing a purchase ID for a refund. Preserve input on all outcomes.

Example: p1/A/1000, p2/B/500, r1->p1/300, r2->p1/700, replay r1 gives
{"A":0,"B":500}. A new refund of 1 cent for p1 raises ValueError.
Return a dictionary for a valid batch; for an invalid batch raise rather than
returning partial totals. Each function call starts fresh.

Run `uv run pytest -q`, add one boundary test, and explain how the earlier stages
still work. Show actual results, remaining uncertainty and time/space complexity.
