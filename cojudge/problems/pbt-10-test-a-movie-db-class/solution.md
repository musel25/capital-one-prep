## Reference tests

```python
import sqlite3
import pytest
from movies import MovieDB

@pytest.fixture
def db():
    database = MovieDB()
    database.init()
    yield database
    database.drop_table()
    database.close()

def test_query(db):
    assert db.query() == [('Alien', 1979, 8.5), ('Arrival', 2016, 7.9), ('Moon', 2009, 7.8)]
    assert db.query(title='ali') == [('Alien', 1979, 8.5)]
    assert db.query(min_score=7.9) == [('Alien', 1979, 8.5), ('Arrival', 2016, 7.9)]
    assert db.query(year=2009) == [('Moon', 2009, 7.8)]
    assert db.query(title='a', min_score=8, year=2016) == []
    assert db.query(title="' OR 1=1 --") == []

def test_add_and_delete(db):
    db.add('Up', 2009, 8.3)
    assert db.query(title='Up') == [('Up', 2009, 8.3)]
    with pytest.raises(sqlite3.IntegrityError):
        db.add('Up', 2009, 8.3)
    assert db.delete('Up') == 1
    assert db.query(title='Up') == []
    assert db.delete('missing') == 0
    assert len(db.query()) == 3

def test_persistence_and_cleanup(tmp_path):
    path = tmp_path / 'movies.db'
    first = MovieDB(path)
    first.init()
    first.add('Up', 2009, 8.3)
    first.close()
    second = MovieDB(path)
    assert second.query(title='Up') == [('Up', 2009, 8.3)]
    assert second.delete('Up') == 1
    second.close()
    third = MovieDB(path)
    assert third.query(title='Up') == []
    third.drop_table()
    with pytest.raises(sqlite3.OperationalError):
        third.query()
    third.close()
```
