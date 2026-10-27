# 49. Expire reservations and make transitions idempotent

[Course list](/?course=capital-one-engineering-50) · Level 5 · Hard · About 40 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** State machines, inventory invariants, and idempotency.

A reservation temporarily removes stock from the available pool. Confirmation makes that allocation permanent. Release or expiry returns the held stock, but must do so only once. Terminal states prevent repeated commands from creating extra stock. An idempotent reserve retry also must not extend the original deadline. Here each accepted reservation retains its ID, payload, and final state. Insufficient attempts create no record and may retry later. Expire held records before processing every command, including commands for another ID. This makes the exact expiry boundary explicit. The task is a deterministic event trace, not an actual parallel, thread, or network test.

</details>

**Scenario:** A ticket site holds seats in a cart for a short time. If the customer does not pay before the hold expires, the seats go back on sale. Clients can send a request again, so a repeated request must be safe.

**Input:** `data` has:
- `stock`: the starting integer stock.
- `ops`: a list of operations. Each has `at` (times never decrease), `id`, and `op`.

**Rules:** before each operation, every `held` reservation with `expires` at or before `at` changes to `expired`, and its quantity goes back to the stock.
- `reserve` (also has positive `qty` and `ttl`):
  - Existing ID: return its current state if `qty` and `ttl` match, otherwise `"conflict"`. Never extend the expiry.
  - New ID and the stock is less than `qty`: return `"insufficient"` and store no record.
  - New ID otherwise: subtract `qty` from the stock, set `expires = at + ttl`, store the state `held`, and return `"held"`.
- `confirm`: change `held` to `confirmed`. The stock does not come back.
- `release`: change `held` to `released`. The quantity goes back to the stock once.
- `confirm` and `release` return the current state after the operation, or `"missing"` for an unknown ID.
- `confirmed`, `released`, and `expired` never change.

**Return** `{"results": [...], "available": int, "reservations": [[id, state], ...]}`, with the reservations sorted by ASCII ID.

**Constraints:**

- Stock is 0–1000000. There are 0–300 operations.
- Times are 0–1000000; qty and ttl are 1–1000000. IDs are nonempty ASCII strings.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 39 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/enum.html), [2](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)
