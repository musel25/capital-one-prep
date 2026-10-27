# 10. Schedule jobs with stable priorities

[Course list](/?course=capital-one-engineering-50) · Level 1 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

A heap provides efficient access to the smallest key. heapq uses Python tuple ordering, so a tuple can hold a priority, an insertion sequence, and the job payload. The sequence gives a stable tie rule and prevents the payload from deciding the order. Keep the sequence increasing across all insertions, including after a pop. A heap’s internal list is not globally sorted. If you need a final ordered report, sort a copy or drain a separate heap. Empty pops need an explicit result. This task uses null so the result list still contains one entry for each requested pop.

</details>

**Input:** `data` has:
- `actions`: a list of operations:
  - `{"op": "add", "id": string, "priority": int}` adds a job. Priority is from -100 to 100. A smaller value runs first.
  - `{"op": "pop"}` removes the next job.

**Rules**
- Jobs with equal priority run in insertion order.
- IDs can repeat.
- A `pop` records the ID of the removed job, or `null` if the queue is empty.
- An `add` records nothing.

**Return** `{"popped": [...], "pending": [...]}`
- `popped`: the result of each `pop`, in order.
- `pending`: the IDs still in the queue, in the order they would be popped.

**Practice:** use `heapq`. The judge checks only the output.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/heapq.html#priority-queue-implementation-notes)
