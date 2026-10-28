Here's the reality: workouts are composed of multiple exercises, and the same exercise appears in different workouts.
For example:

"Upper Body Day" includes: Bench Press, Pull Ups, Shoulder Press
"Push Day" also includes: Bench Press, Shoulder Press

This is a many-to-many relationship - each workout has many exercises, and each exercise belongs to many workouts.

**Constraints:**

- `Workout` and `Exercise` each have `id=None` as an optional integer primary key and required string `name`. Use reciprocal `exercises` and `workouts` relationships. `WorkoutExercise` has foreign keys `workout_id` and `exercise_id` as a composite primary key.
- `link_exercise(session, workout_id, exercise_id)` returns `False` if either row is missing. Otherwise commit the link and return `True`. Repeated links return `True` without adding another row.
