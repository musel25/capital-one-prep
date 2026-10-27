# 46. Schedule dependent jobs and detect blocked cycles

[Course list](/?course=capital-one-engineering-50) · Level 5 · Hard · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Sets, directed graphs, and dependency order.

A job is ready when every prerequisite has completed. A dependency scheduler can repeatedly select ready jobs, run a bounded batch, and then mark that batch complete. All jobs in this task take one round, so a job cannot start in the same round as its prerequisite. If unfinished jobs remain but none is ready, the remaining dependency graph contains a cycle. Some blocked jobs may only depend on a cycle and are not themselves part of it. Report all unfinished jobs separately from the cycle flag. A fixed tie rule makes results reproducible. This is a deterministic event trace model, not an actual parallel, thread, or network test.

</details>

**Input:** `data` has:
- `jobs`: a list of `{"id": string, "depends": [ids]}`. IDs are unique ASCII strings. `depends` lists distinct existing job IDs. Self-dependencies and cycles can occur.
- `workers`: the maximum number of jobs per round.

**Rules:** repeat rounds.
1. At the start of a round, find every unfinished job whose dependencies all finished in earlier rounds.
2. Select up to `workers` of these jobs, in ascending ASCII ID order. All selected jobs finish at the end of the round.
3. Stop when all jobs are finished or no job is ready.

**Return** `{"rounds": [[id, ...], ...], "blocked": [...], "has_cycle": bool}`
- `blocked`: the unfinished jobs, sorted.
- `has_cycle`: `true` exactly when some jobs are blocked. Do not claim that every blocked job is part of a cycle.

**Constraints:**

- 0–100 jobs, at most 100 dependencies per job, and 1–20 workers.
- Every dependency refers to a supplied job. Each job takes exactly one round and always succeeds.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 37 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/graphlib.html)
