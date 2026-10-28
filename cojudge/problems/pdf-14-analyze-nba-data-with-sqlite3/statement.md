# 14. Analyze nba data with sqlite3

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/analyze-nba-data-with-sqlite3/)

Use real `sqlite3` SELECT queries for the four functions. Each function receives an open connection with a `players(name TEXT, team TEXT, points REAL, age INTEGER)` table. Names are unique. Team names are nonempty, ages are integers, and points are nonnegative numbers or SQL NULL. `get_players_for_team(connection, team)` returns `(name, points)` tuples for an exact team match, ordered by points descending, then name ascending; NULL points come last. `get_top_scorers(connection, limit=3)` excludes NULL points and returns `(name, team, points)` tuples in the same order, limited to `limit` rows. A negative limit raises ValueError; zero returns an empty list. `get_average_points_by_team(connection)` returns `(team, average)` tuples, rounded to two decimal places and ordered by the unrounded average descending, then team ascending. Exclude teams whose points are all NULL; ignore NULL values in other averages. `get_player_count_by_age(connection, minimum_age)` returns an integer count of players whose age is at least minimum_age. Apply filtering, grouping, ordering, and limits in SQL. Use SQL parameters for input values. Do not change or close the connection. The supplied `create_database` helper creates deterministic local practice data; tests also supply other data.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The premium function signatures are unavailable. This version defines four explicit SQL queries against constructed local data. It preserves the public SQL analysis task.

<details>
<summary>Original public description</summary>

In this Bite you are going to use `sqlite3`! We loaded some NBA data into a *players* DB table:

Complete the 4 functions after the *you code* comment, following their docstrings. You need to use different `SQL` queries to get the results.

Good luck and keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`nba_sql`. **Run** checks the first three tests. **Submit** checks all 9 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
