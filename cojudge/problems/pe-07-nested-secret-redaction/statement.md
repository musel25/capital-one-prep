The request logger must remove secret values from nested payloads before it writes them.

Implement redact_secrets(value) for any JSON value. For each object key, compare its ASCII letters without regard to case. If the whole key equals password, token or secret, replace its entire value with the string '[REDACTED]'. Preserve the original key spelling. Do not inspect that replaced subtree. Recursively process values under all other object keys and every list element. Return scalar values unchanged, including strings that contain secret words. Matching does not trim whitespace or match substrings. Empty objects and lists remain empty. Do not change the input tree. Repeated calls must be independent and redacting an already redacted result must leave its JSON value unchanged.

**Constraints:**

- The input is a valid JSON tree with ASCII object keys.
- The maximum nesting depth is 10 and the tree has at most 1000 nodes.
- Inputs satisfy the contract. No input validation, file access or network calls are required.
- Floating-point values have at most six decimal places and an absolute value at most 1000000.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `redact_secrets`. **Run** checks the examples. **Submit** checks all 15 cases.
