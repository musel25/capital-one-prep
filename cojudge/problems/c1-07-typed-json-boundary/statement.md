# 07. Validate JSON before using TypedDict

[Course list](/?course=capital-one-engineering-50) · Level 1 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

TypedDict describes the expected keys and value types in a dictionary for a static type checker. It does not validate a decoded JSON value at runtime. A value from json.loads can still be a list, a number, or an object with missing fields. Put a validator at the boundary. Check the outer type before you read keys. Check each required field and then build a small accepted object. That object can have a TypedDict return annotation because the function has established its shape. Extra fields need a stated policy. This task ignores them and returns only the validated fields.

</details>

**Input:** `data` has:
- `records`: a list of any JSON values.

**Rules:** accept a record only if all of these are true:
- It is an object.
- It has `id`, a nonempty string.
- It has `amount`, a nonnegative integer. Booleans and floats are not integers for this rule. Integers have absolute value at most 1,000,000.

Extra keys do not cause a rejection.

**Return** `{"valid": [...], "rejected": [...]}`
- `valid`: one `{"id": string, "amount": int}` per accepted record, in input order. Keep only these two fields.
- `rejected`: the zero-based positions of the rejected records, in input order.

**Practice:** use `TypedDict` in your solution. The judge checks only the output.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/typing.html#typing.TypedDict)
