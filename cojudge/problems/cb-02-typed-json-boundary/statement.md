# 02. Find the runtime validation boundary

[Course list](/?course=capital-one-codebase-practice) · Level 1 · Easy · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 01. Read dictionary keys, return values, and rejection paths.

This program separates one-record validation from batch processing. `validate` returns an accepted `Entry` or `None`; `solve` records the result. The starter accepts a value that the amount rule excludes. Your objective is to locate the runtime check that must enforce the rule.

TypedDict describes the expected keys and value types in a dictionary for a static type checker. It does not validate a decoded JSON value at runtime. A value from json.loads can still be a list, a number, or an object with missing fields. Put a validator at the boundary. Check the outer type before you read keys. Check each required field and then build a small accepted object. That object can have a TypedDict return annotation because the function has established its shape. Extra fields need a stated policy. This task ignores them and returns only the validated fields.

</details>

**Scenario:** A partner bank sends payment records to your API as JSON. Some records are broken: wrong types, missing fields, or not objects at all. `solve` is the boundary check. It keeps the clean records (only `id` and `amount`) and reports the positions of the rejected ones, so the partner can send them again.

> **Bug report:** "We sent a record with `"amount": true` by mistake. Your API accepted it instead of rejecting it."

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

**What to fix:** The starter runs, but it has one intentional bug.

- Repair the amount acceptance check in `validate`.
- Keep the `Entry` model and the caller's `None` convention.
- Do not coerce strings or floats.
- Preserve zero, valid duplicate IDs, and any nonempty ID string.
- Keep only the two accepted fields.
- Do not add trimming or ID uniqueness rules.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Trace records `[7, {"id": "Q", "amount": 0, "debug": true}, {"id": "R", "amount": 1.0}]`. Position `0` fails the outer shape check. Position `1` becomes `{"id": "Q", "amount": 0}`; the extra field is absent from the result. Position `2` fails the amount type rule. Thus `valid` has one entry and `rejected` is `[0, 2]`. The annotation does not make these decisions.

### Read the existing code

Inspect the `Entry` declaration, the return paths in `validate`, and the `enumerate` loop in `solve`. Find where the outer object shape is checked before `.get` is used. Find where a new accepted dictionary is built. Distinguish a rejected position from an accepted record's `id`.

### Test before and after the change

Make a table for amounts `0`, `-1`, `true`, `false`, `1.0`, `"1"`, null, and an absent amount. Predict acceptance before Run. Use a valid ID in these cases so one rule is under test. Separately test a non-object, an empty ID, a space-only ID, and extra keys. Place a valid record between two invalid records to check the original rejection positions.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “A string containing only one space is an invalid ID, because an ID must contain visible text.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`, including `Entry`, `validate`, and `solve`. Explain which checks establish an `Entry` at runtime. Cite file lines for each rejection path and the accepted-object construction. Identify assumptions made by the caller. Do not write a validator, a repair, or tests. I will write the boundary cases.

### Technical completion checks

- Write an acceptance table before changing validate.
- Run cases that distinguish integers, booleans, and floats.
- Review the Entry construction and rejection positions. Judge results do not prove correct use of TypedDict.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 03](/problems/cb-03-dataclass-list-isolation).

Official documentation: [1](https://docs.python.org/3.11/library/typing.html#typing.TypedDict)
