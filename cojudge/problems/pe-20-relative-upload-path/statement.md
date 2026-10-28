The upload endpoint must reject paths that escape the upload root before it constructs a relative destination.

Implement `resolve_upload_path(path)`. Return a normalized relative POSIX path, or `None` when rejected or no components remain.

Reject a leading slash, any backslash, or any NUL character. Split on `/` and process components in order:

- Ignore empty components and exact `.` components.
- For exact `..`, remove the previous normal component. Reject immediately if none exists; later components cannot repair the escape.
- Keep every other component exactly as supplied.

Join remaining components with `/`. Empty input returns `None`. Operate on the string only. Do not access the filesystem, resolve symlinks, expand variables, or interpret URL encoding.

**Constraints:**

- path is an ASCII string with 0–500 characters from the stated character set.
- Only exact '.' and '..' components have special meaning.
- Characters are ASCII letters, digits, `.`, `_`, `-`, `/`, backslash, or NUL.
- Do not change input objects or their nested values. Each call starts with fresh state.
