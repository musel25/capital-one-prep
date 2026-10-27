# 10. Validate a body before building success

[Course list](/?course=capital-one-codebase-practice) · Level 3 · Easy · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 09. Read request bodies and the runtime validation checks from exercise 02.

The validator builds an ordered error list before it emits a success response. The starter accepts a prohibited amount type. Your objective is to trace the boundary between decoded input and an accepted API body. This exercise has no persistent write; the success branch is the boundary that would precede one in a service.

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

**What to fix:** The starter runs, but it has one intentional bug.

- Repair the amount type validation.
- Preserve the inclusive numeric bounds, account pattern, note default, fixed error order, and unknown-key rule.
- Keep 400 for a non-object and 422 for an invalid object.
- Do not coerce, trim, change status codes, or add storage.
- All input strings are ASCII under the existing constraints.

**Constraints:**

- 0–200 bodies. Every string and object key is ASCII and at most 100 characters.
- Numeric inputs are finite JSON numbers in [-100000,100000]. Decimal or exponent notation decodes as float and must fail the amount check.
- Bodies and field values may have any JSON type. Nested lists and objects have at most 10 elements.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

For `{"account": "ok_2", "amount": 3, "note": ""}`, expect status `201` and preserve the empty note. For `{"account": "Bad", "amount": 0, "note": 7, "extra": true}`, the error list is `["account", "amount", "note", "unknown"]`. No success body is produced for that input. Field validation must accumulate errors in contract order, regardless of input key order.

### Read the existing code

Inspect the non-dictionary branch in `solve` before its `.get` calls. Follow `account`, `amount`, and `note` into their checks. Find where unknown keys add one error. Then locate the final `if errors` decision. Explain why the current record's error list must start empty on every iteration.

### Test before and after the change

Predict responses for amount `1`, `true`, `1.0`, and `"1"` with the same valid account. Then test amounts `0`, `10000`, and `10001`. Combine several invalid fields in a body with reversed key order and assert the exact error list. Test absent, null, empty, 20-character, and 21-character notes. Put an invalid body before a valid body to detect error-list leakage. Confirm that errors and success bodies have different response shapes.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “A JSON amount written as `1.0` is valid because its mathematical value is an integer.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py` and my expected responses. Identify the validation stages before success is constructed. Cite file lines for outer shape, field checks, error order, and the success boundary. Review my assumptions without supplying a fix or writing tests. I will implement the amount repair.

### Technical completion checks

- Map every validation stage before the success response.
- Run type, range, error-order, and consecutive-body tests.
- Review unchanged input and response shape. This judge has no database side effects to verify.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 37 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 11](/problems/cb-11-put-patch-fields).

Official documentation: [1](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool), [2](https://www.rfc-editor.org/rfc/rfc9110.html)
