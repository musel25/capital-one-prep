The gym needs to fix typos in workout names and remove discontinued programs. Time to complete your CRUD (Create, Read, Update, Delete) skills!
SQLModel makes updates simple: fetch the object, modify it, commit. No special UPDATE statements needed!

**Constraints:**

- `update_workout(session, workout_id, **changes)` accepts only `name` and `description`. Reject unknown fields with `ValueError` before any change. Return `None` for a missing row. An empty update returns the existing row. Commit, refresh, and return updated rows.
- `delete_workout(session, workout_id)` commits deletion and returns `True`, or returns `False` for a missing row. Preserve other rows.
