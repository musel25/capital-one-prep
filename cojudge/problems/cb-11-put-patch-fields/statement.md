# 11. Preserve field presence in a partial update

[Course list](/?course=capital-one-codebase-practice) · Level 3 · Medium · About 40 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 09–10. Distinguish an absent field from an explicit null value.

One function validates both replacement and partial-update requests. The starter loses an explicit PATCH value. Your objective is to distinguish absent fields from present fields while preserving validation, atomic updates, and earlier response snapshots.

Replacement and partial update need different rules for absent fields. A replacement describes the new representation. A partial update changes selected fields in the current representation. An absent key is also different from a key whose value is null. For example, absence can preserve an email while null clears it. Validate the entire change before writing any field. Otherwise one invalid field can leave a partial update behind. HTTP PATCH does not prescribe one universal document format; this exercise defines its own two-field patch format. Its PUT rule also supplies a documented default. Both choices must be explicit to API clients.

</details>

**Scenario:** A profile API lets an app update a user's name and email. PUT replaces the whole profile. PATCH changes only the fields it sends. `solve` processes a sequence of update requests for one profile.

> **Bug report:** "I removed my email in the app. The app said 'Saved', but my old email is still on my profile."

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

**What to fix:** The starter runs, but it has one intentional bug.

- Repair PATCH assignment for a present valid field.
- Preserve omission semantics, explicit null for email, empty email strings, and name validation.
- Keep PUT replacement and its null default.
- Do not allow null names, numeric zero as a field value, new keys, or email syntax validation.
- Keep each response independent of later state changes.

**Constraints:**

- 0–200 requests. Bodies are decoded JSON values with at most 10 fields.
- All strings have at most 100 ASCII characters. Initial profiles meet the same field limits.
- Each call starts with its supplied initial state. No network calls.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Start with `{"name": "Mia", "email": "m@x"}`. PATCH `{"email": ""}` produces an empty email. PATCH `{}` keeps it empty. PATCH `{"email": null}` clears it. PUT `{"name": "Noa"}` then replaces the profile with `{"name": "Noa", "email": null}`. Each successful response describes state at that point; the earlier empty-email response must remain empty.

### Read the existing code

In `solve`, inspect the validation block before any state update. Compare the PUT assignment with the PATCH loop over `("name", "email")`. Track `body`, `state`, and the dictionary stored in `out` as distinct roles. Locate the rejection `continue` and explain why no field may change before it.

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

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 31 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 12](/problems/cb-12-idempotency-conflicts).

Official documentation: [1](https://www.rfc-editor.org/rfc/rfc9110.html#name-put), [2](https://www.rfc-editor.org/rfc/rfc5789.html)
