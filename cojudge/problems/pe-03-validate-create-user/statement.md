The create-user endpoint must report invalid fields before it writes a record.

Implement `validate_user(payload)`. Return invalid field names in the order `name`, `email`, `age`.

- `name` is required. It must be a string that remains nonempty after removal of surrounding spaces, tabs, carriage returns, and newlines.
- `email` is required. It must be a string with exactly one `@`, nonempty parts on both sides, and no spaces, tabs, carriage returns, or newlines. Apply no other email rules.
- `age` is optional. If present, it must be a nonnegative integer. Booleans and floats are invalid.

Ignore other fields. Keep field types unchanged. Return an empty list for a valid request.

**Constraints:**

- `payload` is a JSON object with at most 20 fields.
- String values and keys contain ASCII characters. String values have at most 200 characters.
- Numeric values are between -1000000 and 1000000. Missing fields and `None` are allowed.
- Do not change input objects or their nested values. Each call starts with fresh state.
