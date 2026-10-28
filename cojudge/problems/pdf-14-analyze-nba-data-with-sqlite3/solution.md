## Reference solution

Paste this code above the supplied tests and runner.

```python
import sqlite3

# Constructed practice data. These values are not historical NBA statistics.
PLAYERS = [
    ('Ada Guard', 'Blue', 24.0, 25),
    ('Ben Center', 'Blue', 18.0, 30),
    ('Cy Forward', 'Gold', 24.0, 28),
    ('Dee Guard', 'Gold', 12.0, 22),
    ('Eli Center', 'Red', None, 35),
]


def create_database(rows=None):
    """Return an open, independent in-memory database with a players table."""
    connection = sqlite3.connect(':memory:')
    connection.execute('CREATE TABLE players (name TEXT, team TEXT, points REAL, age INTEGER)')
    connection.executemany('INSERT INTO players VALUES (?, ?, ?, ?)',
                           PLAYERS if rows is None else rows)
    connection.commit()
    return connection


def get_players_for_team(connection, team):
    return connection.execute(
        'SELECT name, points FROM players WHERE team = ? ORDER BY points DESC, name ASC',
        (team,)).fetchall()


def get_top_scorers(connection, limit=3):
    if limit < 0:
        raise ValueError('limit must be nonnegative')
    return connection.execute(
        'SELECT name, team, points FROM players WHERE points IS NOT NULL '
        'ORDER BY points DESC, name ASC LIMIT ?', (limit,)).fetchall()


def get_average_points_by_team(connection):
    rows = connection.execute(
        'SELECT team, AVG(points) FROM players GROUP BY team '
        'HAVING COUNT(points) > 0 ORDER BY AVG(points) DESC, team ASC').fetchall()
    return [(team, round(average, 2)) for team, average in rows]


def get_player_count_by_age(connection, minimum_age):
    return connection.execute('SELECT COUNT(*) FROM players WHERE age >= ?',
                              (minimum_age,)).fetchone()[0]
```
