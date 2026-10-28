You're about to build a REST API for the gym app. There's a problem: APIs need different shapes of data for different operations.
When creating a workout, you don't send an id (database generates it). When reading a workout, you want the id included. When returning a workout with exercises, you want nested data.
Instead of duplicating fields, you'll use model inheritance to share common fields and create specialized schemas for different use cases.

**Constraints:**

- Define `WorkoutBase(name, description="")` with nonempty name. Derive `Workout`, `WorkoutCreate`, and `WorkoutRead`. Only `Workout` is a table, with optional integer primary key `id=None`. `WorkoutRead.id` is required; `WorkoutCreate` has no ID.
- `WorkoutUpdate` has optional `name=None` and `description=None`. A non-null name must be nonempty. Preserve the difference between omitted fields and explicit null in `model_dump(exclude_unset=True)`.
- Define `ExerciseRead(id, name)` and `WorkoutWithExercises(WorkoutRead)` with an independent default list of `ExerciseRead` objects.
