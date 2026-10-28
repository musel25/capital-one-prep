# 06. Movie data analysis

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/movie-data-analysis/)

Implement `get_movies_by_director()`, `calc_mean_score(movies)`, and `get_average_scores(directors)`. `MOVIE_DATA` is a supplied local CSV path. Read it with `csv.DictReader`. Ignore rows missing director_name, movie_title, title_year, or imdb_score. Convert year to int and score to float. Include years >= MIN_YEAR (1960). Strip title whitespace. Return `defaultdict(list)` values containing `Movie(title, year, score)` records. `calc_mean_score` accepts a nonempty list of Movie records and rounds the mean to one decimal place. `get_average_scores` returns `(director, mean)` tuples for directors with at least MIN_MOVIES (4) films, highest rounded score first. Ties keep director insertion order. Present numeric CSV values are valid. An empty CSV produces an empty defaultdict.

**Source and offline changes:** The original free tests are retained, with added boundary tests. The template replaces the network download with a compressed copy of the original movie CSV. Only the four columns used in this exercise are retained. The public function signatures are unchanged.

<details>
<summary>Original public description</summary>

In this Bite we are going to parse a *csv* movie dataset to identify the directors with the *highest rated movies.*

1. Write `get_movies_by_director`: use `csv.DictReader` to convert *movie_metadata.csv* into a `(default)dict` of `list`s of *Movie* `namedtuple`s. Convert/filter the data:

  - Only extract director_name, movie_title, title_year and imdb_score, ignoring movies without all of these fields.
  - Type conversions: `title_year` -> `int` / `imdb_score` -> `float`
  - **Discard any movies older than 1960.**

Here is an extract:

```python
....
{ 'Woody Allen': [
    Movie(title='Midnight in Paris', year=2011, score=7.7),
    Movie(title='The Curse of the Jade Scorpion', year=2001, score=6.8),
    Movie(title='To Rome with Love', year=2012, score=6.3),  ....
    ], ...
}

```

1. Write the `calc_mean_score` helper that takes a list of Movie `namedtuple`s and calculates the mean IMDb score, returning the score rounded to 1 decimal place.
1. Complete `get_average_scores` which takes the directors data structure returned by `get_movies_by_director` (see 1.) and returns a list of tuples (`director`, `average_score`) ordered by highest score in descending order. Only take directors into account with >= `MIN_MOVIES`

See the tests for more info. This could be tough one, but we really hope you learn a thing or two. Good luck and keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`directors`. **Run** checks the first three tests. **Submit** checks all 17 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
