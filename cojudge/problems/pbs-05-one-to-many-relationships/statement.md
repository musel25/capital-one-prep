# 05. One-to-Many Relationships

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/one-to-many-relationships/)

Define `Workout(id, name, logs)` and `LogEntry(id, workout_id, sets, reps, weight, workout)`.
Both are tables. IDs default to `None`. Weight defaults to `0.0`. `workout_id` is a
required foreign key to `workout.id`. Use `Relationship(back_populates=...)` in both
directions. Implement `add_log(session, workout_id, sets, reps, weight=0.0)`.
Return `None` for a missing workout. Reject sets or reps below 1, and weight below 0,
with `ValueError`. Commit, refresh, and return each valid log.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

The gym wants to track workout performance over time! Each time someone completes a workout, they log their sets, reps, and weights.
This introduces a relationship: one workout can have many log entries, but each log entry belongs to exactly one workout. This is called a one-to-many relationship.

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 7 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
