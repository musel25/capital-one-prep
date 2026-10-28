## Reference solution

Paste this code above the supplied tests and runner.

```python
import json
import re

def get_movie_data(files):
    movies = []
    for file in files:
        with open(file, encoding='utf-8') as source:
            movies.append(json.load(source))
    return movies

def get_single_comedy(movies):
    return next((movie for movie in movies
                 if 'Comedy' in [genre.strip() for genre in movie['Genre'].split(',')]), None)

def get_movie_most_nominations(movies):
    def nominations(movie):
        return sum(int(count) for count in re.findall(r'(\d+)\s+nominations?\b', movie['Awards']))
    return max(movies, key=nominations, default=None)

def get_movie_longest_runtime(movies):
    known = [movie for movie in movies if movie['Runtime'] != 'N/A']
    return max(known, key=lambda movie: int(movie["Runtime"].split()[0]), default=None)
```
