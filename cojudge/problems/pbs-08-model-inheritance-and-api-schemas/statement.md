# 08. Model Inheritance and API Schemas

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/model-inheritance-and-api-schemas/)

Define `WorkoutBase(name, description="")`, with a nonempty string name.
Derive `Workout`, `WorkoutCreate`, and `WorkoutRead` from it. Only `Workout` is a
table; it has an optional primary key `id=None`. `WorkoutRead.id` is required.
`WorkoutCreate` has no ID field. Define `WorkoutUpdate` with optional `name` and
`description`, both defaulting to `None`; a supplied non-null name must be nonempty.
Define `ExerciseRead(id, name)` and `WorkoutWithExercises(WorkoutRead)` with an
independent default list of `ExerciseRead` objects. Schemas use Pydantic validation.
`model_dump(exclude_unset=True)` must distinguish omitted fields from explicit null.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

You're about to build a REST API for the gym app. There's a problem: APIs need different shapes of data for different operations.
When creating a workout, you don't send an id (database generates it). When reading a workout, you want the id included. When returning a workout with exercises, you want nested data.
Instead of duplicating fields, you'll use model inheritance to share common fields and create specialized schemas for different use cases.

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 7 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
