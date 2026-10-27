# 05. Reconcile repeated item IDs

[Course list](/?course=capital-one-engineering-50) · Level 1 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

A set records whether an item is present. It does not record how many times the item occurs. Counter stores a count for each key and acts as a multiset. In a reconciliation task, repeated IDs can represent separate units. Counter subtraction keeps only positive counts. Therefore expected minus observed gives missing units, and observed minus expected gives extra units. Neither result includes zero or negative counts. Keep the input meaning separate from output order. Sorting the result keys makes the report deterministic even when two batches list their units in different orders. The output should preserve counts, not expand each count into repeated rows.

</details>

**Input:** `data` has:
- `expected`: a list of item IDs (ASCII strings).
- `observed`: a list of item IDs (ASCII strings).

A repeated ID counts as a separate unit each time.

**Rules:** for each ID:
- missing count = max(count in `expected` − count in `observed`, 0)
- extra count = max(count in `observed` − count in `expected`, 0)

**Return** `{"missing": [...], "extra": [...]}`
- Each list contains `{"id": string, "count": int}` for each ID whose count is above 0. Do not include zero counts.
- Sort each list by ID in ascending ASCII order.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3/library/collections.html#collections.Counter)
