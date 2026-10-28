## Reference solution

Paste this implementation above the supplied tests.

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship

class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    muscle_group: str = ""

def get_workouts(session):
    return list(session.exec(select(Workout).order_by(Workout.id)).all())

def get_workout(session, workout_id):
    return session.get(Workout, workout_id)

def find_exercises(session, muscle_group=None):
    query = select(Exercise)
    if muscle_group is not None:
        query = query.where(Exercise.muscle_group == muscle_group)
    return list(session.exec(query.order_by(Exercise.id)).all())
```
