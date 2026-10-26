# 23. Replace or patch a profile

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Medium · About 30 minutes**

**Before this problem:** Problems 21–22; dictionary membership and atomic state changes.

## Learn first

Replacement and partial update need different rules for absent fields. A replacement describes the new representation. A partial update changes selected fields in the current representation. An absent key is also different from a key whose value is null. For example, absence can preserve an email while null clears it. Validate the entire change before writing any field. Otherwise one invalid field can leave a partial update behind. HTTP PATCH does not prescribe one universal document format; this exercise defines its own two-field patch format. Its PUT rule also supplies a documented default. Both choices must be explicit to API clients.

## Your task

`initial` is a valid profile `{name:string, email:string|null}`. `requests` contains `{method:"PUT"|"PATCH", body:JSON}`. A valid body is an object with only name and email. If present, name must be an ASCII string of length 1–20. If present, email must be null or an ASCII string of length 0–30; no email syntax check is required. PUT requires name and replaces the profile, with email defaulting to null. PATCH leaves omitted fields unchanged; explicit null clears email. Empty PATCH is valid. Invalid bodies return `{status:422, body:{error:"invalid"}}` and change nothing. Valid updates return `{status:200, body:profile_snapshot}`. Return `{responses:[...], state:final_profile}`.

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
