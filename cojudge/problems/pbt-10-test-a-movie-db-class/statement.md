# 10. Test a movie db class

Write **tests**, not the implementation. [Original Pybites exercise](https://pybitesplatform.com/bites/test-a-movie-db-class/).

This is an offline recreation from the public description. The original code and template are premium and were not available. The API below belongs to this recreation.

## Contract

MovieDB(path=":memory:") opens SQLite. init() creates and seeds the table with the three supplied rows. query(title=None, min_score=0, year=None) returns (title, year, score) tuples sorted by title. title is a case-insensitive SQL LIKE substring; min_score is inclusive; all filters combine. add inserts and commits; duplicate titles raise sqlite3.IntegrityError. delete removes an exact title, commits, and returns its row count. drop_table removes the table. close closes the connection. Use a yield fixture with teardown. Use tmp_path to test file persistence.

## Code to test

Import this module as `movies`. The judge supplies it automatically.

```python
import sqlite3

class MovieDB:
    def __init__(self, path=':memory:'):
        self.connection = sqlite3.connect(path)

    def init(self):
        self.connection.execute('CREATE TABLE movies (title TEXT PRIMARY KEY, year INTEGER, score REAL)')
        self.connection.executemany('INSERT INTO movies VALUES (?, ?, ?)',
            [('Alien', 1979, 8.5), ('Arrival', 2016, 7.9), ('Moon', 2009, 7.8)])
        self.connection.commit()

    def query(self, title=None, min_score=0, year=None):
        sql = 'SELECT title, year, score FROM movies WHERE score >= ?'
        args = [min_score]
        if title is not None:
            sql += ' AND title LIKE ?'
            args.append('%' + title + '%')
        if year is not None:
            sql += ' AND year = ?'
            args.append(year)
        return self.connection.execute(sql + ' ORDER BY title', args).fetchall()

    def add(self, title, year, score):
        self.connection.execute('INSERT INTO movies VALUES (?, ?, ?)', (title, year, score))
        self.connection.commit()

    def delete(self, title):
        cursor = self.connection.execute('DELETE FROM movies WHERE title = ?', (title,))
        self.connection.commit()
        return cursor.rowcount

    def drop_table(self):
        self.connection.execute('DROP TABLE movies')
        self.connection.commit()

    def close(self):
        self.connection.close()
```

## Your task

Scroll to **WRITE YOUR TESTS BELOW** in the editor. Replace the placeholder with `test_` functions. Keep the supplied target, runner, and adapter unchanged.

1. All tests must pass against the correct code.
2. Cover at least 90% of executable statements in the supplied target.
3. Detect every supplied faulty variant. A faulty variant is detected when at least one test fails against it.

**Run** checks the baseline and the first two faults. **Submit** checks the baseline and all 7 faults. `SURVIVED` identifies a fault your tests missed. A baseline failure shows the test name and error. Empty suites do not pass.

## Offline pytest support

The supplied runner implements the same small pytest subset used by the OOP course: `pytest.raises` (with `match`), `pytest.mark.parametrize`, function and yield fixtures, `pytest.approx` for numbers, `pytest.fail`, `capsys` / `capfd` for Python output, `monkeypatch`, and `tmp_path`. Standard-library `unittest.mock.patch` also works. Use function-scoped fixtures and top-level test functions. Plugins, async tests, pytest classes with setup hooks, skip/xfail, and advanced fixture scopes are not supported.

The judge uses Python 3.11 and no network. This runner measures statement coverage with Python tracing and uses explicit faulty variants. It does **not** run pytest-cov or mutatest. Its acceptance result is specific to this course.

For an older saved tab, use **+** to open the current template. Keep the old tab intact.
