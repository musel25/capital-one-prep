# 44. Reject stale queue acknowledgements

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Hard · About 35 minutes**

**Before this problem:** State machines, integer clocks, and message retries.

## Learn first

Receiving a queue message can hide it for a limited time without deleting it. If the consumer does not acknowledge it before that deadline, another receive can deliver it again. Each delivery needs a fresh receipt token. An old consumer must not acknowledge the new delivery with its old token. This model uses an increasing token per message and accepts an acknowledgement only during that token's active visibility interval. At the exact deadline the message is visible again and the old token is invalid. These are the explicit rules of this exercise, not a promise about every queue provider. The task is a deterministic event trace, not an actual parallel, thread, or network test.

## Your task

`messages` contains unique IDs in queue order. `timeout` is a positive visibility duration. `ops` have nondecreasing `at` times. `receive` selects the first unacknowledged message whose deadline is at or before `at`; all messages start visible at 0. Increment its token, starting with 1, and set its deadline to `at + timeout`. Return `{id, token}` or null if none is visible. `ack` has `id` and `token`; return true and remove the message only if it has an active delivery with that exact token and `at < deadline`. Otherwise return false. Return `{results: [...], pending: [...]}` with pending IDs in original order, including hidden messages. Unknown IDs and token 0 are allowed in acknowledgements and must fail.

## Examples

### Example 1: ack before visibility timeout

Input to `solve`:
```json
{
  "messages": [
    "a"
  ],
  "timeout": 5,
  "ops": [
    {
      "op": "receive",
      "at": 0
    },
    {
      "op": "ack",
      "at": 4,
      "id": "a",
      "token": 1
    }
  ]
}
```
Return:
```json
{
  "results": [
    {
      "id": "a",
      "token": 1
    },
    true
  ],
  "pending": []
}
```

### Example 2: redelivery invalidates stale token

Input to `solve`:
```json
{
  "messages": [
    "a"
  ],
  "timeout": 5,
  "ops": [
    {
      "op": "receive",
      "at": 0
    },
    {
      "op": "receive",
      "at": 5
    },
    {
      "op": "ack",
      "at": 6,
      "id": "a",
      "token": 1
    },
    {
      "op": "ack",
      "at": 6,
      "id": "a",
      "token": 2
    }
  ]
}
```
Return:
```json
{
  "results": [
    {
      "id": "a",
      "token": 1
    },
    {
      "id": "a",
      "token": 2
    },
    false,
    true
  ],
  "pending": []
}
```

### Example 3: ack at timeout is too late

Input to `solve`:
```json
{
  "messages": [
    "a"
  ],
  "timeout": 5,
  "ops": [
    {
      "op": "receive",
      "at": 0
    },
    {
      "op": "ack",
      "at": 5,
      "id": "a",
      "token": 1
    }
  ]
}
```
Return:
```json
{
  "results": [
    {
      "id": "a",
      "token": 1
    },
    false
  ],
  "pending": [
    "a"
  ]
}
```

## Constraints

- 0–100 messages; 0–300 operations. IDs are nonempty ASCII strings.
- Times are 0–1000000, timeout is 1–1000000, tokens are 0–1000000.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 36 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
