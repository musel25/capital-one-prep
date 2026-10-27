# 06. Read quoted CSV records

[Course list](/?course=capital-one-engineering-50) · Level 1 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, and functions.

CSV fields can contain commas, quotes, and line breaks. Splitting text at commas or splitting it into lines before parsing destroys those fields. The csv module reads records according to the quoting rules. A quoted double quote is written as two double quotes. Open a text stream with newline handling that lets the CSV reader see the original line endings. The reader returns strings, so convert a numeric column only after parsing the record. Keep aggregation separate from parsing. A dictionary preserves the first insertion order of account IDs, which gives a simple way to return totals in first-seen order.

</details>

**Scenario:** Finance exports transactions from a spreadsheet as CSV text: one row per transaction, with an account name and an amount. Account names can contain commas, quotes, and line breaks, so splitting each line on `,` gives wrong results. `solve` produces the total of each account for the monthly report.

**Input:** `data` has:
- `csv`: valid CSV text.
  - The first record (the header) is exactly `account,amount`.
  - Every later record has exactly two fields.
  - `account` is a string of at most 1,000 characters. It can be empty or contain a comma, a quote, or a line break.
  - `amount` is an ASCII integer string, optionally negative, with absolute value at most 1,000,000. It has at most 20 characters, including any sign and leading zeros.
  - Standard double-quote escaping applies: `""` inside a quoted field is one `"`.
  - Records are separated by LF or CRLF. There are no blank records. The last record may have no separator.

**Return** a list of `{"account": string, "total": int}`
- `total` is the sum of that account's amounts.
- Accounts are in the order they first appear.

**Constraints:**

- At most 100 data records after the header.
- Each decoded account field has at most 1,000 characters. Each amount field has at most 20 characters.
- The complete CSV text has at most 200,000 characters. All text follows the stated valid CSV format.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 27 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/csv.html)
