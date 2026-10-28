In this Bite you will use `ElementTree` to parse some [Nolan movies](http://www.imdb.com/name/nm0634240/) we extracted from [OMDb](https://www.omdbapi.com).

Luckily most APIs switched to *JSON*, but sometimes *XML* is all there is, so at least learn to parse some! Complete the `get_tree`, `get_movies` and `get_movie_longest_runtime` functions below. See the docstrings and tests for more info.

Have fun and remember:

> Keep calm and code in Python!

The supplied XML replaces the external movie data.

**Constraints:**

- `get_tree` returns a root element; `get_movies` returns attribute dictionaries in document order.
- Runtime is `N min` or `N/A`; ignore unknown runtimes, keep the first tie, and return `None` if none are known.
