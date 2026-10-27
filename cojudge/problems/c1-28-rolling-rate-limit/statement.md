# 28. Rate limits with a rolling window

[Course list](/?course=capital-one-engineering-50) · Level 3 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 20 and 27; deque, dictionaries, and integer clocks.

A rolling limit counts accepted requests in a recent time interval. Its exact boundary matters. For the interval used here, a request at time t counts earlier accepted requests whose timestamps are greater than t minus the window. A timestamp exactly at that boundary has expired. A deque fits this rule because events arrive in time order and expire from the front. Keep one history per user. Rejected requests do not enter that history, so repeated rejection cannot push the next allowed time farther away. This sequential simulation checks the policy. A live service would also need atomic updates across simultaneous callers and shared storage across workers.

</details>

**Scenario:** A public API allows each user at most `limit` requests in a rolling window of `window` time units. `solve` decides whether to allow each request, and tells a rejected client how long to wait.

**Input:** `data` has:
- `limit`: a positive integer.
- `window`: a positive integer.
- `events`: a list of `{"time": int, "user": string}`, in time order.

**Rules:** each user can have at most `limit` accepted events in the window `(time - window, time]`. Every user's history starts empty. For each event:
1. Remove that user's accepted timestamps that are less than or equal to `time - window`.
2. If the number left is below `limit`, accept the event and add its timestamp. Otherwise reject it and do not add it.

**Return** one `{"allowed": bool, "remaining": int, "retry_after": int}` per event:
- `remaining`: the user's free capacity after this decision.
- `retry_after`: 0 if accepted. If rejected, the positive time until the user's oldest active accepted timestamp expires.

**Practice:** use a `deque`. The judge checks only the output.

**Constraints:**

- limit is 1–100, window is 1–10000, and there are 0–500 events.
- Times are integers from 0 through 1000000 and are globally nondecreasing; ties are allowed.
- User keys are case-sensitive nonempty ASCII strings of at most 30 characters.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 31 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3/library/collections.html#collections.deque)
