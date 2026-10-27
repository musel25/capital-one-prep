# 19. Cap partial refunds with exact cents

[Course list](/?course=capital-one-engineering-50) · Level 2 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Integer cents, dataclasses, and account invariants.

A payment can have several partial refunds. The limit applies to their cumulative total, not to each request in isolation. Store the original charge and the refunded amount, or store a remaining refundable amount. Integer cents keep every subtraction exact. Validate a request before changing state so a failed refund cannot reduce the remaining amount. Keep each payment’s state separate. A request for the exact remaining amount is valid and leaves zero. This exercise also permits zero-cent requests, which succeed without changing the amount. Real refund systems need additional rules for request IDs and external settlement; this task isolates the cumulative amount invariant.

</details>

**Input:** `data` has:
- `payments`: maps payment IDs to charged cents (nonnegative integers).
- `refunds`: a list of `{"payment": string, "cents": int}`, with nonnegative `cents`. Every payment ID exists.

**Rules:** process the refunds in order.
- Accept a refund when `cents` is at most the payment's remaining refundable cents. Subtract only accepted refunds.
- A zero-cent refund is accepted, also after a full refund.

**Return** `{"accepted": [bool], "remaining": {payment_id: int}}`
- `accepted`: one boolean per refund.
- `remaining`: the remaining refundable cents of every payment, including payments with no refund requests.

**Constraints:**

- At most 30 payments and 100 refund requests. Charged and requested cents are at most 1,000,000,000,000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/dataclasses.html), [2](https://docs.python.org/3.11/library/stdtypes.html#numeric-types-int-float-complex)
