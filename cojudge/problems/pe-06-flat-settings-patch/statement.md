The settings endpoint must distinguish deletion from valid false, zero and empty replacement values.

Implement `apply_settings_patch(settings, patch)`. Return a new settings object, even when the patch is empty.

Start with the existing entries. For each patch key:

- A `None` value removes the key. Removing an absent key does nothing.
- Any other value replaces the existing value or adds a new entry. Keep `False`, zero, and empty values.

Apply the patch only at the top level. Nested objects and lists replace entire values; keep `None` inside them. Keep unpatched entries, including existing `None` values. Compare keys exactly; empty keys are valid.

**Constraints:**

- Each top-level object contains 0–200 keys.
- All values are valid JSON values; objects are not merged recursively.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Both arguments are JSON objects with string keys and arbitrary JSON values.
- Do not change input objects or their nested values. Each call starts with fresh state.
