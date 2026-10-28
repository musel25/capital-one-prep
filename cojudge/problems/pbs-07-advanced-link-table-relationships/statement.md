Here's the challenge: you need to track performance for specific workout-exercise combinations.
When someone does Bench Press in "Upper Body Day" vs "Push Day", those are different contexts with potentially different weights and reps. The log entries should link to the specific workout-exercise pair, not just the workout.
This means LogEntry will link to WorkoutExercise (the link table) instead of directly to Workout.

**Constraints:**

- Use the supplied models. `add_pair_log(session, pair_id, sets, reps, weight=0.0)` returns `None` for a missing pair. Reject sets or reps below 1 and negative weight with `ValueError`. Commit, refresh, and return valid logs.
- `get_pair_logs(session, workout_id=None, exercise_id=None)` returns logs in ID order. Apply both optional filters through the link table. No filters selects all logs.
