The request logger must remove secret values from nested payloads before it writes them.

Implement `redact_secrets(value)` for any JSON value.

For each object key, compare ASCII letters without regard to case. If the whole key is `password`, `token`, or `secret`, replace its entire value with `'[REDACTED]'`. Keep the original key spelling and do not inspect the replaced subtree. Do not trim keys or match substrings.

Recursively process other object values and list elements. Keep scalars unchanged, including strings that contain secret words. Keep empty objects and lists empty. Redacting an already redacted result must leave its JSON value unchanged.

**Constraints:**

- The input is a valid JSON tree with ASCII object keys.
- The maximum nesting depth is 10 and the tree has at most 1000 nodes.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Do not change input objects or their nested values. Each call starts with fresh state.
