# 09. Keep the final iterator batch

[Course list](/?course=capital-one-engineering-50) · Level 1 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

An iterator gives values one at a time and remembers its current position. You can group its values without indexing the original sequence. itertools.islice reads up to a fixed number of values from the current iterator position. The final group can be shorter than the requested batch size. That partial group still contains work and must be emitted. Stop only when a read returns no values. In a real streaming application, this pattern can limit the active buffer to one batch. This exercise returns every batch as JSON, so the complete result still occupies memory. The grouping logic should preserve every item exactly once.

</details>

**Scenario:** An email service sends messages through a provider that accepts at most `size` recipients per API call. `solve` splits the list of recipient IDs into calls. The last call can be smaller, but it must not be dropped.

**Input:** `data` has:
- `values`: a list of integers from -1,000,000 to 1,000,000.
- `size`: an integer from 1 to 20.

**Return** the values split into consecutive batches, as a list of lists.
- Every batch has `size` items. Only the last batch can be smaller, and it is never empty.
- Keep the order and the duplicates.
- An empty `values` list returns `[]`.

**Practice:** use an iterator and `itertools.islice`. The judge checks only the output.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/itertools.html#itertools.islice)
