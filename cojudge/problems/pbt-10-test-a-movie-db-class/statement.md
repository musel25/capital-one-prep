Time for fixtures, one of pytest's killer features or as Brian Okken said: pytest fixtures are one of the unique core features that make pytest stand out above other test frameworks, and are the reason why many people switch to and stay with pytest (Python Testing with pytest).

Why fixtures? The purpose of test fixtures is to provide a fixed baseline upon which tests can reliably and repeatedly execute. pytest fixtures offer dramatic improvements over the classic xUnit style of setup/teardown functions (docs).

In this Bite we wrote a little movie DB using sqlite3. The idea is that you write a db fixture to instantiate this class and run its init method to get the movies table created and populated.

At the end of the fixture you use drop_table to undo any changes.

Apart from this setup and teardown there are 3 methods you need to test: query, add and delete. Specially query has various args, so make sure you test them all. Apart from the docs we also wrote an article on fixtures you might want to check out: All You Need to Know to Start Using Fixtures in Your pytest Code. Let us know on Twitter when you finish our pytest learning path ...

Good luck and keep calm and code in Python / pytest!

For this version, write tests for the supplied code. Your tests must pass against the correct code, cover at least 90% of its executable statements, and detect every supplied faulty version. A fault is detected when at least one test fails. An empty test suite does not pass.

Import the target as `movies`. The judge supplies it automatically.

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
