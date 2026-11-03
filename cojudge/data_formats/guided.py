"""Guided starters (the Pybites OOP bite 15 pattern) for the selected exercises.

Each entry keeps the original starter up to MARKER (imports, data and supplied
helpers) and replaces the rest with a short concept explanation, steps mapped
to the tests, and TODO comments with exact input and output examples. Tests
and references do not change.
"""

GUIDED = {
    2: ('def most_prolific_automaker', r'''# What you practise
# -----------------
# CARS is a list of dicts (parsed from JSON), one dict per car:
#     {'automaker': 'Dodge', 'model': 'Charger', 'year': 2008}
#
# 1. collections.Counter counts values. Counter(<generator>) counts every
#    item, and most_common(1) returns the top pair in a list:
#        Counter(['Dodge', 'Ford', 'Dodge']).most_common(1)  -> [('Dodge', 2)]
#    On a tie, the value that was counted FIRST wins.
# 2. A list comprehension with a condition filters records:
#        [car['model'] for car in cars if car['year'] == 2008]
#
# Work in two steps. The tests check both functions together, so finish both
# steps before you run the tests. Submit also runs the edge-case tests.
#
#   Step 1 (most_prolific_automaker)
#   Step 2 (get_models)


# Step 1: the automaker with the most cars in that year.
#
#     most_prolific_automaker(2008)        -> 'Dodge'
#     most_prolific_automaker(1800)        -> None     (no car from that year)
#     most_prolific_automaker(2000, [])    -> None
#
# Filter by year FIRST, then count.
def most_prolific_automaker(year, cars=CARS):
    """Return the automaker with the most cars in year, or None."""
    # TODO: counts = Counter(car['automaker'] for car in cars if car['year'] == year)
    # TODO: return counts.most_common(1)[0][0], or None if counts is empty.
    ...


# Step 2: the models of one automaker in one year, in input order.
#
#     get_models('Dodge', 2008)  -> ['Charger', 'Avenger']
#     get_models('dodge', 2008)  -> []                  (exact name only)
#
# Keep duplicates. Return a new list on every call.
def get_models(automaker, year, cars=CARS):
    """Return the model names for automaker and year."""
    # TODO: a list comprehension with two conditions: automaker AND year.
    ...
'''),

    4: ('# define namedtuple here', r'''# What you practise
# -----------------
# 1. namedtuple can build a record type at run time from a list of field
#    names. A dict gives the names (its keys) and the values:
#
#        Record = namedtuple('Record', ['name', 'site'])   <- the type
#        Record(name='PyBites', site='https://pybit.es')   <- one record
#
#    namedtuple('Record', some_dict) uses the keys of some_dict as field
#    names, in dict order. Record(**some_dict) passes the values by name.
#
# 2. nt._asdict() turns a namedtuple back into a dict, and json.dumps turns a
#    dict into JSON text. JSON has no datetime type: default=str tells
#    json.dumps to use str(value) for a value it cannot encode.
#
# Work in two steps. The tests run top to bottom. Submit also runs the
# edge-case tests.
#
#   Step 1 (dict2nt)  -> test_dict2nt
#   Step 2 (nt2json)  -> test_nt2json and the tests after it


# Step 1: dict -> namedtuple. Build the type from the keys of THIS dict, so
# every dict can have its own fields.
#
#     nt = dict2nt(blog)
#     nt.name         -> 'PyBites'
#     nt.founders[1]  -> 'Bob'
#     dict2nt({'z': 3, 'a': ['x']})._fields  -> ('z', 'a')
#     dict2nt({})._fields                    -> ()
def dict2nt(dict_):
    """Return a namedtuple with the keys of dict_ as fields."""
    # TODO: Record = namedtuple('Record', dict_)
    # TODO: return Record(**dict_)
    ...


# Step 2: namedtuple -> JSON text.
#
#     nt2json(dict2nt({'x': 1}))  -> '{"x": 1}'
#     nt2json(dict2nt(blog))      -> '{"name": "PyBites", ..., "started": "2016-12-19 00:00:00", ...}'
def nt2json(nt):
    """Return nt as a JSON string. Encode a datetime with str()."""
    # TODO: return json.dumps(nt._asdict(), default=str)
    ...
'''),

    5: ('def get_movie_data', r'''# What you practise
# -----------------
# 1. json.load(file) reads one JSON file into Python objects. Here each file
#    holds one movie dict, such as
#        {'Title': 'Up', 'Genre': 'Animation, Comedy', 'Awards': '...', 'Runtime': '96 min'}
#
# 2. next(<generator>, None) returns the FIRST matching item, or None:
#        next((m for m in movies if <condition>), None)
#
# 3. max(items, key=function, default=None) returns the item with the
#    largest key. On a tie, the FIRST of the tied items wins. default is
#    returned for an empty list.
#
# The supplied helpers give the key values: _genres(movie) -> list of genres,
# _nominations(movie) -> int, _minutes(movie) -> int or None.
#
# Work in four steps. The tests run top to bottom. Submit also runs the
# edge-case tests.
#
#   Step 1 (get_movie_data)              -> test_read_json_files_in_order
#   Step 2 (get_single_comedy)           -> test_comedy_token_and_first_match
#   Step 3 (get_movie_most_nominations)  -> the nominations tests
#   Step 4 (get_movie_longest_runtime)   -> the runtime tests and the rest


# Step 1: read each file in order. A file name can be a str or a Path.
#
#     get_movie_data(['a.json', 'b.json'])  -> [<movie dict of a>, <movie dict of b>]
#     get_movie_data([])                    -> []
def get_movie_data(files):
    """Return a list with the movie dict of each JSON file."""
    # TODO: for each file: with open(file, encoding='utf-8') as source:
    #           append json.load(source) to a list.
    # TODO: return the list.
    ...


# Step 2: the first movie whose genres include exactly 'Comedy'.
#
#     Genre 'Drama, Comedy, Romance'  -> match
#     Genre 'ComedyDrama'             -> no match (use _genres, not "in" on the text)
#     no comedy                       -> None
def get_single_comedy(movies):
    """Return the first comedy movie dict, or None."""
    # TODO: next((movie for movie in movies if 'Comedy' in _genres(movie)), None)
    ...


# Step 3: the movie with the most nominations ('N/A' counts as 0).
#
#     Awards '1 win & 12 nominations.' beats 'Won 2 Oscars. 100 wins & 9 nominations.'
#     empty list  -> None
def get_movie_most_nominations(movies):
    """Return the movie dict with the most nominations, or None."""
    # TODO: max(movies, key=_nominations, default=None)
    ...


# Step 4: the longest movie. Skip movies whose runtime is 'N/A' (_minutes
# returns None for them).
#
#     runtimes 'N/A', '99 min', '100 min'  -> the 100 min movie
#     only 'N/A'                            -> None
def get_movie_longest_runtime(movies):
    """Return the movie dict with the longest known runtime, or None."""
    # TODO: known = [movie for movie in movies if _minutes(movie) is not None]
    # TODO: return max(known, key=_minutes, default=None)
    ...
'''),

    9: ('def get_country', r'''# What you practise
# -----------------
# Calling a JSON web API with a requests-style client:
#
#     response = client.get(url)    <- one HTTP GET
#     data = response.json()        <- the JSON body as a dict
#     data['country']               <- one field
#
# The judge has no network, so the module-level name requests is a
# LocalClient with the same get()/json() interface. Tests can pass their own
# client, or replace the module-level requests.
#
# Dependency injection: get_country takes an optional client. When it is
# None, use the module-level requests. Read requests inside the function (on
# each call), so a test that replaces it is seen.
#
# There is one step. Every test calls get_country.


# Build the URL from IPINFO_URL, make one GET call, return the country code.
#
#     IPINFO_URL.format(ip='8.8.8.8')  -> 'https://ipinfo.io/8.8.8.8/json'
#
#     get_country()                    -> 'US'     (local data for 8.8.8.8)
#     get_country('1.1.1.1')           -> 'AU'
#     get_country('192.0.2.1', client) -> client.get('https://ipinfo.io/192.0.2.1/json')
#                                         .json()['country']
#
# Return the code unchanged ('gb' stays 'gb'). Do not catch errors: a missing
# 'country' key raises KeyError, and client errors reach the caller.
def get_country(ip="8.8.8.8", client=None):
    """Return the country code of ip from the ipinfo API."""
    # TODO: if client is None: client = requests
    # TODO: response = client.get(IPINFO_URL.format(ip=ip))
    # TODO: return response.json()['country']
    ...
'''),

    11: ('def convert_to_json', r'''# What you practise
# -----------------
# Turning rows of text into a list of dicts, then into JSON text:
#
#     header = ['id', 'name']
#     values = ['1', 'Ada']
#     dict(zip(header, values))   -> {'id': '1', 'name': 'Ada'}
#     json.dumps([{...}, {...}])  -> '[{"id": "1", "name": "Ada"}, ...]'
#
# The header row uses commas only. The data rows mix three delimiters
# (, | ;). The supplied _fields(line) splits one data row on all three.
#
# There is one step. Every test calls convert_to_json.


# Convert the messy CSV text into a JSON list of objects (one per data row).
#
#     convert_to_json('a,b,c,d\n1|2;3,4')  -> '[{"a": "1", "b": "2", "c": "3", "d": "4"}]'
#     convert_to_json('id,name\n001; Ada ') -> '[{"id": "001", "name": " Ada "}]'
#     convert_to_json('')                   -> '[]'
#     convert_to_json('a,b\n1')              -> raises ValueError (1 value, 2 columns)
#
# Rules: skip blank lines (also lines with only spaces). Keep every value as
# a str, exactly as it is (no strip, no int). Empty fields stay ''.
def convert_to_json(data=members):
    """Return a JSON string: a list with one dict per data row."""
    # TODO: lines = the lines of data (data.splitlines()) that are not blank.
    # TODO: if there are no lines, return json.dumps([]).
    # TODO: header = lines[0].split(',')
    # TODO: for each other line: values = _fields(line)
    #           if len(values) != len(header): raise ValueError(...)
    #           append dict(zip(header, values)) to a list.
    # TODO: return json.dumps(the list).
    ...
'''),

    12: ('class BiteStats:', r'''# What you practise
# -----------------
# 1. csv.DictReader reads CSV text into one dict per row. The header row gives
#    the keys, and every value is a str:
#        list(csv.DictReader(StringIO('bite,user,completed\n7,ada,True\n')))
#        -> [{'bite': '7', 'user': 'ada', 'completed': 'True'}]
#    So convert bite with int(), and compare completed with the text 'True'
#    ('False' is a non-empty string, so it is truthy).
# 2. Read-only properties that compute each statistic from self.rows.
# 3. collections.Counter counts values. The supplied _top(counter) returns the
#    key with the highest count (smallest key on a tie), or None.
#
# Work in three steps. The first test checks all six properties together, so
# finish all steps before you run the tests. Submit also runs edge-case tests.
#
#   Step 1 (__init__)     -> self.rows
#   Step 2 (four totals)
#   Step 3 (two "most")   -> then every test

# Example used in the comments below: LOG_DATA (6 rows).
#     bite  user  completed
#     102   alex  False
#     101   alex  True
#     29    bea   True
#     9     cy    False
#     101   bea   True
#     29    alex  False


class BiteStats:

    # Step 1: read the CSV once. Each object keeps its own list.
    #
    #     BiteStats().rows[0]  -> {'bite': '102', 'user': 'alex', 'completed': 'False'}
    def __init__(self, data=LOG_DATA):
        # TODO: self.rows = list(csv.DictReader(StringIO(data)))
        ...

    # Step 2: four totals.
    #
    #     total_attempts   -> 6    (rows)
    #     total_users      -> 3    (different users: alex, bea, cy)
    #     total_bites      -> 4    (different bites: 102, 101, 29, 9)
    #     total_completed  -> 3    (rows with completed == 'True')
    @property
    def total_attempts(self):
        # TODO: the number of rows.
        ...

    @property
    def total_users(self):
        # TODO: the size of the set of row['user'] values.
        ...

    @property
    def total_bites(self):
        # TODO: the size of the set of int(row['bite']) values.
        ...

    @property
    def total_completed(self):
        # TODO: count the rows where row['completed'] == 'True'.
        ...

    # Step 3: the most frequent user and bite. Use Counter, then _top.
    #
    #     most_active_user   -> 'alex'   (3 rows)
    #     most_popular_bite  -> 29       (an int; 101 and 29 have 2 rows each,
    #                                     and _top picks the smaller one)
    @property
    def most_active_user(self):
        # TODO: _top(Counter(row['user'] for row in self.rows))
        ...

    @property
    def most_popular_bite(self):
        # TODO: _top(Counter(int(row['bite']) for row in self.rows))
        ...
'''),

    14: ('def get_players_for_team', r'''# What you practise
# -----------------
# SQL queries from Python with the standard sqlite3 module:
#
#     rows = connection.execute(
#         'SELECT name, points FROM players WHERE team = ?',   <- ? is a placeholder
#         (team,),                                             <- values, as a tuple
#     ).fetchall()                                             <- list of tuples
#
# Always pass values through ? placeholders. Never build SQL with f-strings:
# a test sends "Blue' OR 1=1 --" as a team name.
#
# The table: players(name TEXT, team TEXT, points REAL, age INTEGER).
# points can be NULL (Python None). The tests check that each function runs
# real SQL (WHERE, ORDER BY, LIMIT, GROUP BY, AVG, COUNT). Read only: do not
# change the table, and do not close the connection.
#
# Work in four steps. The tests run top to bottom. Submit also runs the
# edge-case tests.
#
#   Step 1 (get_players_for_team)        -> the team tests
#   Step 2 (get_top_scorers)             -> the top scorer tests
#   Step 3 (get_average_points_by_team)  -> the average tests
#   Step 4 (get_player_count_by_age)     -> the age test and the rest


# Step 1: (name, points) of one team, highest points first, then name A-Z.
#
#     get_players_for_team(db, 'Blue')  -> [('Ada Guard', 24.0), ('Ben Center', 18.0)]
#     get_players_for_team(db, 'Red')   -> [('Eli Center', None)]
#     get_players_for_team(db, 'blue')  -> []        (exact name)
#
# SQL: SELECT name, points FROM players WHERE team = ? ORDER BY points DESC, name ASC
def get_players_for_team(connection, team):
    """Return a list of (name, points) tuples."""
    ...


# Step 2: the top `limit` players by points, skipping NULL points.
# On equal points, order by name. A negative limit raises ValueError.
#
#     get_top_scorers(db)     -> [('Ada Guard', 'Blue', 24.0),
#                                 ('Cy Forward', 'Gold', 24.0),
#                                 ('Ben Center', 'Blue', 18.0)]
#     get_top_scorers(db, 0)  -> []
#
# SQL: ... WHERE points IS NOT NULL ORDER BY points DESC, name ASC LIMIT ?
def get_top_scorers(connection, limit=3):
    """Return a list of (name, team, points) tuples."""
    # TODO: if limit < 0: raise ValueError(...)
    # TODO: run the query with (limit,) and return fetchall().
    ...


# Step 3: average points per team, rounded to 2 decimals in Python.
# AVG ignores NULL. Leave out a team whose points are all NULL.
# Highest average first (sort on the unrounded average), then team A-Z.
#
#     get_average_points_by_team(db)  -> [('Blue', 21.0), ('Gold', 18.0)]   ('Red' has no points)
#
# SQL: SELECT team, AVG(points) FROM players GROUP BY team
#      HAVING COUNT(points) > 0 ORDER BY AVG(points) DESC, team ASC
def get_average_points_by_team(connection):
    """Return a list of (team, average) tuples."""
    # TODO: run the query, then return [(team, round(average, 2)) for team, average in rows].
    ...


# Step 4: the number of players with age >= minimum_age (inclusive).
#
#     get_player_count_by_age(db, 30)  -> 2     (30 and 35)
#     get_player_count_by_age(db, 36)  -> 0
#
# SQL: SELECT COUNT(*) FROM players WHERE age >= ?
# fetchone() returns a tuple such as (2,). Return the number inside it.
def get_player_count_by_age(connection, minimum_age):
    """Return the count as an int."""
    ...
'''),
}

HINTS = {
    2: ['Concept: Counter counts values, and most_common(1) returns [(value, count)]. Filter the cars by year inside the generator that you give to Counter.',
        "most_prolific_automaker: Counter(car['automaker'] for car in cars if car['year'] == year). Return most_common(1)[0][0], or None when the Counter is empty.",
        "get_models: [car['model'] for car in cars if car['automaker'] == automaker and car['year'] == year]. Names must match exactly."],
    4: ["Concept: namedtuple('Record', fields) creates a record type at run time. A dict works as the list of fields: its keys become the field names, in order.",
        'dict2nt: build the type from this dict, then fill it with Record(**dict_). Do not define one fixed namedtuple: the tests use dicts with different keys.',
        'nt2json: nt._asdict() returns a dict. json.dumps(..., default=str) writes a datetime as text such as "2016-12-19 00:00:00".'],
    5: ["Concept: json.load(file) reads one JSON document. next(generator, None) finds the first match, and max(items, key=..., default=None) finds the largest by a key.",
        "get_movie_data opens each file with encoding='utf-8' and appends json.load(source). get_single_comedy checks 'Comedy' in _genres(movie), so 'ComedyDrama' does not match.",
        'Use max(movies, key=_nominations, default=None). For runtime, first drop movies where _minutes(movie) is None, then use max with key=_minutes and default=None.'],
    9: ['Concept: a client object makes the HTTP call: client.get(url) returns a response, and response.json() returns the body as a dict.',
        "Build the URL with IPINFO_URL.format(ip=ip). If client is None, use the module-level requests. Look it up inside the function, so a test can replace it.",
        "Return response.json()['country'] unchanged. Do not catch exceptions: the tests expect KeyError and client errors to reach the caller."],
    11: ['Concept: dict(zip(header, values)) pairs each column name with its value. json.dumps(list_of_dicts) returns the JSON text.',
         "Skip blank lines: keep only lines where line.strip() is not empty. The first kept line is the header; split it on ','. Split the other lines with _fields(line).",
         'If a row has a different number of values than the header, raise ValueError. Do not strip or convert the values. With no lines at all, return json.dumps([]).'],
    12: ["Concept: csv.DictReader(StringIO(data)) yields one dict per row with str values. Store list(...) as self.rows, and compute every property from it.",
         "Totals: len(self.rows); len of a set of users; len of a set of int(row['bite']); and sum(row['completed'] == 'True' for row in self.rows). The text 'False' is truthy, so compare with 'True'.",
         "Most active and most popular: _top(Counter(...)). Convert bite with int(), so most_popular_bite returns 29, not '29'."],
    14: ["Concept: connection.execute(sql, params).fetchall() returns a list of tuples. Put a ? in the SQL for each value and pass the values as a tuple, for example (team,).",
         'Sort in SQL with ORDER BY points DESC, name ASC. For the top scorers, add WHERE points IS NOT NULL and LIMIT ?. Raise ValueError for a negative limit before the query.',
         'Averages: GROUP BY team with HAVING COUNT(points) > 0, then round each average to 2 decimals in Python. Count: SELECT COUNT(*) ... WHERE age >= ?, then fetchone()[0].'],
}


def apply(spec):
    """Replace the starter and hints of a selected exercise."""
    number = spec['number']
    if number in GUIDED:
        marker, tail = GUIDED[number]
        template = spec['template']
        assert template.count(marker) == 1, (number, marker)
        spec = {**spec, 'template': template[:template.index(marker)] + tail,
                'hints': HINTS[number], 'guided': True}
    return spec
