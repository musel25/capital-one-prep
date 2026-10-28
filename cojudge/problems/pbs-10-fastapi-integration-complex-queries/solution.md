## Reference solution

Paste this implementation above the supplied tests.

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship
from fastapi import FastAPI, Depends, HTTPException, Query, Response

class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""
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

    return app
```
