# 28. Rate limits with a rolling window

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Medium · About 30 minutes**

**Before this problem:** Problems 20 and 27; deque, dictionaries, and integer clocks.

## Learn first

A rolling limit counts accepted requests in a recent time interval. Its exact boundary matters. For the interval used here, a request at time t counts earlier accepted requests whose timestamps are greater than t minus the window. A timestamp exactly at that boundary has expired. A deque fits this rule because events arrive in time order and expire from the front. Keep one history per user. Rejected requests do not enter that history, so repeated rejection cannot push the next allowed time farther away. This sequential simulation checks the policy. A live service would also need atomic updates across simultaneous callers and shared storage across workers.

## Your task

Input has positive `limit`, positive `window`, and ordered `events` containing `{time:int, user:string}`. Each user may have at most limit accepted events in `(time-window, time]`. Before each event, remove that user's accepted timestamps less than or equal to time-window. Accept the event if the remaining count is below limit, then add its timestamp. Reject otherwise and do not add it. Return one object per event: `{allowed:bool, remaining:int, retry_after:int}`. remaining is available capacity after this decision. For accepted events retry_after is 0. For rejected events it is the positive time until the oldest active accepted timestamp expires. Histories start empty. Use a deque in your Python implementation; the output judge cannot enforce this data structure.

## Examples

### Example 1: third call exceeds window

Input to `solve`:
```json
{
  "limit": 2,
  "window": 10,
  "events": [
    {
      "time": 0,
      "user": "a"
    },
    {
      "time": 1,
      "user": "a"
    },
    {
      "time": 2,
      "user": "a"
    }
  ]
}
```
Return:
```json
[
  {
    "allowed": true,
    "remaining": 1,
    "retry_after": 0
  },
  {
    "allowed": true,
    "remaining": 0,
    "retry_after": 0
  },
  {
    "allowed": false,
    "remaining": 0,
    "retry_after": 8
  }
]
```

### Example 2: timestamp at left boundary expires

Input to `solve`:
```json
{
  "limit": 1,
  "window": 10,
  "events": [
    {
      "time": 0,
      "user": "a"
    },
    {
      "time": 10,
      "user": "a"
    }
  ]
}
```
Return:
```json
[
  {
    "allowed": true,
    "remaining": 0,
    "retry_after": 0
  },
  {
    "allowed": true,
    "remaining": 0,
    "retry_after": 0
  }
]
```

### Example 3: users have independent windows

Input to `solve`:
```json
{
  "limit": 1,
  "window": 10,
  "events": [
    {
      "time": 0,
      "user": "a"
    },
    {
      "time": 0,
      "user": "b"
    },
    {
      "time": 1,
      "user": "a"
    }
  ]
}
```
Return:
```json
[
  {
    "allowed": true,
    "remaining": 0,
    "retry_after": 0
  },
  {
    "allowed": true,
    "remaining": 0,
    "retry_after": 0
  },
  {
    "allowed": false,
    "remaining": 0,
    "retry_after": 9
  }
]
```

## Constraints

- limit is 1–100, window is 1–10000, and there are 0–500 events.
- Times are integers from 0 through 1000000 and are globally nondecreasing; ties are allowed.
- User keys are case-sensitive nonempty ASCII strings of at most 30 characters.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 31 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3/library/collections.html#collections.deque)
