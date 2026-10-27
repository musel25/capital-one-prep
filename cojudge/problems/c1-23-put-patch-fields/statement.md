# 23. Replace or patch a profile

[Course list](/?course=capital-one-engineering-50) · Level 3 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 21–22; dictionary membership and atomic state changes.

Replacement and partial update need different rules for absent fields. A replacement describes the new representation. A partial update changes selected fields in the current representation. An absent key is also different from a key whose value is null. For example, absence can preserve an email while null clears it. Validate the entire change before writing any field. Otherwise one invalid field can leave a partial update behind. HTTP PATCH does not prescribe one universal document format; this exercise defines its own two-field patch format. Its PUT rule also supplies a documented default. Both choices must be explicit to API clients.

</details>

**Scenario:** A profile API lets an app update a user's name and email. PUT replaces the whole profile. PATCH changes only the fields it sends. `solve` processes a sequence of update requests for one profile.

**Input:** `data` has:
- `initial`: a valid profile `{"name": string, "email": string | null}`.
- `requests`: a list of `{"method": "PUT" | "PATCH", "body": any JSON}`.

**Valid body:** an object with no keys other than `name` and `email`.
- `name`, if present: an ASCII string of length 1–20.
- `email`, if present: `null` or an ASCII string of length 0–30. Do not check the email syntax.
- A PUT body must contain `name`.

**Rules**
- PUT replaces the whole profile. `email` is `null` when the body omits it.
- PATCH changes only the fields in the body. Omitted fields stay the same. `"email": null` clears the email. An empty PATCH body `{}` is valid.
- Invalid body → `{"status": 422, "body": {"error": "invalid"}}`. Nothing changes.
- Valid update → `{"status": 200, "body": the profile after the update}`.

**Return** `{"responses": [...], "state": the final profile}`.

**Constraints:**

- 0–200 requests. Bodies are decoded JSON values with at most 10 fields.
- All strings have at most 100 ASCII characters. Initial profiles meet the same field limits.
- Each call starts with its supplied initial state. No network calls.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 31 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.rfc-editor.org/rfc/rfc9110.html#name-put), [2](https://www.rfc-editor.org/rfc/rfc5789.html)
