# 32. Fix a LEFT JOIN that loses customers

[Course list](/?course=capital-one-engineering-50) · Level 4 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problem 31; SELECT, WHERE, ordering, and SQL NULL.

A LEFT JOIN keeps each row from its left table even when no right-table row matches. Missing right-side values become NULL. A condition in ON controls which right rows can match. A condition in WHERE runs after the join and can remove those generated NULL rows. This difference often breaks reports that must include customers with no activity. The starter query has that defect. Move the payment qualification to the correct place while preserving the full output contract. A zero amount is a real value, not a missing value. Customers can also share a name, so joins must use their ids rather than display text.

</details>

**Bug fix.** The `report_rows(connection)` query is intentionally faulty. Fix it.

**Input:** `data` has the lists `customers` and `payments`. The scaffold loads them into:
- `customers(id PRIMARY KEY, name)`
- `payments(id PRIMARY KEY, customer_id nullable, amount, status)`

**Rules**
- For each customer, output one row per payment that has a matching `customer_id` and `status` paid.
- A customer with no matching paid payment gets exactly one row, with `payment_id` and `amount` set to null.
- Ignore orphan payments, payments with a null `customer_id`, and pending payments.

**Return** a list of `{"customer_id": ..., "name": ..., "payment_id": ..., "amount": ...}`, ordered by `customer_id` ascending, then `payment_id` ascending.

**Practice:** use a LEFT JOIN. The reference runs SQLite. The judge cannot check SQL use or query structure.

**Constraints:**

- 0–200 customers and 0–300 payments. Ids are positive integers at most 1000000 and unique within each table.
- Payment customer_id is null or a positive integer at most 1000000. Foreign keys are intentionally not enforced.
- status is paid or pending. amount is an integer in [-1000000,1000000]. Names have 1–50 printable ASCII characters.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.sqlite.org/lang_select.html#whereclause)
