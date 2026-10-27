# 48. Preserve read-your-writes with version floors

[Course list](/?course=capital-one-engineering-50) · Level 5 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Version numbers, replication lag, and deterministic selection.

Replicas can lag behind a completed write. A client can carry the version of its last write as a minimum acceptable version for later reads. A replica below that floor must not answer the read, even if it is reachable. If none qualifies, the caller must wait or use another source. This exercise selects the freshest eligible replica and uses its ID to break ties. Replication updates can also arrive out of order, so a replica must never replace a newer version with an older one. All equal versions represent the same value here. This is a deterministic event trace, not an actual parallel, thread, or network test.

</details>

**Scenario:** A database has several replicas that can lag behind. After a user saves data, the app gets a write token (a version). The user's next read must go to a replica that has at least that version, so the user sees their own change.

**Input:** `data` has:
- `replicas`: a list of `{"id": ..., "version": ..., "value": ...}`, with unique IDs.
- `ops`: a list of operations:
  - `publish`: an existing `id`, a `version`, and a `value`.
  - `read`: a `min_version`, which is the client's write token.

In all input records and publications, equal versions always have equal values.

**Rules**
- `publish`: a higher version than the replica's → update the replica and return `"applied"`. A lower version → ignore it and return `"stale"`. An equal version → return `"unchanged"`.
- `read`: eligible replicas have a version of at least `min_version`. Return `{"id": ..., "version": ..., "value": ...}` of the replica with the highest version. On a tie, use the smallest ASCII ID. Return `null` if no replica is eligible. Use only the supplied `min_version`; do not infer it from other reads.

**Return** `{"results": [...], "replicas": [[id, version, value], ...]}`, with the final replicas sorted by ID.

**Constraints:**

- 0–100 replicas and 0–300 operations. Publish IDs always exist.
- IDs are nonempty ASCII strings; versions and min_version are 0–1000000; values are integers from -1000000 to 1000000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 36 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels)
