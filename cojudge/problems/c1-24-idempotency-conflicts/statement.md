# 24. Replay writes with idempotency keys

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Medium · About 30 minutes**

**Before this problem:** Problems 20–23; state, validation, and response snapshots.

## Learn first

A client can lose a response after the server completes a write. Retrying the write without a stable identifier can create a second effect. An idempotency key names one logical request. The service stores the original body and result for that key. A retry with the same body gets the stored result. A different body must not silently reuse the key. The cache and the write need one atomic outcome in a real service. Here all operations are sequential and all bodies are valid. The exercise focuses on replay, conflicts, and identifier allocation. Cache expiration and concurrent requests are outside its scope.

## Your task

`requests` contains `{key:string, body:{to:string, amount:int}}`. All requests are valid. Process them in order with an initially empty key cache. A new key creates one transfer with consecutive id starting at 1. Return `{status:201, body:{id,to,amount}, replayed:false}`. An existing key with the same recipient and amount returns its original body with status 201 and `replayed:true`. An existing key with a different body returns `{status:409, body:{error:"key_conflict"}, replayed:false}`. A conflict changes nothing and consumes no id. Compare body fields, not serialized key order. Keys are case sensitive. Return `{responses:[...], transfers:[...]}` with transfers in creation order. This is a local application policy for a deterministic API simulation.

## Examples

### Example 1: same key and body replay one transfer

Input to `solve`:
```json
{
  "requests": [
    {
      "key": "k",
      "body": {
        "to": "a",
        "amount": 10
      }
    },
    {
      "key": "k",
      "body": {
        "to": "a",
        "amount": 10
      }
    }
  ]
}
```
Return:
```json
{
  "responses": [
    {
      "status": 201,
      "body": {
        "id": 1,
        "to": "a",
        "amount": 10
      },
      "replayed": false
    },
    {
      "status": 201,
      "body": {
        "id": 1,
        "to": "a",
        "amount": 10
      },
      "replayed": true
    }
  ],
  "transfers": [
    {
      "id": 1,
      "to": "a",
      "amount": 10
    }
  ]
}
```

### Example 2: same key with changed amount conflicts

Input to `solve`:
```json
{
  "requests": [
    {
      "key": "k",
      "body": {
        "to": "a",
        "amount": 10
      }
    },
    {
      "key": "k",
      "body": {
        "to": "a",
        "amount": 11
      }
    }
  ]
}
```
Return:
```json
{
  "responses": [
    {
      "status": 201,
      "body": {
        "id": 1,
        "to": "a",
        "amount": 10
      },
      "replayed": false
    },
    {
      "status": 409,
      "body": {
        "error": "key_conflict"
      },
      "replayed": false
    }
  ],
  "transfers": [
    {
      "id": 1,
      "to": "a",
      "amount": 10
    }
  ]
}
```

### Example 3: different keys permit same body

Input to `solve`:
```json
{
  "requests": [
    {
      "key": "k",
      "body": {
        "to": "a",
        "amount": 10
      }
    },
    {
      "key": "j",
      "body": {
        "to": "a",
        "amount": 10
      }
    }
  ]
}
```
Return:
```json
{
  "responses": [
    {
      "status": 201,
      "body": {
        "id": 1,
        "to": "a",
        "amount": 10
      },
      "replayed": false
    },
    {
      "status": 201,
      "body": {
        "id": 2,
        "to": "a",
        "amount": 10
      },
      "replayed": false
    }
  ],
  "transfers": [
    {
      "id": 1,
      "to": "a",
      "amount": 10
    },
    {
      "id": 2,
      "to": "a",
      "amount": 10
    }
  ]
}
```

## Constraints

- 0–200 requests. Keys and recipients are nonempty ASCII strings of at most 40 characters.
- Amounts are integers from 1 through 1000000; booleans are excluded.
- Bodies contain exactly to and amount. Keys never expire during one call.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 29 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.stripe.com/api/idempotent_requests)
