The gym wants to track workout performance over time! Each time someone completes a workout, they log their sets, reps, and weights.
This introduces a relationship: one workout can have many log entries, but each log entry belongs to exactly one workout. This is called a one-to-many relationship.

**Constraints:**

- Define reciprocal `Workout.logs` and `LogEntry.workout` relationships. `LogEntry` has `id`, required foreign key `workout_id`, `sets`, `reps`, and `weight=0.0`. IDs default to `None`; `Workout` also has required `name`.
- `add_log(session, workout_id, sets, reps, weight=0.0)` returns `None` for a missing workout. Reject sets or reps below 1 and negative weight with `ValueError`. Commit, refresh, and return a valid log.
