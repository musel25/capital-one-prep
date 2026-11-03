**The ticket.** The create-user endpoint must reject bad input before it saves a user.

**Why it matters.** Bad data in a database causes errors later, far from the cause. Report all bad fields at once, so the client can fix them in one try.

### Your task

Write `validate_user(payload)`. Return a list with the names of the invalid fields, in the order `name`, `email`, `age`. Return `[]` when all fields are valid.

1. `name` is required. It must be a string. After `.strip()`, it must not be empty.
2. `email` is required. It must be a string with exactly one `@`, text before and after the `@`, and no whitespace (space, tab, `\r`, `\n`). Do not strip the email.
3. `age` is optional. If the key is there, the value must be an `int` that is `0` or more. `True`, `1.0`, `"4"`, and `None` are not valid ages.
4. Ignore all other fields. Do not convert types.

**Constraints:**

- `payload` is a dictionary with at most 20 fields. Values can be any JSON value.
