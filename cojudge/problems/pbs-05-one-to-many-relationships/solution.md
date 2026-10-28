## Reference solution

Paste this implementation above the supplied tests.

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship

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
```
