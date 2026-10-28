Time for the grand finale! You'll build advanced API endpoints that handle the full complexity of the gym app: creating log entries, viewing workout exercises, and filtering logs with optional query parameters.
This exercise brings together everything you've learned: relationships, link tables, complex queries, and FastAPI integration.

**Constraints:**

- Complete the new routes in `create_app(engine)`. POST `/logs` accepts `LogCreate`, commits and refreshes a log, and returns `LogRead` with status 201. A missing workout/exercise pair returns 404. Require sets and reps of at least 1 and nonnegative weight (default 0); invalid input returns 422.
- GET `/logs` returns logs in ID order. Optional integer `workout_id` and `exercise_id` filters must both match through the link table. No matches returns `[]`; invalid queries return 422.
- GET `/workouts/{workout_id}/exercises` returns distinct `ExerciseRead` objects in ID order. An empty workout returns `[]`; a missing workout returns 404. Keep the supplied workout routes working.
