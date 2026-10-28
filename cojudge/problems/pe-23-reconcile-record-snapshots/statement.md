The sync client needs an action plan for local and remote records without inferring deletions.

Implement `reconcile_records(local, remote)`. Each list contains records with `id`, `version`, and `checksum`. Return `{'upload': [...], 'download': [...], 'conflicts': [...]}`.

- An ID found only locally needs an upload. An ID found only remotely needs a download.
- For an ID on both sides, upload if its local version is higher; download if its remote version is higher.
- Equal versions with equal checksums need no action. Equal versions with different checksums produce a conflict.

Compare versions before checksums. Compare IDs and checksums exactly. Sort each output list by ASCII lexical order. Do not infer deletions.

**Constraints:**

- Each list has 0 through 200 records with all three required fields.
- IDs are nonempty ASCII strings; checksums are ASCII strings and can be empty.
- Versions are integers from 0 through 1000000000; booleans are not versions.
- IDs are unique within each list, but can occur in both lists.
- Do not change input objects or their nested values. Each call starts with fresh state.
