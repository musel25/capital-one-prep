# 11. Preserve field presence in a partial update

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 3 · Medium · About 40 minutes**

**Before this problem:** Exercises 09–10. Distinguish an absent field from an explicit null value.

## Learn first

One function validates both replacement and partial-update requests. The starter loses an explicit PATCH value. Your objective is to distinguish absent fields from present fields while preserving validation, atomic updates, and earlier response snapshots.

Replacement and partial update need different rules for absent fields. A replacement describes the new representation. A partial update changes selected fields in the current representation. An absent key is also different from a key whose value is null. For example, absence can preserve an email while null clears it. Validate the entire change before writing any field. Otherwise one invalid field can leave a partial update behind. HTTP PATCH does not prescribe one universal document format; this exercise defines its own two-field patch format. Its PUT rule also supplies a documented default. Both choices must be explicit to API clients.

### Worked trace

Start with `{"name": "Mia", "email": "m@x"}`. PATCH `{"email": ""}` produces an empty email. PATCH `{}` keeps it empty. PATCH `{"email": null}` clears it. PUT `{"name": "Noa"}` then replaces the profile with `{"name": "Noa", "email": null}`. Each successful response describes state at that point; the earlier empty-email response must remain empty.

### Read the existing code

In `solve`, inspect the validation block before any state update. Compare the PUT assignment with the PATCH loop over `("name", "email")`. Track `body`, `state`, and the dictionary stored in `out` as distinct roles. Locate the rejection `continue` and explain why no field may change before it.

## Your task

### Scoped repair

Repair PATCH assignment for a present valid field. Preserve omission semantics, explicit null for email, empty email strings, and name validation. Keep PUT replacement and its null default. Do not allow null names, numeric zero as a field value, new keys, or email syntax validation. Keep each response independent of later state changes.

### Required behavior

`initial` is a valid profile `{name:string, email:string|null}`. `requests` contains `{method:"PUT"|"PATCH", body:JSON}`. A valid body is an object with only name and email. If present, name must be an ASCII string of length 1–20. If present, email must be null or an ASCII string of length 0–30; no email syntax check is required. PUT requires name and replaces the profile, with email defaulting to null. PATCH leaves omitted fields unchanged; explicit null clears email. Empty PATCH is valid. Invalid bodies return `{status:422, body:{error:"invalid"}}` and change nothing. Valid updates return `{status:200, body:profile_snapshot}`. Return `{responses:[...], state:final_profile}`.

### Test before and after the change

Predict a sequence with missing email, null email, and empty email. Assert every response and the final state. Use a non-null starting email so an ignored clear is visible. Pair `PATCH {}` with `PUT {}` to check their different requirements. Submit a valid new name with an invalid email and check that neither field changes. Test numeric zero as invalid input; this two-field contract has no numeric PATCH field. Finish with a later valid update to test continued processing after rejection.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “An empty PATCH and an empty PUT are equivalent because both request no explicit field changes.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py` and my learner-written diff. Trace absent, null, and empty email through validation and mutation. Cite file lines for each path. Review whether PUT behavior, rejection atomicity, and response snapshots remain compatible. Do not write a patch or replacement implementation.

### Technical completion checks

- Write separate presence rules for PUT and PATCH.
- Run absent, null, empty, invalid, and multi-request snapshot cases.
- Review the diff for compatibility beyond the seeded defect. Passing final-state checks alone do not prove correct earlier responses.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 12](/problems/cb-12-idempotency-conflicts).

## Examples

### Example 1: PATCH keeps omitted email

Input to `solve`:
```json
{
  "initial": {
    "name": "Ada",
    "email": "a@x"
  },
  "requests": [
    {
      "method": "PATCH",
      "body": {
        "name": "Bo"
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
      "status": 200,
      "body": {
        "name": "Bo",
        "email": "a@x"
      }
    }
  ],
  "state": {
    "name": "Bo",
    "email": "a@x"
  }
}
```

### Example 2: PUT resets omitted email

Input to `solve`:
```json
{
  "initial": {
    "name": "Ada",
    "email": "a@x"
  },
  "requests": [
    {
      "method": "PUT",
      "body": {
        "name": "Bo"
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
      "status": 200,
      "body": {
        "name": "Bo",
        "email": null
      }
    }
  ],
  "state": {
    "name": "Bo",
    "email": null
  }
}
```

### Example 3: explicit null clears email

Input to `solve`:
```json
{
  "initial": {
    "name": "Ada",
    "email": "a@x"
  },
  "requests": [
    {
      "method": "PATCH",
      "body": {
        "email": null
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
      "status": 200,
      "body": {
        "name": "Ada",
        "email": null
      }
    }
  ],
  "state": {
    "name": "Ada",
    "email": null
  }
}
```

## Constraints

- 0–200 requests. Bodies are decoded JSON values with at most 10 fields.
- All strings have at most 100 ASCII characters. Initial profiles meet the same field limits.
- Each call starts with its supplied initial state. No network calls.

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

- [Official documentation 1](https://www.rfc-editor.org/rfc/rfc9110.html#name-put)
- [Official documentation 2](https://www.rfc-editor.org/rfc/rfc5789.html)
