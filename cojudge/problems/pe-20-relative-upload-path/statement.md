The upload endpoint must reject paths that escape the upload root before it constructs a relative destination.

Implement resolve_upload_path(path). Return a normalized relative POSIX path or null if it is rejected or has no remaining components. Reject a leading slash, any backslash or any NUL character. Split the string on '/'. Ignore empty components and exact '.' components. For an exact '..' component, remove the prior normal component. If none exists, reject immediately; later components cannot repair that escape. Keep all other components exactly as supplied. Join the remaining components with '/'. Return null when none remain. Empty input is valid and returns null. This is a string operation only. Do not access the filesystem, resolve symlinks, expand variables or interpret URL encoding. Inputs contain only ASCII letters, digits, '.', '_', '-', '/', backslash or NUL.

**Constraints:**

- path is an ASCII string with 0–500 characters from the stated character set.
- Only exact '.' and '..' components have special meaning.
- Use no filesystem, environment, network or current-directory state. Each call is independent.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `resolve_upload_path`. **Run** checks the examples. **Submit** checks all 20 cases.
