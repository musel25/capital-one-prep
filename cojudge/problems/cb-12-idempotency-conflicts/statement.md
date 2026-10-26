# 12. Trace request identity through a replay cache

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 3 · Medium · About 40 minutes**

**Before this problem:** Exercise 11. Trace a request through validation, lookup, and a state update.

## Learn first

The cache connects an idempotency key to the first body and result. The starter confuses a conflicting request with a replay. Your objective is to trace all state affected by new requests, replays, and conflicts, then repair the identity comparison.

A client can lose a response after the server completes a write. Retrying the write without a stable identifier can create a second effect. An idempotency key names one logical request. The service stores the original body and result for that key. A retry with the same body gets the stored result. A different body must not silently reuse the key. The cache and the write need one atomic outcome in a real service. Here all operations are sequential and all bodies are valid. The exercise focuses on replay, conflicts, and identifier allocation. Cache expiration and concurrent requests are outside its scope.

### Worked trace

Submit key `k` with recipient `Ada` and amount `4`: create transfer id `1`. Repeat that key and body: replay id `1`. Submit key `k` with recipient `Ada` and amount `5`: return 409. Submit key `m` with recipient `Bo` and amount `2`: create id `2`. There are four responses but only two transfers. Neither the replay nor the conflict allocates an ID.

### Read the existing code

Inspect `cache`, `transfers`, and `out` in `solve`. Trace the existing-key branch through `saved_body` and `result`. Then follow the new-key branch to ID allocation, cache insertion, and response construction. Identify which stored data establishes identity and which stored data supplies a replay response.

## Your task

### Scoped repair

Repair comparison of a request body with the saved body. Keep both recipient and amount significant. Preserve case-sensitive keys, original results, creation order, and consecutive IDs. A conflict must not replace the cache or consume an ID. Do not serialize dictionaries to compare their key order. Do not add expiry, retries, persistent storage, or concurrency.

### Required behavior

`requests` contains `{key:string, body:{to:string, amount:int}}`. All requests are valid. Process them in order with an initially empty key cache. A new key creates one transfer with consecutive id starting at 1. Return `{status:201, body:{id,to,amount}, replayed:false}`. An existing key with the same recipient and amount returns its original body with status 201 and `replayed:true`. An existing key with a different body returns `{status:409, body:{error:"key_conflict"}, replayed:false}`. A conflict changes nothing and consumes no id. Compare body fields, not serialized key order. Keys are case sensitive. Return `{responses:[...], transfers:[...]}` with transfers in creation order. This is a local application policy for a deterministic API simulation.

### Test before and after the change

Write the full expected responses for an original request, an amount-only change, and a replay of the original body. The final replay tests whether the conflict corrupted the cache. Test recipient-only changes, identical bodies with different keys, key case changes, and bodies with reversed field order. After a conflict, create a new key and check its ID. Assert transfers as well as response statuses; correct error output can hide an unwanted stored write.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “If the same body is sent under a new key, the service should replay the existing transfer.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py` and my expected request sequence. Trace which branches read and write `cache`, `transfers`, and `out`. Cite file lines. Check whether my cases distinguish replay from conflict and detect an ID gap. Do not supply the comparison, implementation, or test code.

### Technical completion checks

- Map cache, transfer, and response changes for all three request classes.
- Run conflict-then-replay and conflict-then-create sequences.
- Review ID allocation and saved-result preservation. Sequential judge checks do not prove safe concurrent idempotency.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Next, complete lab05 and lab06 from the guide.

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
