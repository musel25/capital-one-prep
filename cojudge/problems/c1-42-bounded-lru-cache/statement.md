# 42. Build a capacity-bounded LRU cache

[Course list](/?course=capital-one-engineering-50) · Level 5 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Dictionaries, ordered collections, and cache misses.

A least-recently-used cache evicts the entry whose last successful use is oldest. A successful read counts as use. In this contract, an insert or overwrite also counts as use. A missing read does not change the order. Python's OrderedDict can move a key to the newest end and remove a key from the oldest end. This keeps the value and recency order in one structure. Capacity is a count of entries, not a byte limit. Capacity zero is still valid: every inserted key is immediately evicted. This exercise is a deterministic event trace, not an actual parallel, thread, or network test.

</details>

**Scenario:** An API gateway keeps a small in-memory cache of user profiles. When the cache is full, it removes the profile that was used least recently (LRU).

**Input:** `data` has:
- `capacity`: the maximum number of entries.
- `ops`: a list of `put` (`key`, integer `value`), `get` (`key`), or `delete` (`key`).

**Rules**
- `put`: insert or overwrite, and make the key the most recent. If the cache is now over capacity, evict the least recent key. The result is the evicted key, or `null`.
- `get`: return the value and make the key the most recent. If the key is absent, return `null` and change nothing.
- `delete`: remove the key. Return `true` if it existed, otherwise `false`.

**Return** `{"results": [...], "entries": [[key, value], ...]}`. List the final entries from least recent to most recent.

**Constraints:**

- Capacity is 0–100; there are 0–300 operations.
- Keys are nonempty ASCII strings. Values are integers from -1000000 to 1000000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 37 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/collections.html#collections.OrderedDict)
