# 47. Route requests around a consistent hash ring

[Course list](/?course=capital-one-engineering-50) · Level 5 · Hard · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Sorted lists, binary search, and dictionaries.

A hash ring assigns each request to the first node at or after its hash, moving in increasing hash order. If no node remains in that direction, the search wraps to the first node. An exact hash match belongs to that node. Adding a node changes the interval immediately before it; removing a node hands its interval to its successor. This exercise supplies deterministic integer hashes so that language hash randomization cannot change the answers. Python's bisect_left finds the required insertion position, including exact matches. The model uses one point per node. This is a deterministic event trace, not an actual parallel, thread, or network test.

</details>

**Input:** `data` has:
- `nodes`: a list of `{"id": ..., "hash": ...}`, with unique IDs and hashes. Hashes are points on a ring from 0 to 999.
- `ops`: a list of operations. Process them in order.

**Rules**
- `lookup` (`hash`): return the ID at the smallest active hash that is greater than or equal to `hash`. If there is none, wrap around to the smallest hash. Return `null` if the ring is empty.
- `add` (`id`, `hash`, both currently unused): add the node and return `"added"`.
- `remove` (`id`): remove the node and return `true`, or return `false` if it is absent.

The input supplies the hashes. Do not call Python's `hash` function.

**Return** `{"results": [...], "ring": [[hash, id], ...]}`, with the final ring sorted by hash.

**Constraints:**

- 0–100 initial nodes and 0–300 operations. Active hashes and IDs remain unique.
- IDs are nonempty ASCII strings. Removed IDs and hash points may later be reused.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 36 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/bisect.html)
