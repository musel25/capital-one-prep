The create-user endpoint must report invalid fields before it writes a record.

Given a dictionary `payload`, return a list of invalid field names in this order: `name`, `email`, `age`.

- `name` is required. It must be a string that is nonempty after removal of surrounding spaces, tabs, carriage returns, and newlines.
- `email` is required. It must be a string with exactly one `@`, nonempty parts on both sides, and no spaces, tabs, carriage returns, or newlines. Do not apply other email rules.
- `age` is optional. If present, it must be an integer of zero or more. Booleans and floats are invalid.

Ignore other fields. Return an empty list for a valid request. Do not convert field types.

**Constraints:**

- `payload` is a JSON object with at most 20 fields.
- String values and keys contain ASCII characters. String values have at most 200 characters.
- Numeric values are between -1000000 and 1000000. Missing fields and `None` are allowed.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `validate_user`. **Run** checks the examples. **Submit** checks all 15 cases.
