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
```
