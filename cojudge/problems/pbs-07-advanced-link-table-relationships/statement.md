# 07. Advanced Link Table Relationships

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/advanced-link-table-relationships/)

The models are supplied. `WorkoutExercise.id` identifies a workout/exercise pair.
`LogEntry.workout_exercise_id` links a performance log to that exact pair.
Implement `add_pair_log(session, pair_id, sets, reps, weight=0.0)`. Reject sets or reps
below 1 and negative weight with `ValueError`. Return `None` if the pair is missing.
Commit and refresh valid logs. Implement `get_pair_logs(session, workout_id=None,
exercise_id=None)`. Return logs in ID order. Apply each optional filter through the
link table. When both filters are present, both must match. No filters means all logs.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Here's the challenge: you need to track performance for specific workout-exercise combinations.
When someone does Bench Press in "Upper Body Day" vs "Push Day", those are different contexts with potentially different weights and reps. The log entries should link to the specific workout-exercise pair, not just the workout.
This means LogEntry will link to WorkoutExercise (the link table) instead of directly to Workout.

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 7 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
