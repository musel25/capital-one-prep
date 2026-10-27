# 22. Validate a request body

[Course list](/?course=capital-one-engineering-50) · Level 3 · Easy · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problem 21; strict Python type checks and regular expressions.

A JSON parser can accept a value that your API cannot use. Validation is a separate boundary. First check the whole body shape. Then check required fields, types, ranges, and unknown keys. Do not silently turn a string into a number unless the contract permits that conversion. Python needs care because bool is a subclass of int. Error ordering is part of this exercise's contract, so clients can compare responses reliably. The status choices below are a local API policy, not a claim that every service uses the same validation convention. A successful result includes explicit defaults for optional fields.

</details>

**Input:** `data` has:
- `bodies`: a list of decoded JSON values of any type.

**Return** one response per body.

**Rules**
- The body is not an object → `{"status": 400, "errors": ["body"]}`.
- Otherwise check the fields:
  - `account` (required): a string that fully matches `[a-z][a-z0-9_]{0,11}`.
  - `amount` (required): a JSON integer from 1 to 10000. Booleans and floats fail: `1` passes, but `1.0` and `1e0` fail.
  - `note` (optional, default `null`): `null` or an ASCII string of at most 20 characters.
  - Any other key is unknown.
- One or more checks fail → `{"status": 422, "errors": [...]}`. List only the failed checks, in this order: `account`, `amount`, `note`, `unknown`. Add one `unknown` entry if there is at least one unknown key.
- All checks pass → `{"status": 201, "body": {"account": ..., "amount": ..., "note": ...}}`. A success response has no `errors` field.

Do not trim or convert the input.

**Constraints:**

- 0–200 bodies. Every string and object key is ASCII and at most 100 characters.
- Numeric inputs are finite JSON numbers in [-100000,100000]. Decimal or exponent notation decodes as float and must fail the amount check.
- Bodies and field values may have any JSON type. Nested lists and objects have at most 10 elements.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 37 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool), [2](https://www.rfc-editor.org/rfc/rfc9110.html)
