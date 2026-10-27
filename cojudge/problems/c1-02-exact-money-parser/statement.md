# 02. Parse money into exact cents

[Course list](/?course=capital-one-engineering-50) · Level 1 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

Binary floating point cannot represent many decimal fractions exactly. Money from a text boundary is easier to handle with Decimal. First validate the allowed text format. Then construct Decimal from that text, multiply by 100, and convert the exact result to an integer. This order keeps the cents. Constructing Decimal from a float would preserve the float error. Format validation is a separate concern: Decimal accepts forms that an API might forbid, such as an exponent. This task permits one or two fractional digits and rejects every other text format. Once parsed, integer cents support exact addition and comparison.

</details>

**Scenario:** A bank's import tool reads amounts that people typed into a form, such as `"12.34"`. A float cannot store cents exactly, so the tool converts the text to an integer number of cents. Text that does not match the strict format becomes `null`, so the import can flag it for review.

**Input:** `data` has:
- `amounts`: a list of JSON values. Strings have at most 30 characters.

**Rules**
- A valid amount is a string that fully matches the ASCII pattern `-?[0-9]{1,12}(?:\.[0-9]{1,2})?`: an optional `-`, 1–12 digits, then optionally `.` and 1–2 digits.
- Leading zeros and negative zero are valid: `"007"` → `700`, `"-0"` → `0`.
- Invalid: spaces, a leading `+`, exponent notation, Unicode digits, and every non-string value.
- Convert each valid amount to exact integer cents: `"1.5"` → `150`, `"-0.05"` → `-5`.

**Return** `{"cents": [...]}` with one entry per amount, in input order: the integer cents for a valid amount, or `null` for an invalid one.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 27 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3/library/decimal.html), [2](https://docs.python.org/3/library/re.html#re.fullmatch)
