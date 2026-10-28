Time to expose your gym database to the world! You'll build a REST API using FastAPI, the modern web framework designed to work seamlessly with SQLModel.
FastAPI lets you create HTTP endpoints that receive requests and return responses. Combined with SQLModel, you get automatic validation, serialization, and documentation.

**Constraints:**

- Implement `create_app(engine)`. Create tables and use the supplied session dependency. POST `/workouts` accepts `WorkoutCreate`, commits and refreshes the row, and returns `WorkoutRead` with status 201. The database chooses its ID.
- GET `/workouts` returns rows in ID order with `offset=0` (minimum 0) and `limit=100` (range 1–100). GET `/workouts/{workout_id}` returns a row or 404. DELETE commits deletion and returns an empty 204 response, or 404. Invalid input returns 422.
