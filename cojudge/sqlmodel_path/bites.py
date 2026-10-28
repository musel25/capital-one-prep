"""Table, session, CRUD, and one-to-many exercises. Tests define this version's contract."""

IMPORTS = '''from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship
'''

TABLES = '''
class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    muscle_group: str = ""
'''

FIXTURES = '''import pytest
from sqlmodel import SQLModel, Session, create_engine, select
import workout_app as app

@pytest.fixture
def engine():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session

'''

SPECS = [
    dict(number=1, contract='''Define `Workout` and `Exercise` as SQLModel tables. Both have an optional integer
primary key `id` with default `None`, and required string `name`. `Workout.description`
and `Exercise.muscle_group` default to the empty string. Implement `create_tables(engine)`.
It creates both tables and can be called again without losing rows. No global database is required.''',
         template=IMPORTS + '''
class Workout(SQLModel):
    # Add table=True and the required fields.
    pass

class Exercise(SQLModel):
    # Add table=True and the required fields.
    pass

def create_tables(engine):
    raise NotImplementedError
''', reference=IMPORTS + TABLES + '''
def create_tables(engine):
    SQLModel.metadata.create_all(engine)
''', tests=FIXTURES + '''
def test_workout_table_fields():
    assert app.Workout.__tablename__ == "workout"
    assert set(app.Workout.__table__.columns.keys()) == {"id", "name", "description"}
    assert app.Workout.__table__.c.id.primary_key

def test_exercise_table_fields():
    assert set(app.Exercise.__table__.columns.keys()) == {"id", "name", "muscle_group"}
    assert app.Exercise.__table__.c.id.primary_key

def test_defaults():
    workout, exercise = app.Workout(name="Leg Day"), app.Exercise(name="Squats")
    assert workout.id is None and workout.description == ""
    assert exercise.id is None and exercise.muscle_group == ""

def test_required_name():
    assert app.Workout.model_fields["name"].is_required()
    assert app.Exercise.model_fields["name"].is_required()

def test_create_and_persist():
    engine = create_engine("sqlite://")
    try:
        app.create_tables(engine)
        with Session(engine) as session:
            session.add(app.Workout(name="Upper Body", description="Press"))
            session.add(app.Exercise(name="Bench Press", muscle_group="chest"))
            session.commit()
        with Session(engine) as session:
            assert session.exec(select(app.Workout)).one().description == "Press"
            assert session.exec(select(app.Exercise)).one().muscle_group == "chest"
    finally:
        engine.dispose()

def test_create_tables_is_idempotent(engine):
    with Session(engine) as session:
        session.add(app.Workout(name="Keep me"))
        session.commit()
    app.create_tables(engine)
    app.create_tables(engine)
    with Session(engine) as session:
        assert session.exec(select(app.Workout)).one().name == "Keep me"
''', mutations=[dict(name='wrong description default', old='description: str = ""', new='description: str = "unknown"'),
                  dict(name='table creation omitted', old='SQLModel.metadata.create_all(engine)', new='pass')]),
    dict(number=2, contract='''The two table models are supplied. Implement `add_workout(session, name, description="")`
and `add_exercise(session, name, muscle_group="")`. Add one row, commit, refresh, and
return that model with its database ID. Do not close the caller's session. Repeated
names are allowed. Implement `get_session(engine)` as a generator that yields a
Session inside a context manager. An uncommitted insert must roll back when it closes.''',
         template=IMPORTS + TABLES + '''
def add_workout(session, name, description=""):
    raise NotImplementedError

def add_exercise(session, name, muscle_group=""):
    raise NotImplementedError

def get_session(engine):
    raise NotImplementedError
''', reference=IMPORTS + TABLES + '''
def add_workout(session, name, description=""):
    row = Workout(name=name, description=description)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

def add_exercise(session, name, muscle_group=""):
    row = Exercise(name=name, muscle_group=muscle_group)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

def get_session(engine):
    with Session(engine) as session:
        yield session
''', tests=FIXTURES + '''
def test_add_workout(session):
    row = app.add_workout(session, "Leg Day", "Strength")
    assert row.id is not None and row.name == "Leg Day" and row.description == "Strength"
    assert row in session

def test_add_exercise(session):
    row = app.add_exercise(session, "Squats", "legs")
    assert row.id is not None and row.muscle_group == "legs"
    assert row in session

def test_defaults_and_duplicate_names(session):
    first = app.add_workout(session, "Same")
    second = app.add_workout(session, "Same")
    exercise = app.add_exercise(session, "Same")
    assert first.id != second.id and second.description == "" and exercise.muscle_group == ""

def test_rows_survive_a_new_session(engine):
    with Session(engine) as session:
        app.add_workout(session, "Persisted")
        app.add_exercise(session, "Persisted exercise")
    with Session(engine) as session:
        assert session.exec(select(app.Workout)).one().name == "Persisted"
        assert session.exec(select(app.Exercise)).one().name == "Persisted exercise"

def test_session_generator_committed_rows(engine):
    generator = app.get_session(engine)
    session = next(generator)
    assert isinstance(session, Session)
    app.add_workout(session, "Saved")
    generator.close()
    with Session(engine) as check:
        assert check.exec(select(app.Workout)).one().name == "Saved"

def test_session_generator_rolls_back(engine):
    generator = app.get_session(engine)
    session = next(generator)
    session.add(app.Workout(name="Discard"))
    session.flush()
    generator.close()
    with Session(engine) as check:
        assert check.exec(select(app.Workout)).all() == []
''', mutations=[dict(name='workout insert is not committed', old='session.commit()', new='session.flush()'),
                  dict(name='muscle group is discarded', old='muscle_group=muscle_group', new='muscle_group=""'),
                  dict(name='caller session is closed', old='session.refresh(row)\n    return row', new='session.refresh(row)\n    session.close()\n    return row')]),
    dict(number=3, contract='''Implement `get_workouts(session)` in ID order, `get_workout(session, workout_id)`
returning a row or `None`, and `find_exercises(session, muscle_group=None)` in ID order.
A group filter uses exact, case-sensitive equality. `None` means all groups. An empty
string selects the empty group. Reads must not insert or change rows.''',
         template=IMPORTS + TABLES + '''
def get_workouts(session):
    raise NotImplementedError

def get_workout(session, workout_id):
    raise NotImplementedError

def find_exercises(session, muscle_group=None):
    raise NotImplementedError
''', reference=IMPORTS + TABLES + '''
def get_workouts(session):
    return list(session.exec(select(Workout).order_by(Workout.id)).all())

def get_workout(session, workout_id):
    return session.get(Workout, workout_id)

def find_exercises(session, muscle_group=None):
    query = select(Exercise)
    if muscle_group is not None:
        query = query.where(Exercise.muscle_group == muscle_group)
    return list(session.exec(query.order_by(Exercise.id)).all())
''', tests=FIXTURES + '''
def test_empty_results(session):
    assert app.get_workouts(session) == [] and app.find_exercises(session) == []

def test_workouts_are_in_id_order(session):
    session.add_all([app.Workout(id=5, name="A"), app.Workout(id=2, name="Z")])
    session.commit()
    assert [w.id for w in app.get_workouts(session)] == [2, 5]

def test_get_one_and_missing(session):
    session.add_all([app.Workout(id=1, name="A"), app.Workout(id=2, name="B")])
    session.commit()
    assert app.get_workout(session, 2).name == "B"
    assert app.get_workout(session, 99) is None

def test_filter_is_exact(session):
    session.add_all([app.Exercise(name="A", muscle_group="legs"), app.Exercise(name="B", muscle_group="Legs"), app.Exercise(name="C", muscle_group="legs")])
    session.commit()
    assert [e.name for e in app.find_exercises(session, "legs")] == ["A", "C"]
    assert app.find_exercises(session, "missing") == []

def test_empty_filter_is_not_all(session):
    session.add_all([app.Exercise(name="A"), app.Exercise(name="B", muscle_group="legs")])
    session.commit()
    assert [e.name for e in app.find_exercises(session, "")] == ["A"]
    assert len(app.find_exercises(session)) == 2

def test_reads_do_not_write(session):
    app.get_workouts(session)
    app.get_workout(session, 100)
    app.find_exercises(session, "legs")
    assert not session.new and not session.dirty and not session.deleted
''', mutations=[dict(name='empty group treated as no filter', old='if muscle_group is not None:', new='if muscle_group:'),
                  dict(name='reverse workout order', old='order_by(Workout.id)', new='order_by(Workout.id.desc())')]),
    dict(number=4, contract='''Implement `update_workout(session, workout_id, **changes)`. Only `name` and
`description` can change. Reject every unknown field with `ValueError` before any
change. Return `None` for a missing row. An empty update returns the existing row.
Commit and refresh successful updates. Implement `delete_workout(session, workout_id)`.
Commit a deletion and return `True`. Return `False` if the row is missing. Preserve other rows.''',
         template=IMPORTS + TABLES + '''
def update_workout(session, workout_id, **changes):
    raise NotImplementedError

def delete_workout(session, workout_id):
    raise NotImplementedError
''', reference=IMPORTS + TABLES + '''
def update_workout(session, workout_id, **changes):
    if set(changes) - {"name", "description"}:
        raise ValueError("Unknown field")
    row = session.get(Workout, workout_id)
    if row is None:
        return None
    for key, value in changes.items():
        setattr(row, key, value)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row

def delete_workout(session, workout_id):
    row = session.get(Workout, workout_id)
    if row is None:
        return False
    session.delete(row)
    session.commit()
    return True
''', tests=FIXTURES + '''
@pytest.fixture
def seeded(session):
    session.add_all([app.Workout(id=1, name="A", description="old"), app.Workout(id=2, name="B")])
    session.commit()
    return session

def test_update_fields(seeded):
    row = app.update_workout(seeded, 1, name="New", description="")
    assert row.id == 1 and row.name == "New" and row.description == ""
    assert seeded.get(app.Workout, 2).name == "B"

def test_partial_and_empty_update(seeded):
    row = app.update_workout(seeded, 1, description="changed")
    assert row.name == "A" and row.description == "changed"
    assert app.update_workout(seeded, 1).name == "A"

def test_update_is_durable(seeded, engine):
    app.update_workout(seeded, 1, name="Saved")
    seeded.close()
    with Session(engine) as check:
        assert check.get(app.Workout, 1).name == "Saved"

def test_missing_rows(seeded):
    assert app.update_workout(seeded, 99, name="No") is None
    assert app.delete_workout(seeded, 99) is False

def test_invalid_field_is_atomic(seeded):
    with pytest.raises(ValueError):
        app.update_workout(seeded, 1, name="Must not change", id=7)
    assert seeded.get(app.Workout, 1).name == "A"
    assert seeded.get(app.Workout, 7) is None

def test_delete_is_durable(seeded, engine):
    assert app.delete_workout(seeded, 1) is True
    assert app.delete_workout(seeded, 1) is False
    seeded.close()
    with Session(engine) as check:
        assert check.get(app.Workout, 1) is None and check.get(app.Workout, 2).name == "B"
''', mutations=[dict(name='update is not committed', old='session.commit()', new='session.flush()'),
                  dict(name='deletion reports false', old='return True', new='return False')]),
]

ONE_MANY = '''
class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    logs: list["LogEntry"] = Relationship(back_populates="workout")

class LogEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workout_id: int = Field(foreign_key="workout.id")
    sets: int
    reps: int
    weight: float = 0.0
    workout: Optional[Workout] = Relationship(back_populates="logs")
'''

SPECS.append(dict(number=5, contract='''Define `Workout(id, name, logs)` and `LogEntry(id, workout_id, sets, reps, weight, workout)`.
Both are tables. IDs default to `None`. Weight defaults to `0.0`. `workout_id` is a
required foreign key to `workout.id`. Use `Relationship(back_populates=...)` in both
directions. Implement `add_log(session, workout_id, sets, reps, weight=0.0)`.
Return `None` for a missing workout. Reject sets or reps below 1, and weight below 0,
with `ValueError`. Commit, refresh, and return each valid log.''',
    template=IMPORTS + '''
class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # Add the logs relationship.

class LogEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Add fields, the foreign key, and the workout relationship.

def add_log(session, workout_id, sets, reps, weight=0.0):
    raise NotImplementedError
''', reference=IMPORTS + ONE_MANY + '''
def add_log(session, workout_id, sets, reps, weight=0.0):
    if sets < 1 or reps < 1 or weight < 0:
        raise ValueError("Invalid performance")
    if session.get(Workout, workout_id) is None:
        return None
    row = LogEntry(workout_id=workout_id, sets=sets, reps=reps, weight=weight)
    session.add(row)
    session.commit()
    session.refresh(row)
    return row
''', tests=FIXTURES + '''
def test_foreign_key():
    assert {fk.target_fullname for fk in app.LogEntry.__table__.c.workout_id.foreign_keys} == {"workout.id"}

def test_empty_relationship(session):
    workout = app.Workout(name="A")
    session.add(workout)
    session.commit()
    assert workout.logs == []

def test_relationships_in_both_directions(session):
    session.add(app.Workout(id=1, name="A"))
    session.commit()
    row = app.add_log(session, 1, 3, 8, 42.5)
    assert row.id is not None and row.sets == 3 and row.reps == 8 and row.weight == 42.5
    assert row.workout.name == "A"
    assert row.workout.logs[0].id == row.id

def test_other_workouts_are_separate(session):
    session.add_all([app.Workout(id=1, name="A"), app.Workout(id=2, name="B")])
    session.commit()
    app.add_log(session, 1, 1, 1)
    app.add_log(session, 1, 2, 2)
    session.expire_all()
    assert len(session.get(app.Workout, 1).logs) == 2
    assert session.get(app.Workout, 2).logs == []

def test_missing_workout(session):
    assert app.add_log(session, 99, 1, 1) is None
    assert session.exec(select(app.LogEntry)).all() == []

def test_invalid_performance(session):
    session.add(app.Workout(id=1, name="A"))
    session.commit()
    for sets, reps, weight in [(0, 5, 1), (2, 0, 1), (2, 5, -0.1)]:
        with pytest.raises(ValueError):
            app.add_log(session, 1, sets, reps, weight)
    assert session.exec(select(app.LogEntry)).all() == []

def test_log_survives_a_new_session(session, engine):
    session.add(app.Workout(id=1, name="A"))
    session.commit()
    app.add_log(session, 1, 1, 1)
    session.close()
    with Session(engine) as check:
        assert check.exec(select(app.LogEntry)).one().weight == 0.0
''', mutations=[dict(name='zero sets allowed', old='sets < 1', new='sets < 0'),
               dict(name='log weight discarded', old='weight=weight)', new='weight=0.0)')]))
