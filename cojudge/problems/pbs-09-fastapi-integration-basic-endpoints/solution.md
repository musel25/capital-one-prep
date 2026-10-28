## Reference solution

Paste this implementation above the supplied tests.

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship
from fastapi import FastAPI, Depends, HTTPException, Query, Response

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

def create_app(engine):
    SQLModel.metadata.create_all(engine)
    app = FastAPI()

    def get_session():
        with Session(engine) as session:
            yield session

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

    return app
```
