"""Local API details and executable examples for the public SQLModel tasks."""

CLARIFICATIONS = {
    1: ('Define `Workout` and `Exercise` tables with optional integer primary key `id=None` and required string `name`. Default `Workout.description` and `Exercise.muscle_group` to `""`. `create_tables(engine)` must preserve rows when called again.',),
    2: ('Implement `add_workout(session, name, description="")` and `add_exercise(session, name, muscle_group="")`. Commit, refresh, and return the new row. Duplicate names are allowed. Keep the caller\'s session open.',
        '`get_session(engine)` yields a session in a context manager. Closing the generator rolls back uncommitted changes.'),
    3: ('Implement `get_workouts(session)`, `get_workout(session, workout_id)`, and `find_exercises(session, muscle_group=None)`. Lists use ID order. A missing workout returns `None`. The group filter is exact and case-sensitive; `None` selects all groups and `""` selects the empty group. Reads must not change rows.',),
    4: ('`update_workout(session, workout_id, **changes)` accepts only `name` and `description`. Reject unknown fields with `ValueError` before any change. Return `None` for a missing row. An empty update returns the existing row. Commit, refresh, and return updated rows.',
        '`delete_workout(session, workout_id)` commits deletion and returns `True`, or returns `False` for a missing row. Preserve other rows.'),
    5: ('Define reciprocal `Workout.logs` and `LogEntry.workout` relationships. `LogEntry` has `id`, required foreign key `workout_id`, `sets`, `reps`, and `weight=0.0`. IDs default to `None`; `Workout` also has required `name`.',
        '`add_log(session, workout_id, sets, reps, weight=0.0)` returns `None` for a missing workout. Reject sets or reps below 1 and negative weight with `ValueError`. Commit, refresh, and return a valid log.'),
    6: ('`Workout` and `Exercise` each have `id=None` as an optional integer primary key and required string `name`. Use reciprocal `exercises` and `workouts` relationships. `WorkoutExercise` has foreign keys `workout_id` and `exercise_id` as a composite primary key.',
        '`link_exercise(session, workout_id, exercise_id)` returns `False` if either row is missing. Otherwise commit the link and return `True`. Repeated links return `True` without adding another row.'),
    7: ('Use the supplied models. `add_pair_log(session, pair_id, sets, reps, weight=0.0)` returns `None` for a missing pair. Reject sets or reps below 1 and negative weight with `ValueError`. Commit, refresh, and return valid logs.',
        '`get_pair_logs(session, workout_id=None, exercise_id=None)` returns logs in ID order. Apply both optional filters through the link table. No filters selects all logs.'),
    8: ('Define `WorkoutBase(name, description="")` with nonempty name. Derive `Workout`, `WorkoutCreate`, and `WorkoutRead`. Only `Workout` is a table, with optional integer primary key `id=None`. `WorkoutRead.id` is required; `WorkoutCreate` has no ID.',
        '`WorkoutUpdate` has optional `name=None` and `description=None`. A non-null name must be nonempty. Preserve the difference between omitted fields and explicit null in `model_dump(exclude_unset=True)`.',
        'Define `ExerciseRead(id, name)` and `WorkoutWithExercises(WorkoutRead)` with an independent default list of `ExerciseRead` objects.'),
    9: ('Implement `create_app(engine)`. Create tables and use the supplied session dependency. POST `/workouts` accepts `WorkoutCreate`, commits and refreshes the row, and returns `WorkoutRead` with status 201. The database chooses its ID.',
        'GET `/workouts` returns rows in ID order with `offset=0` (minimum 0) and `limit=100` (range 1–100). GET `/workouts/{workout_id}` returns a row or 404. DELETE commits deletion and returns an empty 204 response, or 404. Invalid input returns 422.'),
    10: ('Complete the new routes in `create_app(engine)`. POST `/logs` accepts `LogCreate`, commits and refreshes a log, and returns `LogRead` with status 201. A missing workout/exercise pair returns 404. Require sets and reps of at least 1 and nonnegative weight (default 0); invalid input returns 422.',
         'GET `/logs` returns logs in ID order. Optional integer `workout_id` and `exercise_id` filters must both match through the link table. No matches returns `[]`; invalid queries return 422.',
         'GET `/workouts/{workout_id}/exercises` returns distinct `ExerciseRead` objects in ID order. An empty workout returns `[]`; a missing workout returns 404. Keep the supplied workout routes working.'),
}

DB = ('engine = create_engine("sqlite://")\nSQLModel.metadata.create_all(engine)\n')
API = ('from fastapi.testclient import TestClient\nfrom sqlalchemy.pool import StaticPool\n'
       'engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)\n'
       'client = TestClient(create_app(engine))\n')

EXAMPLES = {
    1: [('workout = Workout(name="Leg Day")\nexercise = Exercise(name="Squats")\nprint(workout.id, repr(workout.description), repr(exercise.muscle_group))', "None '' ''")],
    2: [(DB + 'with Session(engine) as session:\n    row = add_workout(session, "Leg Day", "Strength")\n    print(row.id, row.name, row.description)', '1 Leg Day Strength')],
    3: [(DB + 'with Session(engine) as session:\n    session.add_all([Workout(id=5, name="A"), Workout(id=2, name="Z")])\n    session.commit()\n    print([row.id for row in get_workouts(session)])\n    print(get_workout(session, 99))', '[2, 5]\nNone')],
    4: [(DB + 'with Session(engine) as session:\n    session.add(Workout(id=1, name="Old"))\n    session.commit()\n    print(update_workout(session, 1, name="New").name)\n    print(delete_workout(session, 1))\n    print(delete_workout(session, 1))', 'New\nTrue\nFalse')],
    5: [(DB + 'with Session(engine) as session:\n    session.add(Workout(id=1, name="Leg Day"))\n    session.commit()\n    log = add_log(session, 1, sets=3, reps=10)\n    print(log.workout_id, log.sets, log.reps, log.weight)\n    print(add_log(session, 99, sets=3, reps=10))', '1 3 10 0.0\nNone')],
    6: [(DB + 'with Session(engine) as session:\n    session.add(Workout(id=1, name="Upper Body"))\n    session.add(Exercise(id=1, name="Bench Press"))\n    session.commit()\n    print(link_exercise(session, 1, 1))\n    print(link_exercise(session, 1, 1))\n    print([item.name for item in session.get(Workout, 1).exercises])', "True\nTrue\n['Bench Press']")],
    7: [(DB + 'with Session(engine) as session:\n    session.add(Workout(id=1, name="Upper Body"))\n    session.add(Exercise(id=1, name="Bench Press"))\n    session.commit()\n    session.add(WorkoutExercise(id=1, workout_id=1, exercise_id=1))\n    session.commit()\n    add_pair_log(session, 1, sets=3, reps=8, weight=40)\n    print([(log.sets, log.reps, log.weight) for log in get_pair_logs(session, workout_id=1)])', '[(3, 8, 40.0)]')],
    8: [('print(WorkoutCreate(name="Leg Day").model_dump())\nprint(WorkoutUpdate().model_dump(exclude_unset=True))\nprint(WorkoutUpdate(description=None).model_dump(exclude_unset=True))', "{'name': 'Leg Day', 'description': ''}\n{}\n{'description': None}")],
    9: [(API + 'response = client.post("/workouts", json={"name": "Leg Day"})\nprint(response.status_code, response.json())\nprint(client.delete("/workouts/1").status_code)\nprint(client.get("/workouts").json())', "201 {'name': 'Leg Day', 'description': '', 'id': 1}\n204\n[]")],
    10: [(API + 'with Session(engine) as session:\n    session.add(Workout(id=1, name="Upper Body"))\n    session.add(Exercise(id=1, name="Bench Press"))\n    session.commit()\n    session.add(WorkoutExercise(id=1, workout_id=1, exercise_id=1))\n    session.commit()\nresponse = client.post("/logs", json={"workout_exercise_id": 1, "sets": 3, "reps": 8})\nprint(response.status_code)\nprint(client.get("/workouts/1/exercises").json())\nprint([(row["sets"], row["reps"], row["weight"]) for row in client.get("/logs?workout_id=1").json()])', "201\n[{'id': 1, 'name': 'Bench Press'}]\n[(3, 8, 0.0)]")],
}
