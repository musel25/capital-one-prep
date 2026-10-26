# 43. Deduplicate at-least-once message delivery

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Medium · About 25 minutes**

**Before this problem:** Sets, idempotency, and transaction boundaries.

## Learn first

At-least-once delivery means a message can arrive more than once. A consumer should identify the logical message by its ID and record completed IDs with the business effect. These two changes form one logical commit in this model. If processing fails before commit, a retry must still apply the effect. If the acknowledgement is lost after commit, a retry must acknowledge the message without applying it again. Do not mark a message complete before its effect commits. This task supplies the failures directly. It is a deterministic event trace, not an actual parallel, thread, or network test, and it makes no claim of end-to-end exactly-once delivery.

## Your task

`total` is the initial integer total. `deliveries` contains `{id, amount, fail}`. All deliveries with the same ID have the same amount. If an ID is already processed, return `ack` with no effect, regardless of `fail`. For a new ID, `before` returns `retry` without committing. Otherwise atomically add `amount` and record the ID. Then `after` returns `retry` to model a lost acknowledgement; `none` returns `ack`. Return `{results: [...], total: integer, processed: [...]}` with processed IDs sorted in ASCII order. This is an in-memory model of a commit boundary.

## Examples

### Example 1: duplicate delivery has one effect

Input to `solve`:
```json
{
  "total": 0,
  "deliveries": [
    {
      "id": "a",
      "amount": 2,
      "fail": "none"
    },
    {
      "id": "a",
      "amount": 2,
      "fail": "none"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "ack",
    "ack"
  ],
  "total": 2,
  "processed": [
    "a"
  ]
}
```

### Example 2: failure before commit can retry

Input to `solve`:
```json
{
  "total": 0,
  "deliveries": [
    {
      "id": "a",
      "amount": 2,
      "fail": "before"
    },
    {
      "id": "a",
      "amount": 2,
      "fail": "none"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "retry",
    "ack"
  ],
  "total": 2,
  "processed": [
    "a"
  ]
}
```

### Example 3: lost acknowledgement after commit

Input to `solve`:
```json
{
  "total": 0,
  "deliveries": [
    {
      "id": "a",
      "amount": 2,
      "fail": "after"
    },
    {
      "id": "a",
      "amount": 2,
      "fail": "none"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "retry",
    "ack"
  ],
  "total": 2,
  "processed": [
    "a"
  ]
}
```

## Constraints

- 0–300 deliveries. IDs are nonempty ASCII strings.
- total and amounts are integers from -1000000 to 1000000. fail is none, before, or after.

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

- [Official documentation 1](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html)
