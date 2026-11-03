**The ticket.** A PATCH request changes only some user settings. A value of `null` (`None`) means "delete this setting".

**Why it matters.** `False`, `0`, and `""` are real values. A common bug uses `if value:` and deletes them by mistake. Then a user cannot turn a setting off.

### Your task

Write `apply_settings_patch(settings, patch)`. Return a new settings dictionary. Do not change the inputs.

1. Start with a copy of `settings`.
2. For each key in `patch`:
   - If the value is `None`, remove the key. If the key is not there, do nothing.
   - Otherwise, set the key to the value. This replaces an old value or adds a new key.
3. Change only the top level. A dictionary in the patch replaces the whole old value. Do not merge it.
4. Keep all other settings unchanged, also settings whose value is `None`.

**Constraints:**

- Both arguments are dictionaries with 0–200 string keys. Values can be any JSON value.
