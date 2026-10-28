"""Data Formats bites 14–17, recreated from the public descriptions."""
import json
from pathlib import Path

PAGES = json.loads((Path(__file__).parent / 'source-pages.json').read_text())
SPECS = []


def add(number, module, contract, header, starter, reference, tests, mutations, **extra):
    SPECS.append(dict(number=number, title=PAGES[number - 1]['title'], module=module,
                      contract=contract, template=header + starter,
                      reference=header + reference, tests=tests, mutations=mutations, **extra))


def fault(name, old, new):
    return dict(name=name, old=old, new=new)


NBA_HEADER = '''import sqlite3

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


'''

add(14, 'nba_sql',
    'Use real `sqlite3` SELECT queries for the four functions. Each function receives an open '
    'connection with a `players(name TEXT, team TEXT, points REAL, age INTEGER)` table. Names '
    'are unique. Team names are nonempty, ages are integers, and points are nonnegative numbers '
    'or SQL NULL. `get_players_for_team(connection, team)` returns `(name, points)` tuples for '
    'an exact team match, ordered by points descending, then name ascending; NULL points come '
    'last. `get_top_scorers(connection, limit=3)` excludes NULL points and returns '
    '`(name, team, points)` tuples in the same order, limited to `limit` rows. A negative limit '
    'raises ValueError; zero returns an empty list. `get_average_points_by_team(connection)` '
    'returns `(team, average)` tuples, rounded to two decimal places and ordered by the '
    'unrounded average descending, then team ascending. Exclude teams whose points are all '
    'NULL; ignore NULL values in other averages. `get_player_count_by_age(connection, '
    'minimum_age)` returns an integer count of players whose age is at least minimum_age. '
    'Apply filtering, grouping, ordering, and limits in SQL. Use SQL parameters for input '
    'values. Do not change or close the connection. The supplied `create_database` helper '
    'creates deterministic local practice data; tests also supply other data.',
    NBA_HEADER,
    '''def get_players_for_team(connection, team):
    pass


def get_top_scorers(connection, limit=3):
    pass


def get_average_points_by_team(connection):
    pass


def get_player_count_by_age(connection, minimum_age):
    pass
''',
    '''def get_players_for_team(connection, team):
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
''',
    '''import pytest
from nba_sql import (create_database, get_players_for_team, get_top_scorers,
                     get_average_points_by_team, get_player_count_by_age)

@pytest.fixture
def db():
    return create_database()

def test_team_filter_and_sort(db):
    assert get_players_for_team(db, 'Blue') == [('Ada Guard', 24.0), ('Ben Center', 18.0)]
    assert get_players_for_team(db, 'Red') == [('Eli Center', None)]
    other = create_database([('Z', 'X', None, 1), ('C', 'X', 0, 1),
                             ('B', 'X', 10, 1), ('A', 'X', 10, 1)])
    assert get_players_for_team(other, 'X') == [('A', 10.0), ('B', 10.0), ('C', 0.0), ('Z', None)]

def test_missing_and_exact_team_names(db):
    assert get_players_for_team(db, 'blue') == []
    assert get_players_for_team(db, 'missing') == []
    assert get_players_for_team(db, "Blue' OR 1=1 --") == []

def test_top_scorers_default_and_ties(db):
    assert get_top_scorers(db) == [('Ada Guard', 'Blue', 24.0),
                                  ('Cy Forward', 'Gold', 24.0),
                                  ('Ben Center', 'Blue', 18.0)]

def test_limit_boundaries_and_null_exclusion(db):
    assert get_top_scorers(db, 0) == []
    assert get_top_scorers(db, 1) == [('Ada Guard', 'Blue', 24.0)]
    assert len(get_top_scorers(db, 100)) == 4
    with pytest.raises(ValueError):
        get_top_scorers(db, -1)

def test_averages_and_nulls(db):
    assert get_average_points_by_team(db) == [('Blue', 21.0), ('Gold', 18.0)]
    other = create_database([('a', 'B', 1, 1), ('b', 'B', 2, 1),
                             ('c', 'A', 1.5, 1), ('d', 'B', None, 1),
                             ('e', 'C', None, 1)])
    assert get_average_points_by_team(other) == [('A', 1.5), ('B', 1.5)]

def test_average_rounding_and_raw_average_order():
    db = create_database([('a', 'A', 1.331, 1), ('b', 'Z', 1.334, 1)])
    assert get_average_points_by_team(db) == [('Z', 1.33), ('A', 1.33)]

def test_age_inclusive_boundary(db):
    assert get_player_count_by_age(db, 30) == 2
    assert get_player_count_by_age(db, 35) == 1
    assert get_player_count_by_age(db, 36) == 0
    assert get_player_count_by_age(db, -1) == 5

def test_empty_database_and_no_changes():
    db = create_database([])
    assert get_players_for_team(db, 'Blue') == []
    assert get_top_scorers(db) == []
    assert get_average_points_by_team(db) == []
    assert get_player_count_by_age(db, 0) == 0
    assert db.execute('SELECT COUNT(*) FROM players').fetchone() == (0,)

def test_real_sql_operations_and_connection_stays_open(db):
    statements = []
    db.set_trace_callback(statements.append)
    get_players_for_team(db, 'Blue')
    get_top_scorers(db, 2)
    get_average_points_by_team(db)
    get_player_count_by_age(db, 28)
    queries = [' '.join(statement.upper().split()) for statement in statements]
    assert any('WHERE' in sql and 'ORDER BY' in sql for sql in queries)
    assert any('ORDER BY' in sql and 'LIMIT' in sql for sql in queries)
    assert any('GROUP BY' in sql and 'AVG(' in sql for sql in queries)
    assert any('COUNT(' in sql and 'WHERE' in sql for sql in queries)
    assert not any(sql.startswith(('INSERT', 'UPDATE', 'DELETE', 'DROP')) for sql in queries)
    assert db.execute('SELECT COUNT(*) FROM players').fetchone() == (5,)
''',
    [fault('exclude exact age threshold', 'WHERE age >= ?', 'WHERE age > ?'),
     fault('sort lowest scorers first', 'ORDER BY points DESC, name ASC LIMIT',
           'ORDER BY points ASC, name ASC LIMIT'),
     fault('count null scores in averages', 'AVG(points)', 'SUM(points) / COUNT(*)')],
    notes='The premium function signatures are unavailable. This version defines four explicit '
          'SQL queries against constructed local data. It preserves the public SQL analysis task.')


STATS_HEADER = '''import csv
import io

BITE_STATS = """Bite;Difficulty
Bite 1. Sum n numbers;3.45
Bite 2. Regex Fun;4.89
Bite 3. Word Values;3.97
Bite 4. Top 10 PyBites tags;4.72
Bite 5. Parse a list of names;4.48
Bite 6. PyBites Die Hard;6.8
Bite 7. Parsing dates from logs;5.76
Bite 8. Rotate string characters;3.5
Bite 9. Palindromes;4.71
Bite 200. Minecraft Enchantable Items;None
"""


'''

add(15, 'bite_stats',
    'Implement `get_most_complex_bites(csv_file=None, n=10)`. Read a semicolon-separated UTF-8 '
    'CSV with headers `Bite;Difficulty`. `csv_file` is a local string or pathlib path. When it '
    'is None, parse the supplied `BITE_STATS` text instead. Support a UTF-8 byte order mark '
    '(BOM) at the start of a file. Return at most `n` `(bite_title, difficulty)` tuples, '
    'ordered by numeric difficulty descending. Keep source order for equal scores. Convert '
    'difficulty to float. Strip surrounding whitespace from the title and difficulty. Ignore '
    'blank difficulty values and the exact text `None`. Zero is a valid score. `n` is an '
    'integer; a negative n raises ValueError and zero returns an empty list. An empty dataset '
    'returns an empty list. Other nonnumeric difficulty values raise ValueError. The CSV has '
    'both named columns and can contain quoted fields. Do not change the source file.',
    STATS_HEADER,
    '''def get_most_complex_bites(csv_file=None, n=10):
    pass
''',
    '''def get_most_complex_bites(csv_file=None, n=10):
    if n < 0:
        raise ValueError('n must be nonnegative')
    if n == 0:
        return []
    if csv_file is None:
        text = BITE_STATS
    else:
        with open(csv_file, encoding='utf-8-sig', newline='') as handle:
            text = handle.read()
    result = []
    for row in csv.DictReader(io.StringIO(text), delimiter=';'):
        score = row['Difficulty'].strip()
        if score in ('', 'None'):
            continue
        result.append((row['Bite'].strip(), float(score)))
    return sorted(result, key=lambda item: -item[1])[:n]
''',
    '''import pytest
from bite_stats import get_most_complex_bites

def write_csv(tmp_path, text, bom=False):
    path = tmp_path / 'scores.csv'
    path.write_text(text, encoding='utf-8-sig' if bom else 'utf-8')
    return path

def test_default_local_data():
    result = get_most_complex_bites()
    assert len(result) == 9
    assert result[:3] == [('Bite 6. PyBites Die Hard', 6.8),
                          ('Bite 7. Parsing dates from logs', 5.76),
                          ('Bite 2. Regex Fun', 4.89)]
    assert result[-1] == ('Bite 1. Sum n numbers', 3.45)

def test_numeric_sort_and_top_n(tmp_path):
    path = write_csv(tmp_path, 'Bite;Difficulty\\nA;9.9\\nB;10.1\\nC;2.0\\n')
    assert get_most_complex_bites(path, 2) == [('B', 10.1), ('A', 9.9)]
    assert get_most_complex_bites(str(path), 1) == [('B', 10.1)]

def test_missing_scores_and_valid_zero(tmp_path):
    path = write_csv(tmp_path, 'Bite;Difficulty\\nA;None\\nB;\\nC;0\\nD;  None  \\n')
    assert get_most_complex_bites(path) == [('C', 0.0)]

def test_equal_scores_keep_file_order(tmp_path):
    path = write_csv(tmp_path, 'Bite;Difficulty\\nZ;5\\nA;5.0\\nM;5\\n')
    assert get_most_complex_bites(path, 2) == [('Z', 5.0), ('A', 5.0)]

def test_bom_quoted_fields_and_spaces(tmp_path):
    path = write_csv(tmp_path, 'Bite;Difficulty\\n"  Title; with punctuation  "; 7.25 \\n', True)
    before = path.read_bytes()
    assert get_most_complex_bites(path) == [('Title; with punctuation', 7.25)]
    assert path.read_bytes() == before

def test_empty_dataset_and_limit_boundaries(tmp_path):
    path = write_csv(tmp_path, 'Bite;Difficulty\\n')
    assert get_most_complex_bites(path) == []
    assert get_most_complex_bites(n=0) == []
    with pytest.raises(ValueError):
        get_most_complex_bites(n=-1)

def test_invalid_numeric_score(tmp_path):
    path = write_csv(tmp_path, 'Bite;Difficulty\\nA;unknown\\n')
    with pytest.raises(ValueError):
        get_most_complex_bites(path)
''',
    [fault('lexical difficulty ordering', '-item[1]', "str(item[1])"),
     fault('read BOM as part of header', "encoding='utf-8-sig'", "encoding='utf-8'"),
     fault('take one fewer result', '[:n]', '[:max(0, n - 1)]')],
    notes='The premium docstring and tests are unavailable. This version states its return '
          'shape, tie rule, and limit behavior explicitly. Its small local CSV uses the public '
          'description sample instead of a download.')


MARVEL_HEADER = ('import csv\n'
 'import io\n'
 'from typing import NamedTuple\n'
 '\n'
 '\n'
 'class Character(NamedTuple):\n'
 '    pid: str\n'
 '    name: str\n'
 '    sid: str\n'
 '    align: str\n'
 '    sex: str\n'
 '    appearances: str\n'
 '    year: str\n'
 '\n'
 '\n'
 '# Small constructed TSV with the fields shown in the public description.\n'
 "MARVEL_TSV = 'pid\\tname\\tsid\\talign\\tsex\\tappearances\\tyear\\n1678\\tSpider-Man\\tSecret "
 'Identity\\tGood Characters\\tMale Characters\\t4043\\t1962\\n2460\\tThor\\tNo Dual '
 'Identity\\tGood Characters\\tMale Characters\\t2258\\t1950\\n755266\\tThor\\tSecret '
 'Identity\\tBad Characters\\tMale Characters\\t1\\t1998\\n20704\\tThor\\t\\tBad Characters\\tMale '
 'Characters\\t\\t1954\\n100\\tStorm\\tPublic Identity\\tGood Characters\\tFemale '
 'Characters\\t1000\\t1975\\n101\\tJean Grey\\tPublic Identity\\tGood Characters\\tFemale '
 'Characters\\t1200\\t1963\\n102\\tUnknown\\t\\t\\t\\t\\t\\n103\\tPractice Hero\\t\\tGood '
 "Characters\\tGenderfluid Characters\\t2\\t1963\\n'\n"
 '\n'
 '\n'
 'def load_characters(tsv=MARVEL_TSV):\n'
 '    """Read the local TSV. Every stored field remains a string."""\n'
 "    return [Character(**row) for row in csv.DictReader(io.StringIO(tsv), delimiter='\\t')]\n"
 '\n'
 '\n'
 'characters = load_characters()\n'
 '\n'
 '\n')

add(16, 'marvel_data',
    'The supplied `Character` typed namedtuple has string fields `pid, name, sid, align, sex, '
    'appearances, year`. The supplied TSV loader creates the default `characters` list without '
    'network access. Each pid uniquely identifies a character; equal names with different '
    'pids are separate characters. Implement three functions. '
    '`most_popular_characters(data=characters, n=5)` returns up to n Character objects ordered '
    'by integer appearances descending, then numeric pid ascending. A blank appearance is '
    'zero. A negative n raises ValueError. `max_and_min_years_new_characters(data=characters)` '
    'counts characters introduced in each nonblank year. Return '
    '`((most_year, most_count), (least_year, least_count))` with integer years and counts. '
    'For ties, choose the earliest year in each result. If no character has a year, return '
    '`(None, None)`. `get_percentage_female_characters(data=characters)` returns the percentage '
    'whose sex is exactly `Female Characters`, rounded to two decimal places. Exclude blank '
    'sex values from the denominator; include every other specified gender. Return 0.0 '
    'if no genders are specified. All nonblank numeric fields contain nonnegative integer '
    'text. Do not change input lists or characters.',
    MARVEL_HEADER,
    '''def most_popular_characters(data=characters, n=5):
    pass


def max_and_min_years_new_characters(data=characters):
    pass


def get_percentage_female_characters(data=characters):
    pass
''',
    '''def most_popular_characters(data=characters, n=5):
    if n < 0:
        raise ValueError('n must be nonnegative')
    return sorted(data, key=lambda ch: (-int(ch.appearances or '0'), int(ch.pid)))[:n]


def max_and_min_years_new_characters(data=characters):
    counts = {}
    for character in data:
        if character.year:
            year = int(character.year)
            counts[year] = counts.get(year, 0) + 1
    if not counts:
        return None, None
    most = min(counts, key=lambda year: (-counts[year], year))
    least = min(counts, key=lambda year: (counts[year], year))
    return (most, counts[most]), (least, counts[least])


def get_percentage_female_characters(data=characters):
    specified = [ch for ch in data if ch.sex]
    if not specified:
        return 0.0
    female = sum(ch.sex == 'Female Characters' for ch in specified)
    return round(100 * female / len(specified), 2)
''',
    '''import pytest
from marvel_data import (Character, characters, load_characters, most_popular_characters,
                         max_and_min_years_new_characters, get_percentage_female_characters)

def hero(pid, name='Hero', appearances='', year='', sex=''):
    return Character(str(pid), name, '', '', sex, str(appearances), str(year))

def test_default_popularity_and_tsv_types():
    assert [ch.pid for ch in most_popular_characters()] == ['1678', '2460', '101', '100', '103']
    assert all(isinstance(ch, Character) for ch in characters)
    assert characters[3].appearances == ''

def test_distinct_characters_with_same_name():
    data = [hero(3, 'Thor', 10), hero(2, 'Thor', 11), hero(1, 'Other', 15)]
    assert [ch.pid for ch in most_popular_characters(data)] == ['1', '2', '3']
    assert max_and_min_years_new_characters([hero(1, 'Thor', year=2000),
                                           hero(2, 'Thor', year=2000)]) == ((2000, 2), (2000, 2))

def test_numeric_sort_pid_ties_and_blank_appearances():
    data = [hero(20, appearances=9), hero(10, appearances=10),
            hero(2, appearances=10), hero(1), hero(3, appearances=0)]
    assert [ch.pid for ch in most_popular_characters(data)] == ['2', '10', '20', '1', '3']

def test_popularity_limit_boundaries():
    data = [hero(1, appearances=2)]
    assert most_popular_characters(data, 0) == []
    assert most_popular_characters(data, 1) == data
    assert most_popular_characters([], 10) == []
    with pytest.raises(ValueError):
        most_popular_characters(data, -1)

def test_year_counts_defaults_and_ties():
    assert max_and_min_years_new_characters() == ((1963, 2), (1950, 1))
    data = [hero(1, year=2002), hero(2, year=2002), hero(3, year=2000),
            hero(4, year=2000), hero(5, year=2001), hero(6, year=1999)]
    assert max_and_min_years_new_characters(data) == ((2000, 2), (1999, 1))

def test_missing_and_single_year():
    assert max_and_min_years_new_characters([]) == (None, None)
    assert max_and_min_years_new_characters([hero(1)]) == (None, None)
    assert max_and_min_years_new_characters([hero(1, year=1962), hero(2)]) == ((1962, 1), (1962, 1))

def test_female_percentage_ignores_unspecified_gender():
    assert get_percentage_female_characters() == 28.57
    data = [hero(1, sex='Female Characters'), hero(2),
            hero(3, sex='Genderfluid Characters'), hero(4, sex='Male Characters')]
    assert get_percentage_female_characters(data) == 33.33

def test_percentage_zero_and_full_boundaries():
    assert get_percentage_female_characters([]) == 0.0
    assert get_percentage_female_characters([hero(1)]) == 0.0
    assert get_percentage_female_characters([hero(1, sex='Male Characters')]) == 0.0
    assert get_percentage_female_characters([hero(1, sex='Female Characters')]) == 100.0

def test_inputs_unchanged_and_new_results():
    data = [hero(2, appearances=1, year=2000), hero(1, appearances=2, year=2001)]
    before = list(data)
    result = most_popular_characters(data)
    max_and_min_years_new_characters(data)
    get_percentage_female_characters(data)
    assert data == before and result is not data
''',
    [fault('rank by appearance text length', "-int(ch.appearances or '0')",
           "-len(ch.appearances or '0')"),
     fault('include unspecified genders in denominator', 'len(specified), 2)', 'len(data), 2)'),
     fault('choose latest year for minimum tie', '(counts[year], year)', '(counts[year], -year)')],
    notes='The premium docstrings and tests are unavailable. This version defines return shapes '
          'and tie rules explicitly. Its TSV is a small local practice sample. Characters with '
          'equal names remain separate, as required by the public description.')


# David C. Lovelace's original graph is cyclic in this order. Each gesture beats
# the next seven. Store CSV input so the exercise still practices data parsing.
GESTURE_ORDER = ('rock', 'fire', 'scissors', 'snake', 'human', 'tree', 'wolf', 'sponge',
                 'paper', 'air', 'water', 'dragon', 'devil', 'lightning', 'gun')
RPS_CSV = 'winner,loser\n' + ''.join(
    f'{gesture},{GESTURE_ORDER[(index + offset) % 15]}\n'
    for index, gesture in enumerate(GESTURE_ORDER) for offset in range(1, 8))
RPS_HEADER = ('import csv\nimport io\n\n'
              f'GESTURES = {GESTURE_ORDER!r}\n'
              f'SCORES = {RPS_CSV!r}\n\n\n')

add(17, 'rps15',
    'Implement `_create_defeat_mapping(csv_text=SCORES)` and `get_winner(player1, player2)`. '
    '`SCORES` is a local CSV with columns `winner,loser`. Each row is a directed defeat edge '
    'from the original RPS15 graph: the winner defeats the loser. The helper returns a new '
    'dictionary mapping each listed winner to a set of its losers. Duplicate rows do not '
    'duplicate losers. A header-only CSV returns an empty dictionary. The CSV uses valid '
    'gesture names. `get_winner` accepts only strings that exactly match the lower-case '
    'names in `GESTURES`; do not strip whitespace or change case. Invalid values, including '
    'non-strings, raise ValueError. Validate both inputs before checking for a tie. Equal '
    'valid gestures return the string `Tie`. Otherwise return the lower-case text '
    '`<winner> defeats <loser>`, regardless of which argument wins. The graph has 15 gestures '
    'and 105 distinct unordered matchups. Use `_create_defeat_mapping` in `get_winner` to '
    'parse the supplied CSV and determine its outcomes.',
    RPS_HEADER,
    '''def _create_defeat_mapping(csv_text=SCORES):
    pass


def get_winner(player1, player2):
    pass
''',
    '''def _create_defeat_mapping(csv_text=SCORES):
    mapping = {}
    for row in csv.DictReader(io.StringIO(csv_text)):
        mapping.setdefault(row['winner'], set()).add(row['loser'])
    return mapping


def get_winner(player1, player2):
    for player in (player1, player2):
        if not isinstance(player, str) or player not in GESTURES:
            raise ValueError('unknown gesture')
    if player1 == player2:
        return 'Tie'
    mapping = _create_defeat_mapping()
    if player2 in mapping[player1]:
        winner, loser = player1, player2
    else:
        winner, loser = player2, player1
    return f'{winner} defeats {loser}'
''',
    '''import pytest
import rps15
from rps15 import GESTURES, _create_defeat_mapping, get_winner

# Explicit expected edges from the original graph, independent of the CSV parser.
BEATS = {
    'rock': 'fire scissors snake human tree wolf sponge',
    'fire': 'scissors snake human tree wolf sponge paper',
    'scissors': 'snake human tree wolf sponge paper air',
    'snake': 'human tree wolf sponge paper air water',
    'human': 'tree wolf sponge paper air water dragon',
    'tree': 'wolf sponge paper air water dragon devil',
    'wolf': 'sponge paper air water dragon devil lightning',
    'sponge': 'paper air water dragon devil lightning gun',
    'paper': 'air water dragon devil lightning gun rock',
    'air': 'water dragon devil lightning gun rock fire',
    'water': 'dragon devil lightning gun rock fire scissors',
    'dragon': 'devil lightning gun rock fire scissors snake',
    'devil': 'lightning gun rock fire scissors snake human',
    'lightning': 'gun rock fire scissors snake human tree',
    'gun': 'rock fire scissors snake human tree wolf',
}
MATCHUPS = [(winner, loser) for winner, losers in BEATS.items() for loser in losers.split()]

def test_every_original_matchup_in_both_argument_orders():
    for winner, loser in MATCHUPS:
        expected = f'{winner} defeats {loser}'
        assert get_winner(winner, loser) == expected
        assert get_winner(loser, winner) == expected

def test_every_valid_tie():
    for gesture in BEATS:
        assert get_winner(gesture, gesture) == 'Tie'

def test_mapping_exact_edges_and_degree():
    mapping = _create_defeat_mapping()
    assert mapping == {winner: set(losers.split()) for winner, losers in BEATS.items()}
    assert len(GESTURES) == 15 and sum(map(len, mapping.values())) == 105

def test_helper_parses_supplied_csv_and_duplicates():
    csv_text = 'winner,loser\\nrock,fire\\nrock,fire\\nrock,scissors\\npaper,rock\\n'
    assert _create_defeat_mapping(csv_text) == {'rock': {'fire', 'scissors'}, 'paper': {'rock'}}
    assert _create_defeat_mapping('winner,loser\\n') == {}

def test_invalid_strings_and_argument_positions():
    for invalid in ('Rock', ' rock', 'rock ', '', 'lizard', 'Tie'):
        with pytest.raises(ValueError):
            get_winner(invalid, 'rock')
        with pytest.raises(ValueError):
            get_winner('rock', invalid)
        with pytest.raises(ValueError):
            get_winner(invalid, invalid)

def test_nonstring_inputs_raise_valueerror():
    for invalid in (None, 1, [], {}, True):
        with pytest.raises(ValueError):
            get_winner(invalid, 'paper')
        with pytest.raises(ValueError):
            get_winner('paper', invalid)

def test_helper_returns_independent_sets():
    first = _create_defeat_mapping()
    first['rock'].clear()
    assert _create_defeat_mapping()['rock'] == set(BEATS['rock'].split())

def test_get_winner_uses_csv_mapping(monkeypatch):
    monkeypatch.setattr(rps15, '_create_defeat_mapping',
                        lambda: {'rock': set(), 'fire': {'rock'}})
    assert get_winner('rock', 'fire') == 'fire defeats rock'
''',
    [fault('reverse defeat direction', "if player2 in mapping[player1]:", "if player1 in mapping[player2]:"),
     fault('accept unknown gesture strings',
           'if not isinstance(player, str) or player not in GESTURES:',
           'if not isinstance(player, str):'),
     fault('discard earlier CSV edges', "mapping.setdefault(row['winner'], set()).add(row['loser'])",
           "mapping[row['winner']] = {row['loser']}")],
    notes='The premium CSV, docstring, and original RPS15 phrase tests are unavailable. The '
          'local CSV preserves all 105 defeat relationships from '
          '[David C. Lovelace’s RPS15 graph](https://www.umop.com/rps15.htm). Output is '
          'simplified to "winner defeats loser"; it does not reproduce the original action phrases.')
