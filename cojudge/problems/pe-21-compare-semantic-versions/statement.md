The update service must compare semantic versions without treating numeric components as plain text.

Implement `compare_versions(left, right)` for valid SemVer 2.0.0 strings. Return `-1`, `1`, or `0` when the left version has lower, higher, or equal precedence.

Compare major, minor, and patch numerically. A release follows every prerelease with the same core. Compare prerelease identifiers from left to right:

- Numeric identifiers compare numerically and precede nonnumeric identifiers.
- Other identifiers use ASCII lexical order.
- If shared identifiers are equal, the shorter prerelease comes first.

Ignore build metadata after `+`.

**Constraints:**

- Each input is an ASCII SemVer 2.0.0 string of at most 100 characters.
- Core numbers are canonical nonnegative integers through 1000000000.
- Prerelease identifiers contain ASCII letters, digits, or hyphens; numeric identifiers have no leading zeros.
- Build identifiers can have leading zeros.
- Do not change input objects or their nested values. Each call starts with fresh state.
