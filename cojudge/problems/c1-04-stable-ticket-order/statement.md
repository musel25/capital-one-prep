# 04. Sort tickets with stable ties

[Course list](/?course=capital-one-engineering-50) · Level 1 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

A sort key can express several business rules. Python compares tuples from left to right. Negating an integer makes a larger value sort first while the next key can still sort in ascending order. Python sorting is stable: records with equal keys keep their original relative order. Stability is useful when input order is the final tie rule. Do not add an identifier as a tie breaker unless the contract asks for it. Two valid ordering choices can produce different results for the same records. Use sorted when you want a new list and want to preserve the caller’s input.

</details>

**Input:** `data` has:
- `tickets`: a list of objects with `id` (string), `priority` (integer 0–9), and `created` (integer 0–1,000,000). IDs are not always unique.

**Return** the list of ticket IDs, sorted by:
1. `priority`, highest first.
2. Then `created`, lowest first.
3. If both tie, keep the input order.

The ID text never changes the order.

**Constraints:**

- At most 1,000 tickets. All records contain the required fields.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts)
