## Reference solution

Paste this implementation above the supplied tests.

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship

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

def link_exercise(session, workout_id, exercise_id):
    if session.get(Workout, workout_id) is None or session.get(Exercise, exercise_id) is None:
        return False
    if session.get(WorkoutExercise, (workout_id, exercise_id)) is None:
        session.add(WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id))
        session.commit()
    return True
```
