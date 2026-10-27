# 01. Strict numeric fields

[Course list](/?course=capital-one-engineering-50) · Level 1 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

Python treats bool as a subclass of int. As a result, isinstance(True, int) returns True. This can turn a flag into one cent when you validate a numeric field. At a JSON boundary, decide which exact types the contract permits. Use type(value) is int when a field requires an integer and must exclude booleans. Validate the range in a separate condition. Do not convert strings or round floats unless the contract requires it. Keep rejected positions so a caller can identify each bad field. Zero is a valid amount in this task. An empty batch has a total of zero.

</details>

**Input:** `data` has:
- `values`: a list of JSON values. Integers have absolute value at most 1,000,000,000.

**Rules**
- Accept a value only if its exact Python type is `int` and it is at least 0.
- Reject everything else: booleans, floats, strings, null, lists, objects, and negative integers.

**Return** `{"total": int, "rejected": [int]}`
- `total`: the sum of the accepted values.
- `rejected`: the zero-based positions of the rejected values, in input order.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)
