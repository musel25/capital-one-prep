# 06. Read quoted CSV records

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Easy · About 20 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

CSV fields can contain commas, quotes, and line breaks. Splitting text at commas or splitting it into lines before parsing destroys those fields. The csv module reads records according to the quoting rules. A quoted double quote is written as two double quotes. Open a text stream with newline handling that lets the CSV reader see the original line endings. The reader returns strings, so convert a numeric column only after parsing the record. Keep aggregation separate from parsing. A dictionary preserves the first insertion order of account IDs, which gives a simple way to return totals in first-seen order.

## Your task

`data.csv` is valid comma-separated CSV text. Its first record is exactly the two fields `account,amount`. Each later record has exactly two fields. `account` is a string of at most 1,000 characters, including an empty string, comma, quote, or line break. `amount` is an optionally negative ASCII integer string with absolute value at most 1,000,000 and at most 20 characters, including any sign and leading zeros. Standard double-quote escaping applies. Record separators are LF or CRLF. There are no blank records. The last record may omit its separator. Return a list of `{"account": string, "total": integer}`. Sum each account’s amounts. Keep accounts in first-seen order.

## Examples

### Example 1: quoted comma and repeated account

Input to `solve`:
```json
{
  "csv": "account,amount\n\"Acme, West\",10\nBeta,3\n\"Acme, West\",-4\n"
}
```
Return:
```json
[
  {
    "account": "Acme, West",
    "total": 6
  },
  {
    "account": "Beta",
    "total": 3
  }
]
```

### Example 2: quote and embedded line break

Input to `solve`:
```json
{
  "csv": "account,amount\n\"a\"\"b\",7\n\"line\nbreak\",2\n"
}
```
Return:
```json
[
  {
    "account": "a\"b",
    "total": 7
  },
  {
    "account": "line\nbreak",
    "total": 2
  }
]
```

### Example 3: header only

Input to `solve`:
```json
{
  "csv": "account,amount\n"
}
```
Return:
```json
[]
```

## Constraints

- At most 100 data records after the header.
- Each decoded account field has at most 1,000 characters. Each amount field has at most 20 characters.
- The complete CSV text has at most 200,000 characters. All text follows the stated valid CSV format.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 27 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3.11/library/csv.html)
