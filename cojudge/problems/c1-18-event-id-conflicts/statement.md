# 18. Separate duplicate events from conflicts

[Course list](/?course=capital-one-engineering-50) · Level 2 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Dictionaries, event processing, and signed integer arithmetic.

An event ID can make a retried operation safe to handle more than once. Store the payload associated with the first use of that ID. If a later event has the same ID and the same payload, it is a duplicate and must not apply again. If it has a different payload, it is a conflict. Ignoring that distinction can hide a caller bug or apply an unintended change. Do not replace the stored payload when a conflict arrives. The first event remains the reference for later comparisons. This task uses a single signed delta as the payload, so equality has one clear meaning.

</details>

**Input:** `data` has:
- `balance`: the integer starting total.
- `events`: a list of `{"id": string, "delta": int}`.

Totals and deltas can be negative.

**Rules:** for each event, in order:
- First time an ID appears: add its `delta` to the total. Status `applied`.
- ID seen before, with the same `delta` as its first event: status `duplicate`.
- ID seen before, with a different `delta`: status `conflict`.
- `duplicate` and `conflict` do not change the total or the stored first delta.

**Return** `{"status": [string], "balance": int}`: the statuses in event order, and the final total.

**Constraints:**

- At most 100 events. Initial total and deltas have absolute value at most 1,000,000,000,000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)
