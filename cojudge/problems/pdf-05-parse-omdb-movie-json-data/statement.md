# 05. Parse omdb movie json data

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/parse-omdb-movie-json-data/)

Implement `get_movie_data(files)`, `get_single_comedy(movies)`, `get_movie_most_nominations(movies)`, and `get_movie_longest_runtime(movies)`. Read each UTF-8 JSON file path into one movie dictionary and return a list in path order. Paths can be strings or pathlib Paths. The other functions return whole movie dictionaries, or `None` for no matching movie. Find the first movie with the exact `Comedy` token in comma-separated `Genre`. For nominations, sum integers directly before `nomination` or `nominations` in `Awards`. A missing such phrase, including `N/A`, counts as zero. Other award counts do not count. Runtime is `N min` or `N/A`; ignore `N/A` and compare numeric minutes. Numeric ties keep first input order. All movies contain `Title`, `Genre`, `Awards`, and `Runtime`. Return `None` for an empty movie list. Do not change the input.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The premium template and tests are recreated. Tests write small constructed OMDb-style JSON files locally. Award parsing and empty-input rules are explicit for this version; no external data download is required.

<details>
<summary>Original public description</summary>

Working with APIs is very common these days and lucky for us they increasingly return *JSON* (over *XML*). We saved [OMDb](http://www.omdbapi.com/) responses for some cool movies [into a file](https://bites-data.s3.us-east-2.amazonaws.com/omdb_data) that the tests load in.

Parse this data answering some questions:

1. `get_movie_data` consumes a list of movie json files (1 movie per file), returning a list of movie dicts, so for each movie you convert the json file to a `dict`.
1. now you have the data structure, loop through the movies and return the movie:

  - with Comedy in Genres (`get_single_comedy`)
  - that had the most nominations (`get_movie_most_nominations`)
  - having the longest runtime (`get_movie_longest_runtime`)

Expect to do some string parsing and type conversions here. We hope you like it, enjoy!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`omdb_movies`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
