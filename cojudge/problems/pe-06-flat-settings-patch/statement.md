# 06. Apply a settings patch

The settings endpoint must distinguish deletion from valid false, zero and empty replacement values.

Implement apply_settings_patch(settings, patch). Both arguments are JSON objects with string keys and arbitrary JSON values. Return a new settings object. Start with all existing entries. For each patch entry, remove the key if its value is null. Removing an absent key does nothing. Otherwise set the key to that value, replacing any existing value. Apply these rules only at the top level: nested objects and lists replace entire values, and null inside a nested value is retained. Unpatched entries remain unchanged, including existing null values. Keys are case-sensitive and may be empty strings. Do not change settings, patch or their nested values. An empty patch still returns a new object. Each call is independent.

**Constraints:**

- Each top-level object contains 0–200 keys.
- All values are valid JSON values; objects are not merged recursively.
- Inputs satisfy the contract. No input validation or external storage is required.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `apply_settings_patch`. **Run** checks the examples. **Submit** checks all 15 cases.
