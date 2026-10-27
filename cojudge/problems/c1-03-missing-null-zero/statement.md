# 03. Keep missing, null, and zero separate

[Course list](/?course=capital-one-engineering-50) · Level 1 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

A field can be absent, present with null, or present with zero. These states often have different meanings. Dictionary membership tells you whether a key exists. A value of None represents JSON null after decoding. Zero is a configured numeric value, even though it is false in a boolean condition. An expression such as value or default merges these states and can replace a valid zero. Write the decision in the same order as the contract: first check membership, then inspect the stored value. This makes defaults explicit and avoids an accidental change to a caller’s configuration.

</details>

**Input:** `data` has:
- `default`: a nonnegative integer.
- `records`: a list of objects. A record can have a `limit` key whose value is a nonnegative integer or `null`. Ignore all other keys.

**Rules:** resolve the limit of each record.
- No `limit` key → `default`.
- `limit` is `null` → `null`.
- `limit` is a number, including `0` → that number.

**Return** `{"limits": [...], "configured": int}`
- `limits`: the resolved limit of each record, in input order.
- `configured`: the number of records that have a `limit` key with a non-null value. A `0` counts.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
