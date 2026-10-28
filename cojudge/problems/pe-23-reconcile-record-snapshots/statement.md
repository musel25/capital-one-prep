The sync client needs an action plan for local and remote records without inferring deletions.

Implement `reconcile_records(local, remote)`. Each list contains records with `id`, `version`, and `checksum`. IDs are unique within each list. For an ID found only locally, upload it. For an ID found only remotely, download it. For an ID on both sides, upload when its local version is higher and download when its remote version is higher. When versions are equal, matching checksums require no action; different checksums produce a conflict. Version comparison takes priority over checksum comparison. Return `{'upload': [...], 'download': [...], 'conflicts': [...]}` with IDs in ASCII lexical order within each list. Compare IDs and checksums exactly. Do not infer deletions. Do not change the input.

**Constraints:**

- Each list has 0 through 200 records with all three required fields.
- IDs are nonempty ASCII strings; checksums are ASCII strings and can be empty.
- Versions are integers from 0 through 1000000000; booleans are not versions.
- IDs are unique within each list, but can occur in both lists.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `reconcile_records`. **Run** checks the examples. **Submit** checks all 16 cases.
