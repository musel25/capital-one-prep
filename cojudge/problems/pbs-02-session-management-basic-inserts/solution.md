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
```
