# 43. Deduplicate at-least-once message delivery

[Course list](/?course=capital-one-engineering-50) · Level 5 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Sets, idempotency, and transaction boundaries.

At-least-once delivery means a message can arrive more than once. A consumer should identify the logical message by its ID and record completed IDs with the business effect. These two changes form one logical commit in this model. If processing fails before commit, a retry must still apply the effect. If the acknowledgement is lost after commit, a retry must acknowledge the message without applying it again. Do not mark a message complete before its effect commits. This task supplies the failures directly. It is a deterministic event trace, not an actual parallel, thread, or network test, and it makes no claim of end-to-end exactly-once delivery.

</details>

**Scenario:** A rewards service reads point events from a queue that delivers each message at least once. A message arrives again if its acknowledgement is lost. Points must be added exactly once per message ID.

**Input:** `data` has:
- `total`: the initial integer total.
- `deliveries`: a list of `{"id": ..., "amount": ..., "fail": ...}`. `fail` is `"none"`, `"before"`, or `"after"`. All deliveries with the same ID have the same amount.

**Rules:** for each delivery:
- **ID already processed:** return `"ack"`. Nothing changes, whatever `fail` is.
- **New ID:**
  - `"before"` → return `"retry"`. Nothing is committed.
  - Otherwise, in one atomic step, add `amount` to the total and record the ID as processed. Then `"after"` returns `"retry"` (a lost acknowledgement), and `"none"` returns `"ack"`.

**Return** `{"results": [...], "total": int, "processed": [...]}`. `processed` lists the processed IDs in ASCII order.

This is an in-memory model of a commit boundary.

**Constraints:**

- 0–300 deliveries. IDs are nonempty ASCII strings.
- total and amounts are integers from -1000000 to 1000000. fail is none, before, or after.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 36 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html)
