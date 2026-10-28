## Reference solution

Paste this implementation above the supplied tests.

```python
from typing import Optional
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship

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
```
