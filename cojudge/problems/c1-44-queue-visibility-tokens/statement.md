# 44. Reject stale queue acknowledgements

[Course list](/?course=capital-one-engineering-50) · Level 5 · Hard · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** State machines, integer clocks, and message retries.

Receiving a queue message can hide it for a limited time without deleting it. If the consumer does not acknowledge it before that deadline, another receive can deliver it again. Each delivery needs a fresh receipt token. An old consumer must not acknowledge the new delivery with its old token. This model uses an increasing token per message and accepts an acknowledgement only during that token's active visibility interval. At the exact deadline the message is visible again and the old token is invalid. These are the explicit rules of this exercise, not a promise about every queue provider. The task is a deterministic event trace, not an actual parallel, thread, or network test.

</details>

**Scenario:** A job queue hides a message for `timeout` time units after a worker receives it. If the worker does not finish in time, the message becomes visible again, and another worker can take it. Each receipt gets a new token, so a slow first worker cannot acknowledge a message that another worker now owns.

**Input:** `data` has:
- `messages`: unique IDs in queue order.
- `timeout`: a positive visibility duration.
- `ops`: a list of operations. Their `at` times never decrease.

**Rules:** all messages start visible at time 0.
- `receive`: select the first unacknowledged message whose deadline is at or before `at`. Add 1 to its token (the first token is 1) and set its deadline to `at + timeout`. Return `{"id": ..., "token": ...}`, or `null` if no message is visible.
- `ack` (`id`, `token`): return `true` and remove the message only if it has an active delivery with exactly this token and `at < deadline`. Otherwise return `false`. Unknown IDs and token 0 can occur, and they always fail.

**Return** `{"results": [...], "pending": [...]}`. `pending` lists the unacknowledged IDs in original order, including hidden messages.

**Constraints:**

- 0–100 messages; 0–300 operations. IDs are nonempty ASCII strings.
- Times are 0–1000000, timeout is 1–1000000, tokens are 0–1000000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 36 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
