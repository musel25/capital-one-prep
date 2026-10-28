# 09. FastAPI Integration - Basic Endpoints

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/fastapi-integration-basic-endpoints/)

Implement `create_app(engine)` and return a FastAPI app. Models and the session
dependency are supplied. Create the tables in the supplied engine. Use a session
dependency for each request. Implement these endpoints:

- `POST /workouts`: accept `WorkoutCreate`, commit and refresh a row, return `WorkoutRead` with status 201. The client cannot choose its ID.
- `GET /workouts`: return rows in ID order. Support `offset=0` (minimum 0) and `limit=100` (range 1–100).
- `GET /workouts/{workout_id}`: return a row or 404.
- `DELETE /workouts/{workout_id}`: commit deletion and return an empty 204 response, or 404.

Use FastAPI validation: invalid bodies, IDs, and pagination return 422. Tests use
TestClient and a supplied in-memory engine. Do not start a server or use the network.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Time to expose your gym database to the world! You'll build a REST API using FastAPI, the modern web framework designed to work seamlessly with SQLModel.
FastAPI lets you create HTTP endpoints that receive requests and return responses. Combined with SQLModel, you get automatic validation, serialization, and documentation.

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 8 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
