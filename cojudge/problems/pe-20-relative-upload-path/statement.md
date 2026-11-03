**The ticket.** The upload endpoint gets a file path from the user and saves the file below the upload folder.

**Why it matters.** If a user sends `../../etc/passwd`, the server can write outside the upload folder. This attack is called path traversal. Clean the path as text, and reject any path that leaves the folder.

### Your task

Write `resolve_upload_path(path)`. Return a clean relative path, or `None` when you reject the path.

1. Reject the path if it starts with `/`, or if it contains a backslash (`\`) or the NUL character (`\x00`).
2. Split the path on `/`. Process the parts in order:
   - Skip empty parts and `.` parts.
   - For `..`, remove the last kept part. If no part is kept, reject the path at once. Later parts cannot repair it.
   - Keep every other part exactly as it is.
3. Join the kept parts with `/`. If no part is kept, return `None`.

Only exact `.` and `..` are special. `...` and `..hidden` are normal names. Do not use the file system.

**Constraints:**

- `path` has 0–500 ASCII characters.
