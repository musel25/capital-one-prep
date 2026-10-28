"""FastAPI exercises run through TestClient against real in-memory SQLite."""
from .bites import IMPORTS
from .relationships import SCHEMAS, LINKED

API_IMPORTS = '''from fastapi import FastAPI, Depends, HTTPException, Query, Response
'''

HEADER = '''
def create_app(engine):
    SQLModel.metadata.create_all(engine)
    app = FastAPI()

    def get_session():
        with Session(engine) as session:
            yield session
'''

BASIC_ROUTES = '''
    @app.post("/workouts", response_model=WorkoutRead, status_code=201)
    def create_workout(data: WorkoutCreate, session: Session = Depends(get_session)):
        row = Workout.model_validate(data)
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @app.get("/workouts", response_model=list[WorkoutRead])
    def list_workouts(offset: int = Query(default=0, ge=0), limit: int = Query(default=100, ge=1, le=100), session: Session = Depends(get_session)):
        return session.exec(select(Workout).order_by(Workout.id).offset(offset).limit(limit)).all()

    @app.get("/workouts/{workout_id}", response_model=WorkoutRead)
    def read_workout(workout_id: int, session: Session = Depends(get_session)):
        row = session.get(Workout, workout_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Workout not found")
        return row

    @app.delete("/workouts/{workout_id}", status_code=204)
    def delete_workout(workout_id: int, session: Session = Depends(get_session)):
        row = session.get(Workout, workout_id)
        if row is None:
            raise HTTPException(status_code=404, detail="Workout not found")
        session.delete(row)
        session.commit()
        return Response(status_code=204)
'''

API_FIXTURES = '''import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool
import workout_app as app

@pytest.fixture
def engine():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def client(engine):
    with TestClient(app.create_app(engine)) as client:
        yield client

'''

BASIC_TESTS = '''
def test_factory_initializes_tables():
    from sqlalchemy import inspect
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    try:
        app.create_app(engine)
        assert set(inspect(engine).get_table_names()) == set(SQLModel.metadata.tables)
    finally:
        engine.dispose()

def test_empty_list(client):
    response = client.get("/workouts")
    assert response.status_code == 200 and response.json() == []

def test_create_and_read(client):
    response = client.post("/workouts", json={"name": "Upper", "description": "Press"})
    assert response.status_code == 201
    row = response.json()
    assert isinstance(row["id"], int)
    assert row == {"id": row["id"], "name": "Upper", "description": "Press"}
    assert client.get(f"/workouts/{row['id']}").json() == row

def test_create_is_durable(client, engine):
    row = client.post("/workouts", json={"name": "Legs", "id": 9999}).json()
    assert row["description"] == "" and row["id"] != 9999
    with Session(engine) as session:
        assert session.get(app.Workout, row["id"]).name == "Legs"

def test_invalid_body(client):
    for body in ({}, {"name": ""}, {"name": None}, {"name": []}):
        assert client.post("/workouts", json=body).status_code == 422
    assert client.get("/workouts").json() == []

def test_missing_and_invalid_id(client):
    assert client.get("/workouts/999").status_code == 404
    assert client.delete("/workouts/999").status_code == 404
    assert client.get("/workouts/abc").status_code == 422

def test_order_and_pagination(client):
    for name in ("Z", "A", "B"):
        assert client.post("/workouts", json={"name": name}).status_code == 201
    assert [row["name"] for row in client.get("/workouts?offset=1&limit=1").json()] == ["A"]
    assert client.get("/workouts?offset=10").json() == []
    for query in ("offset=-1", "limit=0", "limit=101", "limit=abc"):
        assert client.get("/workouts?" + query).status_code == 422

def test_delete_preserves_other_rows(client, engine):
    first = client.post("/workouts", json={"name": "First"}).json()["id"]
    second = client.post("/workouts", json={"name": "Second"}).json()["id"]
    response = client.delete(f"/workouts/{first}")
    assert response.status_code == 204 and response.content == b""
    assert client.get(f"/workouts/{first}").status_code == 404
    assert client.get(f"/workouts/{second}").status_code == 200
    with Session(engine) as session:
        assert session.get(app.Workout, first) is None
'''

SPECS = [dict(number=9, contract='''Implement `create_app(engine)` and return a FastAPI app. Models and the session
dependency are supplied. Create the tables in the supplied engine. Use a session
dependency for each request. Implement these endpoints:

- `POST /workouts`: accept `WorkoutCreate`, commit and refresh a row, return `WorkoutRead` with status 201. The client cannot choose its ID.
- `GET /workouts`: return rows in ID order. Support `offset=0` (minimum 0) and `limit=100` (range 1–100).
- `GET /workouts/{workout_id}`: return a row or 404.
- `DELETE /workouts/{workout_id}`: commit deletion and return an empty 204 response, or 404.

Use FastAPI validation: invalid bodies, IDs, and pagination return 422. Tests use
TestClient and a supplied in-memory engine. Do not start a server or use the network.''',
    template=IMPORTS + API_IMPORTS + SCHEMAS + HEADER + '''
    # Add the four routes here. Use the supplied get_session dependency.
    return app
''', reference=IMPORTS + API_IMPORTS + SCHEMAS + HEADER + BASIC_ROUTES + '\n    return app\n',
    tests=API_FIXTURES + BASIC_TESTS,
    mutations=[dict(name='creation returns wrong status', old='status_code=201', new='status_code=200'),
               dict(name='pagination ignores offset', old='.offset(offset)', new='.offset(0)'),
               dict(name='factory does not create tables', old='SQLModel.metadata.create_all(engine)', new='pass')])]

API_SCHEMAS = '''
class WorkoutCreate(SQLModel):
    name: str = Field(min_length=1)
    description: str = ""

class WorkoutRead(WorkoutCreate):
    id: int

class LogCreate(SQLModel):
    workout_exercise_id: int
    sets: int = Field(ge=1)
    reps: int = Field(ge=1)
    weight: float = Field(default=0.0, ge=0)

class LogRead(LogCreate):
    id: int

class ExerciseRead(SQLModel):
    id: int
    name: str
'''

COMPLEX_ROUTES = '''
    @app.post("/logs", response_model=LogRead, status_code=201)
    def create_log(data: LogCreate, session: Session = Depends(get_session)):
        if session.get(WorkoutExercise, data.workout_exercise_id) is None:
            raise HTTPException(status_code=404, detail="Workout/exercise pair not found")
        row = LogEntry.model_validate(data)
        session.add(row)
        session.commit()
        session.refresh(row)
        return row

    @app.get("/logs", response_model=list[LogRead])
    def list_logs(workout_id: Optional[int] = None, exercise_id: Optional[int] = None, session: Session = Depends(get_session)):
        query = select(LogEntry).join(WorkoutExercise)
        if workout_id is not None:
            query = query.where(WorkoutExercise.workout_id == workout_id)
        if exercise_id is not None:
            query = query.where(WorkoutExercise.exercise_id == exercise_id)
        return session.exec(query.order_by(LogEntry.id)).all()

    @app.get("/workouts/{workout_id}/exercises", response_model=list[ExerciseRead])
    def workout_exercises(workout_id: int, session: Session = Depends(get_session)):
        if session.get(Workout, workout_id) is None:
            raise HTTPException(status_code=404, detail="Workout not found")
        query = select(Exercise).join(WorkoutExercise).where(WorkoutExercise.workout_id == workout_id).distinct().order_by(Exercise.id)
        return session.exec(query).all()
'''

COMPLEX_TESTS = '''
@pytest.fixture
def seeded(client, engine):
    with Session(engine) as session:
        session.add_all([app.Workout(id=1, name="Upper"), app.Workout(id=2, name="Push"), app.Workout(id=3, name="Rest"), app.Exercise(id=1, name="Bench"), app.Exercise(id=2, name="Rows")])
        session.commit()
        session.add_all([app.WorkoutExercise(id=10, workout_id=1, exercise_id=1), app.WorkoutExercise(id=20, workout_id=2, exercise_id=1), app.WorkoutExercise(id=30, workout_id=1, exercise_id=2)])
        session.commit()
    return client

@pytest.fixture
def logged(seeded):
    for pair, weight in [(10, 50), (20, 30), (30, 20)]:
        response = seeded.post("/logs", json={"workout_exercise_id": pair, "sets": 3, "reps": 8, "weight": weight})
        assert response.status_code == 201
    return seeded

def test_create_log_and_persist(seeded, engine):
    response = seeded.post("/logs", json={"workout_exercise_id": 10, "sets": 1, "reps": 2})
    assert response.status_code == 201
    row = response.json()
    assert row == {"id": row["id"], "workout_exercise_id": 10, "sets": 1, "reps": 2, "weight": 0.0}
    with Session(engine) as session:
        assert session.get(app.LogEntry, row["id"]).reps == 2

def test_missing_pair(seeded):
    response = seeded.post("/logs", json={"workout_exercise_id": 999, "sets": 1, "reps": 1})
    assert response.status_code == 404
    assert seeded.get("/logs").json() == []

def test_invalid_log_body(seeded):
    base = {"workout_exercise_id": 10, "sets": 1, "reps": 1}
    for field, value in [("sets", 0), ("reps", 0), ("weight", -1), ("workout_exercise_id", "bad")]:
        assert seeded.post("/logs", json={**base, field: value}).status_code == 422
    assert seeded.post("/logs", json={}).status_code == 422
    assert seeded.get("/logs").json() == []

def test_list_all_in_id_order(logged):
    response = logged.get("/logs")
    assert response.status_code == 200
    assert [row["weight"] for row in response.json()] == [50, 30, 20]

def test_filter_by_workout(logged):
    assert [row["weight"] for row in logged.get("/logs?workout_id=1").json()] == [50, 20]

def test_filter_by_exercise(logged):
    assert [row["weight"] for row in logged.get("/logs?exercise_id=1").json()] == [50, 30]

def test_combined_filters_are_intersection(logged):
    assert [row["weight"] for row in logged.get("/logs?workout_id=1&exercise_id=1").json()] == [50]
    assert logged.get("/logs?workout_id=2&exercise_id=2").json() == []
    assert logged.get("/logs?workout_id=999").json() == []
    assert logged.get("/logs?workout_id=0").json() == []
    assert logged.get("/logs?exercise_id=0").json() == []
    assert logged.get("/logs?exercise_id=bad").status_code == 422

def test_workout_exercises(seeded):
    response = seeded.get("/workouts/1/exercises")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Bench"}, {"id": 2, "name": "Rows"}]
    assert seeded.get("/workouts/2/exercises").json() == [{"id": 1, "name": "Bench"}]
    assert seeded.get("/workouts/3/exercises").json() == []
    assert seeded.get("/workouts/99/exercises").status_code == 404

def test_duplicate_links_return_distinct_exercises(seeded, engine):
    with Session(engine) as session:
        session.add(app.WorkoutExercise(id=40, workout_id=1, exercise_id=1))
        session.commit()
    assert seeded.get("/workouts/1/exercises").json() == [{"id": 1, "name": "Bench"}, {"id": 2, "name": "Rows"}]
'''

ADVANCED_MODELS = LINKED.replace('    exercise_links:', '    description: str = ""\n    exercise_links:')
COMPLEX_STARTER = '''
    @app.post("/logs", response_model=LogRead, status_code=201)
    def create_log(data: LogCreate, session: Session = Depends(get_session)):
        raise NotImplementedError

    @app.get("/logs", response_model=list[LogRead])
    def list_logs(workout_id: Optional[int] = None, exercise_id: Optional[int] = None, session: Session = Depends(get_session)):
        raise NotImplementedError

    @app.get("/workouts/{workout_id}/exercises", response_model=list[ExerciseRead])
    def workout_exercises(workout_id: int, session: Session = Depends(get_session)):
        raise NotImplementedError
'''

SPECS.append(dict(number=10, contract='''The models and basic workout endpoints are supplied. Complete the three new routes
inside `create_app(engine)`. Keep the basic endpoints working.

- `POST /logs`: accept `LogCreate`. Require an existing workout/exercise link. Return 404 for a missing pair. Commit and refresh a valid log. Return `LogRead` with status 201. Sets and reps must be at least 1. Weight defaults to zero and must be nonnegative. Invalid bodies return 422.
- `GET /logs`: return logs in ID order. Optional integer `workout_id` and `exercise_id` filters use the link table. Apply both filters together. Missing matches return an empty list. Invalid query values return 422.
- `GET /workouts/{workout_id}/exercises`: return distinct `ExerciseRead` objects in ID order. An empty workout returns an empty list. A missing workout returns 404.

TestClient supplies a fresh SQLite engine. The same exercise can appear in different
workouts. A log must stay attached to its exact workout/exercise pair.''',
    template=IMPORTS + API_IMPORTS + ADVANCED_MODELS + API_SCHEMAS + HEADER + BASIC_ROUTES + COMPLEX_STARTER + '\n    return app\n',
    reference=IMPORTS + API_IMPORTS + ADVANCED_MODELS + API_SCHEMAS + HEADER + BASIC_ROUTES + COMPLEX_ROUTES + '\n    return app\n',
    tests=API_FIXTURES + BASIC_TESTS + COMPLEX_TESTS,
    mutations=[dict(name='exercise filter omitted', old='query = query.where(WorkoutExercise.exercise_id == exercise_id)', new='query = query'),
               dict(name='missing pair returns wrong status', old='status_code=404, detail="Workout/exercise pair not found"', new='status_code=400, detail="Workout/exercise pair not found"'),
               dict(name='factory does not create tables', old='SQLModel.metadata.create_all(engine)', new='pass'),
               dict(name='duplicate exercises returned', old='.distinct()', new='')]))
