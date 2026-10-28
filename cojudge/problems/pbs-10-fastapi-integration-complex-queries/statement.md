# 10. FastAPI Integration - Complex Queries

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/fastapi-integration-complex-queries/)

The models and basic workout endpoints are supplied. Complete the three new routes
inside `create_app(engine)`. Keep the basic endpoints working.

- `POST /logs`: accept `LogCreate`. Require an existing workout/exercise link. Return 404 for a missing pair. Commit and refresh a valid log. Return `LogRead` with status 201. Sets and reps must be at least 1. Weight defaults to zero and must be nonnegative. Invalid bodies return 422.
- `GET /logs`: return logs in ID order. Optional integer `workout_id` and `exercise_id` filters use the link table. Apply both filters together. Missing matches return an empty list. Invalid query values return 422.
- `GET /workouts/{workout_id}/exercises`: return distinct `ExerciseRead` objects in ID order. An empty workout returns an empty list. A missing workout returns 404.

TestClient supplies a fresh SQLite engine. The same exercise can appear in different
workouts. A log must stay attached to its exact workout/exercise pair.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Time for the grand finale! You'll build advanced API endpoints that handle the full complexity of the gym app: creating log entries, viewing workout exercises, and filtering logs with optional query parameters.
This exercise brings together everything you've learned: relationships, link tables, complex queries, and FastAPI integration.

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 17 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
