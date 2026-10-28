# 06. Many-to-Many Relationships

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/many-to-many-relationships/)

Define a many-to-many relationship between `Workout` and `Exercise`.
Each table has an optional integer `id` primary key and required `name`.
`Workout.exercises` and `Exercise.workouts` are reciprocal SQLModel relationships.
`WorkoutExercise` has the foreign keys `workout_id` and `exercise_id` as a composite
primary key. Implement `link_exercise(session, workout_id, exercise_id)`. Return
`False` for a missing endpoint. Otherwise create and commit the link, then return
`True`. A repeated call for the same pair succeeds without adding another link.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Here's the reality: workouts are composed of multiple exercises, and the same exercise appears in different workouts.
For example:

"Upper Body Day" includes: Bench Press, Pull Ups, Shoulder Press
"Push Day" also includes: Bench Press, Shoulder Press

This is a many-to-many relationship - each workout has many exercises, and each exercise belongs to many workouts.

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 6 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
