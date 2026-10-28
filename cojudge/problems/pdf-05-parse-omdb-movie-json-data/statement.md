Working with APIs is very common these days and lucky for us they increasingly return *JSON* (over *XML*). We saved [OMDb](http://www.omdbapi.com/) responses for some cool movies [into a file](https://bites-data.s3.us-east-2.amazonaws.com/omdb_data) that the tests load in.

Parse this data answering some questions:

1. `get_movie_data` consumes a list of movie json files (1 movie per file), returning a list of movie dicts, so for each movie you convert the json file to a `dict`.
1. now you have the data structure, loop through the movies and return the movie:

  - with Comedy in Genres (`get_single_comedy`)
  - that had the most nominations (`get_movie_most_nominations`)
  - having the longest runtime (`get_movie_longest_runtime`)

Expect to do some string parsing and type conversions here. We hope you like it, enjoy!

Tests supply local OMDb-style JSON files.

**Constraints:**

- Return whole movie dictionaries; ties keep input order and absent matches return `None`.
- Match `Comedy` as a genre token; count only nominations, not wins; ignore `N/A` runtimes.
