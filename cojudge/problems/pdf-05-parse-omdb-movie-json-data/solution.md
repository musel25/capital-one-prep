## Reference solution

Paste this code above the supplied tests and runner.

```python
import json
import re

# FOCUS: read the JSON files by hand with json.load, then pick movies with next() and max().
# SUPPLIED: the three helpers below parse the Genre, Awards and Runtime text.
#        They are not the skill of this exercise. Use them. Do not edit them.


def _genres(movie):
    """'Drama, Comedy' -> ['Drama', 'Comedy']"""
    return [genre.strip() for genre in movie['Genre'].split(',')]


def _nominations(movie):
    """'Won 2 Oscars. 1 win & 12 nominations.' -> 12. 'N/A' -> 0."""
    return sum(int(count) for count in re.findall(r'(\d+)\s+nominations?\b', movie['Awards']))


def _minutes(movie):
    """'113 min' -> 113. 'N/A' -> None."""
    return None if movie['Runtime'] == 'N/A' else int(movie['Runtime'].split()[0])


def get_movie_data(files):
    movies = []
    for file in files:
        with open(file, encoding='utf-8') as source:
            movies.append(json.load(source))
    return movies

def get_single_comedy(movies):
    return next((movie for movie in movies
                 if 'Comedy' in _genres(movie)), None)

def get_movie_most_nominations(movies):
    return max(movies, key=_nominations, default=None)

def get_movie_longest_runtime(movies):
    known = [movie for movie in movies if _minutes(movie) is not None]
    return max(known, key=_minutes, default=None)
```
