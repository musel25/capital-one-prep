## Reference solution

Paste this code above the supplied tests and runner.

```python
from dataclasses import dataclass
from datetime import datetime
@dataclass
class Actor:
    name: str
    born: str
@dataclass
class Movie:
    title: str
    release_date: str
def get_age(actor, movie):
    born = datetime.strptime(actor.born, '%B %d, %Y').date()
    released = datetime.strptime(movie.release_date, '%B %d, %Y').date()
    if released < born:
        raise ValueError('Release before birth')
    age = released.year - born.year - ((released.month, released.day) < (born.month, born.day))
    return f'{actor.name} was {age} years old when {movie.title} came out.'
```
