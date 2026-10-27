# 41. Expire and invalidate cache entries

[Course list](/?course=capital-one-engineering-50) · Level 5 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Dictionaries and integer time arithmetic.

A time-to-live cache stores a value and its expiration time. If an entry is written at time t with lifetime d, its expiration is t + d. It is usable only while the current time is strictly less than that expiration. Reads do not extend this lifetime unless the contract explicitly says so. An overwrite replaces both the value and its expiration. Invalidation removes the entry immediately. Distinguish a missing key from a cached value such as zero. This exercise uses an integer clock supplied by each operation. It is a deterministic event trace, not an actual parallel, thread, or network test.

</details>

**Input:** `data` has:
- `ops`: a list of operations. Each has an integer time `at`. Times never decrease.

**Rules:** before each operation, remove every entry whose expiration time is at or before `at`. Then:
- `put` (`key`, integer `value`, `ttl`): replace the entry, set its expiration to `at + ttl`, and return `"stored"`. A `ttl` of 0 removes any old entry and stores nothing.
- `get` (`key`): return the value, or `null` if there is no entry.
- `invalidate` (`key`): remove the entry. Return `true` if an unexpired entry was removed, otherwise `false`.

**Return** `{"results": [...], "keys": [...]}`: one result per operation, and the keys that remain after the last operation, in ASCII order. An empty `ops` list returns empty lists.

**Constraints:**

- 0–300 operations. at and ttl are 0–1000000.
- Keys are nonempty ASCII strings; values are integers from -1000000 to 1000000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 37 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)
