## Reference solution

Paste this implementation above the supplied tests.

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship

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
```
