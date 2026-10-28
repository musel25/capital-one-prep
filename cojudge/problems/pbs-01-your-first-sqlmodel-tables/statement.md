# 01. Your First SQLModel Tables

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/your-first-sqlmodel-tables/)

Define `Workout` and `Exercise` as SQLModel tables. Both have an optional integer
primary key `id` with default `None`, and required string `name`. `Workout.description`
and `Exercise.muscle_group` default to the empty string. Implement `create_tables(engine)`.
It creates both tables and can be called again without losing rows. No global database is required.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Welcome to the SQLModel learning path! You're about to build a workout tracking app for a local gym.
The gym owner wants to digitize their workout programs and exercises. Your first task? Create the database schema to store workouts (like "Upper Body Day" or "Leg Day") and exercises (like "Bench Press" or "Squats").

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 6 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
