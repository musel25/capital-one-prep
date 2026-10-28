"""Relationship and schema exercises with earlier code supplied."""
from .bites import IMPORTS, FIXTURES

MANY_MANY = '''
class WorkoutExercise(SQLModel, table=True):
    workout_id: int = Field(foreign_key="workout.id", primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id", primary_key=True)

class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    exercises: list["Exercise"] = Relationship(back_populates="workouts", link_model=WorkoutExercise)

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    workouts: list[Workout] = Relationship(back_populates="exercises", link_model=WorkoutExercise)
'''

LINKED = '''
class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    exercise_links: list["WorkoutExercise"] = Relationship(back_populates="workout")

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    workout_links: list["WorkoutExercise"] = Relationship(back_populates="exercise")

class WorkoutExercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workout_id: int = Field(foreign_key="workout.id")
    exercise_id: int = Field(foreign_key="exercise.id")
    workout: Optional[Workout] = Relationship(back_populates="exercise_links")
    exercise: Optional[Exercise] = Relationship(back_populates="workout_links")
    logs: list["LogEntry"] = Relationship(back_populates="workout_exercise")

class LogEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workout_exercise_id: int = Field(foreign_key="workoutexercise.id")
    sets: int
    reps: int
    weight: float = 0.0
    workout_exercise: Optional[WorkoutExercise] = Relationship(back_populates="logs")
'''

SPECS = [dict(number=6, contract='''Define a many-to-many relationship between `Workout` and `Exercise`.
Each table has an optional integer `id` primary key and required `name`.
`Workout.exercises` and `Exercise.workouts` are reciprocal SQLModel relationships.
`WorkoutExercise` has the foreign keys `workout_id` and `exercise_id` as a composite
primary key. Implement `link_exercise(session, workout_id, exercise_id)`. Return
`False` for a missing endpoint. Otherwise create and commit the link, then return
`True`. A repeated call for the same pair succeeds without adding another link.''',
    template=IMPORTS + '''
class WorkoutExercise(SQLModel, table=True):
    workout_id: int = Field(foreign_key="workout.id", primary_key=True)
    exercise_id: int = Field(foreign_key="exercise.id", primary_key=True)

class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # Add exercises and its reciprocal relationship.

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # Add workouts and its reciprocal relationship.

def link_exercise(session, workout_id, exercise_id):
    raise NotImplementedError
''', reference=IMPORTS + MANY_MANY + '''
def link_exercise(session, workout_id, exercise_id):
    if session.get(Workout, workout_id) is None or session.get(Exercise, exercise_id) is None:
        return False
    if session.get(WorkoutExercise, (workout_id, exercise_id)) is None:
        session.add(WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id))
        session.commit()
    return True
''', tests=FIXTURES + '''
@pytest.fixture
def seeded(session):
    session.add_all([app.Workout(id=1, name="Upper"), app.Workout(id=2, name="Push"), app.Exercise(id=1, name="Bench"), app.Exercise(id=2, name="Rows")])
    session.commit()
    return session

def test_composite_key_and_foreign_keys():
    table = app.WorkoutExercise.__table__
    assert set(table.primary_key.columns.keys()) == {"workout_id", "exercise_id"}
    assert {fk.target_fullname for fk in table.foreign_keys} == {"workout.id", "exercise.id"}

def test_link_and_both_relationships(seeded):
    assert app.link_exercise(seeded, 1, 1) is True
    seeded.expire_all()
    assert seeded.get(app.Workout, 1).exercises[0].name == "Bench"
    assert seeded.get(app.Exercise, 1).workouts[0].name == "Upper"

def test_shared_exercise(seeded):
    app.link_exercise(seeded, 1, 1)
    app.link_exercise(seeded, 2, 1)
    app.link_exercise(seeded, 1, 2)
    seeded.expire_all()
    assert {w.id for w in seeded.get(app.Exercise, 1).workouts} == {1, 2}
    assert {e.id for e in seeded.get(app.Workout, 1).exercises} == {1, 2}
    assert [e.id for e in seeded.get(app.Workout, 2).exercises] == [1]

def test_duplicate_link_is_idempotent(seeded):
    assert app.link_exercise(seeded, 1, 1) is True
    assert app.link_exercise(seeded, 1, 1) is True
    assert len(seeded.exec(select(app.WorkoutExercise)).all()) == 1

def test_missing_endpoints(seeded):
    assert app.link_exercise(seeded, 99, 1) is False
    assert app.link_exercise(seeded, 1, 99) is False
    assert seeded.exec(select(app.WorkoutExercise)).all() == []

def test_link_is_durable(seeded, engine):
    app.link_exercise(seeded, 1, 1)
    seeded.close()
    with Session(engine) as check:
        assert check.get(app.WorkoutExercise, (1, 1)) is not None
''', mutations=[dict(name='link is not committed', old='session.commit()', new='session.flush()'),
               dict(name='duplicate pair inserted', old='if session.get(WorkoutExercise, (workout_id, exercise_id)) is None:', new='if True:')]),
dict(number=7, contract='''The models are supplied. `WorkoutExercise.id` identifies a workout/exercise pair.
`LogEntry.workout_exercise_id` links a performance log to that exact pair.
Implement `add_pair_log(session, pair_id, sets, reps, weight=0.0)`. Reject sets or reps
below 1 and negative weight with `ValueError`. Return `None` if the pair is missing.
Commit and refresh valid logs. Implement `get_pair_logs(session, workout_id=None,
exercise_id=None)`. Return logs in ID order. Apply each optional filter through the
link table. When both filters are present, both must match. No filters means all logs.''',
    template=IMPORTS + LINKED + '''
def add_pair_log(session, pair_id, sets, reps, weight=0.0):
    raise NotImplementedError

def get_pair_logs(session, workout_id=None, exercise_id=None):
    raise NotImplementedError
''', reference=IMPORTS + LINKED + '''
def add_pair_log(session, pair_id, sets, reps, weight=0.0):
    if sets < 1 or reps < 1 or weight < 0:
        raise ValueError("Invalid performance")
    if session.get(WorkoutExercise, pair_id) is None:
        return None
    row = LogEntry(workout_exercise_id=pair_id, sets=sets, reps=reps, weight=weight)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

def get_pair_logs(session, workout_id=None, exercise_id=None):
    query = select(LogEntry).join(WorkoutExercise)
    if workout_id is not None:
        query = query.where(WorkoutExercise.workout_id == workout_id)
    if exercise_id is not None:
        query = query.where(WorkoutExercise.exercise_id == exercise_id)
    return list(session.exec(query.order_by(LogEntry.id)).all())
''', tests=FIXTURES + '''
@pytest.fixture
def seeded(session):
    session.add_all([app.Workout(id=1, name="Upper"), app.Workout(id=2, name="Push"), app.Exercise(id=1, name="Bench"), app.Exercise(id=2, name="Rows")])
    session.commit()
    session.add_all([app.WorkoutExercise(id=10, workout_id=1, exercise_id=1), app.WorkoutExercise(id=20, workout_id=2, exercise_id=1), app.WorkoutExercise(id=30, workout_id=1, exercise_id=2)])
    session.commit()
    return session

@pytest.fixture
def logged(seeded):
    app.add_pair_log(seeded, 10, 3, 8, 50)
    app.add_pair_log(seeded, 20, 2, 10, 30)
    app.add_pair_log(seeded, 30, 1, 12, 20)
    return seeded

def test_log_links_to_pair(seeded):
    row = app.add_pair_log(seeded, 20, 2, 10, 30)
    assert row.id is not None and row.workout_exercise_id == 20
    assert row.workout_exercise.workout_id == 2 and row.workout_exercise.exercise_id == 1
    assert row.workout_exercise.logs[0].id == row.id

def test_pair_isolation(logged):
    rows = app.get_pair_logs(logged, workout_id=1, exercise_id=1)
    assert len(rows) == 1 and rows[0].weight == 50

def test_workout_filter(logged):
    assert [r.weight for r in app.get_pair_logs(logged, workout_id=1)] == [50, 20]

def test_exercise_filter(logged):
    assert [r.weight for r in app.get_pair_logs(logged, exercise_id=1)] == [50, 30]

def test_all_and_no_match(logged):
    assert [r.weight for r in app.get_pair_logs(logged)] == [50, 30, 20]
    assert app.get_pair_logs(logged, workout_id=99) == []
    assert app.get_pair_logs(logged, workout_id=2, exercise_id=2) == []
    assert app.get_pair_logs(logged, workout_id=0) == []
    assert app.get_pair_logs(logged, exercise_id=0) == []

def test_invalid_and_missing(seeded):
    assert app.add_pair_log(seeded, 99, 1, 1) is None
    for sets, reps, weight in [(0, 2, 0), (1, 0, 0), (1, 1, -1)]:
        with pytest.raises(ValueError):
            app.add_pair_log(seeded, 10, sets, reps, weight)
    assert app.get_pair_logs(seeded) == []

def test_pair_log_is_durable(seeded, engine):
    app.add_pair_log(seeded, 10, 1, 2)
    seeded.close()
    with Session(engine) as check:
        row = check.exec(select(app.LogEntry)).one()
        assert row.workout_exercise_id == 10 and row.sets == 1 and row.reps == 2 and row.weight == 0
''', mutations=[dict(name='exercise filter omitted', old='query = query.where(WorkoutExercise.exercise_id == exercise_id)', new='query = query'),
               dict(name='pair log is not committed', old='session.commit()', new='session.flush()')]),
]

SCHEMAS = '''
class WorkoutBase(SQLModel):
    name: str = Field(min_length=1)
    description: str = ""

class Workout(WorkoutBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutRead(WorkoutBase):
    id: int

class WorkoutUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None

class ExerciseRead(SQLModel):
    id: int
    name: str

class WorkoutWithExercises(WorkoutRead):
    exercises: list[ExerciseRead] = Field(default_factory=list)
'''

SPECS.append(dict(number=8, contract='''Define `WorkoutBase(name, description="")`, with a nonempty string name.
Derive `Workout`, `WorkoutCreate`, and `WorkoutRead` from it. Only `Workout` is a
table; it has an optional primary key `id=None`. `WorkoutRead.id` is required.
`WorkoutCreate` has no ID field. Define `WorkoutUpdate` with optional `name` and
`description`, both defaulting to `None`; a supplied non-null name must be nonempty.
Define `ExerciseRead(id, name)` and `WorkoutWithExercises(WorkoutRead)` with an
independent default list of `ExerciseRead` objects. Schemas use Pydantic validation.
`model_dump(exclude_unset=True)` must distinguish omitted fields from explicit null.''',
    template=IMPORTS + '''
class WorkoutBase(SQLModel):
    # Add shared fields and name validation.
    pass

class Workout(WorkoutBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutRead(WorkoutBase):
    pass

class WorkoutUpdate(SQLModel):
    pass

class ExerciseRead(SQLModel):
    pass

class WorkoutWithExercises(WorkoutRead):
    pass
''', reference=IMPORTS + SCHEMAS, tests=FIXTURES + '''from pydantic import ValidationError

def test_only_workout_is_a_table():
    assert set(SQLModel.metadata.tables) == {"workout"}
    assert issubclass(app.WorkoutCreate, app.WorkoutBase)
    assert issubclass(app.WorkoutRead, app.WorkoutBase)

def test_create_has_no_id():
    row = app.WorkoutCreate(name="Leg Day")
    assert row.model_dump() == {"name": "Leg Day", "description": ""}
    assert "id" not in app.WorkoutCreate.model_fields

def test_read_requires_id():
    with pytest.raises(ValidationError):
        app.WorkoutRead(name="A")
    assert app.WorkoutRead(id=7, name="A").id == 7

def test_name_validation():
    for schema in (app.WorkoutCreate, app.WorkoutRead):
        with pytest.raises(ValidationError):
            schema(id=1, name="")
    with pytest.raises(ValidationError):
        app.WorkoutUpdate(name="")

def test_patch_omitted_and_null():
    assert app.WorkoutUpdate().name is None and app.WorkoutUpdate().description is None
    assert app.WorkoutUpdate().model_dump(exclude_unset=True) == {}
    assert app.WorkoutUpdate(name=None).model_dump(exclude_unset=True) == {"name": None}
    assert app.WorkoutUpdate(description=None).model_dump(exclude_unset=True) == {"description": None}
    assert app.WorkoutUpdate(name="A").model_dump(exclude_unset=True) == {"name": "A"}

def test_nested_serialization():
    row = app.WorkoutWithExercises(id=1, name="Upper", exercises=[{"id": 2, "name": "Bench"}])
    assert isinstance(row.exercises[0], app.ExerciseRead)
    assert row.model_dump()["exercises"] == [{"id": 2, "name": "Bench"}]

def test_nested_default_is_independent():
    first = app.WorkoutWithExercises(id=1, name="A")
    second = app.WorkoutWithExercises(id=2, name="B")
    first.exercises.append(app.ExerciseRead(id=1, name="Squat"))
    assert second.exercises == []
''', mutations=[dict(name='empty names allowed', old='name: str = Field(min_length=1)', new='name: str'),
               dict(name='read id is optional', old='    id: int\n', new='    id: Optional[int] = None\n'),
               dict(name='update name cannot be null', old='name: Optional[str] = Field(default=None, min_length=1)', new='name: str = Field(default="missing", min_length=1)')] ))
