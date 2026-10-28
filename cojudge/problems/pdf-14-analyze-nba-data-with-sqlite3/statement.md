In this Bite you are going to use `sqlite3`! We loaded some NBA data into a *players* DB table:

Complete the 4 functions after the *you code* comment, following their docstrings. You need to use different `SQL` queries to get the results.

Good luck and keep calm and code in Python!

The supplied `create_database` helper provides constructed practice data.

**Constraints:**

- Use SQL queries with parameters; order players by points descending, then name, with NULL points last.
- Top scorers exclude NULL points; negative limits raise `ValueError`; age counts include the minimum age.
- Team averages ignore NULL points, round to two decimals, and sort by unrounded average descending, then team name.
