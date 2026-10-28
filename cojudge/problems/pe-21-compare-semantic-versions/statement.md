# 21. Compare release versions correctly

The update service must compare semantic versions without treating numeric components as plain text.

Implement `compare_versions(left, right)` for valid SemVer 2.0.0 strings. Return -1 if left precedes right, 1 if it follows, or 0 for equal precedence. Compare major, minor, then patch numerically. A release follows every prerelease with the same core. Compare prerelease identifiers from left to right: numeric identifiers compare numerically and precede nonnumeric identifiers; other identifiers use ASCII lexical order. If all shared identifiers are equal, the shorter prerelease precedes the longer one. Ignore build metadata after `+`. Inputs are guaranteed valid; do not add validation.

**Constraints:**

- Each input is an ASCII SemVer 2.0.0 string of at most 100 characters.
- Core numbers are canonical nonnegative integers through 1000000000.
- Prerelease identifiers contain ASCII letters, digits, or hyphens; numeric identifiers have no leading zeros.
- Build identifiers can have leading zeros.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `compare_versions`. **Run** checks the examples. **Submit** checks all 22 cases.
