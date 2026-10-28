"""Offline recreations of the premium Data Formats exercises 1, 2, 3, 5, 7."""
import json
from pathlib import Path

PAGES = {page['n']: page for page in json.loads(
    (Path(__file__).parent / 'source-pages.json').read_text())}
SPECS = []


def add(number, module, contract, header, template, tests, mutations, notes, reference):
    SPECS.append(dict(number=number, title=PAGES[number]['title'], module=module,
                      contract=contract, template=header + template,
                      reference=header + reference, tests=tests, mutations=mutations,
                      original=False, notes=notes))


def fault(name, old, new):
    return dict(name=name, old=old, new=new)


_XML = ('<root response="True"><movie title="Memento" year="2000" runtime="113 min"/>'
        '<movie title="The Dark Knight" year="2008" runtime="152 min"/>'
        '<movie title="Interstellar" year="2014" runtime="169 min"/></root>')
add(1, 'xml_movies',
    'Implement `get_tree(xml=XML)`, `get_movies(tree)`, and '
    '`get_movie_longest_runtime(movies)`. Parse XML text into an ElementTree root '
    '`Element`. Return a list of dictionaries copied from every `<movie>` '
    'element in the tree, in document order. Movie data is in XML attributes. Runtime values are '
    '`N min` with nonnegative integers, or `N/A`. Return the whole movie dictionary '
    'with the largest numeric runtime. Ignore `N/A`. Ties keep the first movie. '
    'Return `None` if there is no numeric runtime. Do not change input dictionaries. '
    'Malformed XML raises `xml.etree.ElementTree.ParseError`.',
    'import xml.etree.ElementTree as ET\n\nXML = ' + repr(_XML) + '\n\n',
    'def get_tree(xml=XML):\n    pass\n\ndef get_movies(tree):\n    pass\n\n'
    'def get_movie_longest_runtime(movies):\n    pass\n',
    r'''import xml.etree.ElementTree as ET
import pytest
from xml_movies import get_tree, get_movies, get_movie_longest_runtime

def test_default_xml():
    root = get_tree()
    assert isinstance(root, ET.Element)
    movies = get_movies(root)
    assert [movie['title'] for movie in movies] == ['Memento', 'The Dark Knight', 'Interstellar']
    assert get_movie_longest_runtime(movies)['title'] == 'Interstellar'

def test_nested_movies_and_xml_entities():
    root = get_tree('<root><group><movie title="A &amp; B" runtime="9 min"/></group><movie title="C" runtime="10 min"/></root>')
    assert get_movies(root) == [{'title': 'A & B', 'runtime': '9 min'}, {'title': 'C', 'runtime': '10 min'}]

def test_empty_document():
    assert get_movies(get_tree('<root/>')) == []
    assert get_movie_longest_runtime([]) is None

def test_numeric_runtime_comparison():
    movies = [{'title': 'short', 'runtime': '99 min'}, {'title': 'long', 'runtime': '100 min'}]
    assert get_movie_longest_runtime(movies) == movies[1]

def test_unknown_and_zero_runtime():
    movies = [{'title': 'unknown', 'runtime': 'N/A'}, {'title': 'zero', 'runtime': '0 min'}]
    assert get_movie_longest_runtime(movies) == movies[1]
    assert get_movie_longest_runtime(movies[:1]) is None

def test_runtime_ties_and_no_input_change():
    movies = [{'title': 'first', 'runtime': '7 min'}, {'title': 'second', 'runtime': '7 min'}]
    before = [dict(movie) for movie in movies]
    assert get_movie_longest_runtime(movies) == movies[0]
    assert movies == before

def test_returned_attributes_are_independent():
    tree = get_tree('<root><movie title="Original" runtime="1 min"/></root>')
    get_movies(tree)[0]['title'] = 'Changed'
    assert tree.find('movie').attrib['title'] == 'Original'

def test_malformed_xml():
    with pytest.raises(ET.ParseError):
        get_tree('<root>')
''', [fault('compare runtime as text', 'key=lambda movie: int(movie["runtime"].split()[0])',
           'key=lambda movie: movie["runtime"]'),
      fault('skip nested movies', "tree.iter('movie')", "tree.findall('movie')"),
      fault('share XML attribute dictionaries', 'dict(node.attrib)', 'node.attrib')],
    'The premium template and tests are recreated. The small Nolan XML example is '
    'constructed locally. The public description does not specify return types or '
    'empty-input behavior; this version defines them above.',
    '''def get_tree(xml=XML):
    return ET.fromstring(xml)

def get_movies(tree):
    return [dict(node.attrib) for node in tree.iter('movie')]

def get_movie_longest_runtime(movies):
    known = [movie for movie in movies if movie['runtime'] != 'N/A']
    return max(known, key=lambda movie: int(movie["runtime"].split()[0]), default=None)
''')


_CARS = [dict(id=1, automaker='Dodge', model='Ram Van 1500', year=1999),
         dict(id=2, automaker='Chrysler', model='Town & Country', year=2002),
         dict(id=3, automaker='Porsche', model='Cayenne', year=2008),
         dict(id=4, automaker='Dodge', model='Charger', year=2008),
         dict(id=5, automaker='Dodge', model='Avenger', year=2008)]
add(2, 'car_data',
    'Implement `most_prolific_automaker(year, cars=CARS)` and '
    '`get_models(automaker, year, cars=CARS)`. `CARS` is decoded from the supplied '
    'JSON text. Each record has `id`, `automaker`, `model`, and integer `year`. '
    'Count matching records for the specified year. Return the automaker name with '
    'the largest count, or `None` if there are none. Ties keep first appearance order '
    'among matching records. Return matching model names in input order from '
    '`get_models`. Keep duplicate records. Match automaker names exactly. Return '
    'an empty list if no models match. Do not change the input.',
    'import json\nfrom collections import Counter\n\nCAR_JSON = ' + repr(json.dumps(_CARS)) +
    '\nCARS = json.loads(CAR_JSON)\n\n',
    'def most_prolific_automaker(year, cars=CARS):\n    pass\n\n'
    'def get_models(automaker, year, cars=CARS):\n    pass\n',
    r'''from car_data import CARS, most_prolific_automaker, get_models

def test_default_json_data():
    assert most_prolific_automaker(2008) == 'Dodge'
    assert get_models('Dodge', 2008) == ['Charger', 'Avenger']

def test_filter_year_before_counting():
    cars = [{'automaker': 'Old', 'model': 'A', 'year': 1999}, {'automaker': 'Old', 'model': 'B', 'year': 1999}, {'automaker': 'New', 'model': 'C', 'year': 2026}]
    assert most_prolific_automaker(2026, cars) == 'New'
    assert get_models('Old', 2026, cars) == []

def test_empty_and_missing_year():
    assert most_prolific_automaker(2000, []) is None
    assert get_models('Dodge', 2000, []) == []
    assert most_prolific_automaker(1800) is None

def test_first_seen_tie():
    cars = [{'automaker': 'Zed', 'model': 'Z', 'year': 1}, {'automaker': 'Alpha', 'model': 'A', 'year': 1}]
    assert most_prolific_automaker(1, cars) == 'Zed'

def test_exact_name_and_both_filters():
    assert get_models('dodge', 2008) == []
    assert get_models('Dodge', 1999) == ['Ram Van 1500']
    assert get_models('Porsche', 2008) == ['Cayenne']

def test_duplicate_models_and_order():
    cars = [{'automaker': 'X', 'model': model, 'year': 2020} for model in ['Z', 'A', 'Z']]
    assert get_models('X', 2020, cars) == ['Z', 'A', 'Z']
    cars += [{'automaker': 'Y', 'model': str(i), 'year': 2020} for i in range(2)]
    assert most_prolific_automaker(2020, cars) == 'X'

def test_inputs_unchanged_and_results_independent():
    before = [dict(car) for car in CARS]
    models = get_models('Dodge', 2008)
    models.append('extra')
    most_prolific_automaker(2008)
    assert CARS == before
    assert get_models('Dodge', 2008) == ['Charger', 'Avenger']
''', [fault('count every year', "if car['year'] == year", 'if True'),
      fault('ignore automaker filter', "car['automaker'] == automaker and ", '')],
    'The premium template and tests are recreated. A small local JSON fixture '
    'replaces the unavailable 1,000-record download. Argument order, tie rules, '
    'and empty-input results are defined for this version.',
    '''def most_prolific_automaker(year, cars=CARS):
    counts = Counter(car['automaker'] for car in cars if car['year'] == year)
    return counts.most_common(1)[0][0] if counts else None

def get_models(automaker, year, cars=CARS):
    return [car['model'] for car in cars
            if car['automaker'] == automaker and car['year'] == year]
''')


add(3, 'pickling',
    'Implement `deserialize(file=None)` and `serialize(file, data=None)`. Paths can '
    'be strings or pathlib Paths. Read and write files in binary mode using pickle. '
    '`deserialize(path)` returns the stored object unchanged, including namedtuple '
    'types. With no path, deserialize the trusted local `DEFAULT_PICKLE` bytes into '
    'a list of `Record(name, score)` values. `serialize` writes the supplied data '
    'and returns `None`. Only when `data is None`, call `deserialize()` for default '
    'data. Empty lists and other false values must be stored as supplied. Replace '
    'existing file content. Missing files raise `FileNotFoundError`; invalid '
    'pickle data raises `pickle.UnpicklingError` or `EOFError`. Only load trusted exercise data.',
    'import pickle\nfrom collections import namedtuple\n\n'
    'Record = namedtuple("Record", "name score")\n'
    'DEFAULT_PICKLE = pickle.dumps([Record("Ada", 9), Record("Bo", 7)])\n\n',
    'def deserialize(file=None):\n    pass\n\ndef serialize(file, data=None):\n    pass\n',
    r'''import pickle
import pytest
import pickling
from pickling import Record, deserialize, serialize

def test_default_namedtuples():
    result = deserialize()
    assert result == [Record('Ada', 9), Record('Bo', 7)]
    assert isinstance(result[0], Record)
    assert result[0].name == 'Ada'

def test_deserialize_supplied_path(tmp_path):
    path = tmp_path / 'records.pickle'
    path.write_bytes(pickle.dumps([Record('Zoë', 0)]))
    result = deserialize(path)
    assert result == [Record('Zoë', 0)]
    assert type(result[0]) is Record

def test_serialize_namedtuples_and_string_path(tmp_path):
    path = tmp_path / 'records.pickle'
    records = [Record('Lee', 3)]
    assert serialize(str(path), records) is None
    assert pickle.loads(path.read_bytes()) == records
    assert deserialize(str(path)) == records
    assert records == [Record('Lee', 3)]

def test_explicit_false_values(tmp_path):
    path = tmp_path / 'false.pickle'
    for value in [[], {}, (), False, 0, '']:
        serialize(path, value)
        result = pickle.loads(path.read_bytes())
        assert type(result) is type(value)
        assert result == value

def test_default_calls_deserialize(tmp_path, monkeypatch):
    calls = []
    def load_default():
        calls.append('called')
        return [Record('Mocked', 12)]
    monkeypatch.setattr(pickling, 'deserialize', load_default)
    path = tmp_path / 'default.pickle'
    serialize(path)
    assert calls == ['called']
    assert pickle.loads(path.read_bytes()) == [Record('Mocked', 12)]

def test_overwrite_old_data(tmp_path):
    path = tmp_path / 'overwrite.pickle'
    serialize(path, list(range(100)))
    serialize(path, [1])
    assert pickle.loads(path.read_bytes()) == [1]
    assert len(path.read_bytes()) < len(pickle.dumps(list(range(100))))

def test_missing_and_invalid_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        deserialize(tmp_path / 'missing.pickle')
    path = tmp_path / 'invalid.pickle'
    path.write_bytes(b'not a pickle')
    with pytest.raises(pickle.UnpicklingError):
        deserialize(path)
    path.write_bytes(b'')
    with pytest.raises(EOFError):
        deserialize(path)

def test_default_is_independent():
    first = deserialize()
    first.append(Record('Extra', 1))
    assert deserialize() == [Record('Ada', 9), Record('Bo', 7)]
''', [fault('replace false values with default', 'if data is None:', 'if not data:'),
      fault('append instead of overwrite', "open(file, 'wb')", "open(file, 'ab')")],
    'The premium template and tests are recreated. Trusted pickle bytes built '
    'from a small local namedtuple list replace the downloaded default file. '
    '`deserialize(None)` selects that local default; explicit paths still use files.',
    '''def deserialize(file=None):
    if file is None:
        return pickle.loads(DEFAULT_PICKLE)
    with open(file, 'rb') as source:
        return pickle.load(source)

def serialize(file, data=None):
    if data is None:
        data = deserialize()
    with open(file, 'wb') as destination:
        pickle.dump(data, destination)
''')


add(5, 'omdb_movies',
    'Implement `get_movie_data(files)`, `get_single_comedy(movies)`, '
    '`get_movie_most_nominations(movies)`, and `get_movie_longest_runtime(movies)`. '
    'Read each UTF-8 JSON file path into one movie dictionary and return a list '
    'in path order. Paths can be strings or pathlib Paths. The other functions '
    'return whole movie dictionaries, or `None` for no matching movie. '
    'Find the first movie with the exact `Comedy` token in comma-separated '
    '`Genre`. For nominations, sum integers directly before `nomination` or '
    '`nominations` in `Awards`. A missing such phrase, including `N/A`, counts '
    'as zero. Other award counts do not count. Runtime is `N min` or `N/A`; '
    'ignore `N/A` and compare numeric minutes. Numeric ties keep first input '
    'order. All movies contain `Title`, `Genre`, `Awards`, and `Runtime`. '
    'Return `None` for an empty movie list. Do not change the input.',
    'import json\nimport re\n\n',
    'def get_movie_data(files):\n    pass\n\ndef get_single_comedy(movies):\n    pass\n\n'
    'def get_movie_most_nominations(movies):\n    pass\n\n'
    'def get_movie_longest_runtime(movies):\n    pass\n',
    r'''import json
from omdb_movies import get_movie_data, get_single_comedy, get_movie_most_nominations, get_movie_longest_runtime

def movie(title, genre='Drama', awards='N/A', runtime='N/A'):
    return dict(Title=title, Genre=genre, Awards=awards, Runtime=runtime)

def test_read_json_files_in_order(tmp_path):
    data = [movie('Café', 'Drama, Comedy', '3 nominations.', '90 min'), movie('Long', runtime='120 min')]
    files = []
    for index, row in enumerate(data):
        path = tmp_path / f'movie{index}.json'
        path.write_text(json.dumps(row, ensure_ascii=False), encoding='utf-8')
        files.append(str(path) if index == 0 else path)
    assert get_movie_data(files) == data

def test_comedy_token_and_first_match():
    rows = [movie('Wrong', 'ComedyDrama'), movie('First', 'Drama, Comedy, Romance'), movie('Second', 'Comedy')]
    assert get_single_comedy(rows) == rows[1]
    assert get_single_comedy([movie('No comedy', 'comedy')]) is None

def test_numeric_nominations_and_other_awards():
    rows = [movie('Wins', awards='Won 2 Oscars. 100 wins & 9 nominations.'), movie('Nominations', awards='1 win & 12 nominations.')]
    assert get_movie_most_nominations(rows) == rows[1]

def test_singular_and_repeated_nomination_phrases():
    rows = [movie('One', awards='1 nomination.'), movie('Sum', awards='2 nominations. Another 3 nominations.'), movie('Four', awards='4 nominations.')]
    assert get_movie_most_nominations(rows) == rows[1]

def test_unknown_awards_and_first_tie():
    rows = [movie('First'), movie('Second', awards='7 wins.')]
    assert get_movie_most_nominations(rows) == rows[0]
    rows = [movie('First', awards='4 nominations.'), movie('Second', awards='4 nominations.')]
    assert get_movie_most_nominations(rows) == rows[0]

def test_numeric_runtime_and_unknown():
    rows = [movie('Unknown'), movie('Short', runtime='99 min'), movie('Long', runtime='100 min')]
    assert get_movie_longest_runtime(rows) == rows[2]
    assert get_movie_longest_runtime(rows[:1]) is None

def test_zero_runtime_tie_and_inputs_unchanged():
    rows = [movie('First', 'Comedy', runtime='0 min'), movie('Second', 'Comedy', runtime='0 min')]
    before = [dict(row) for row in rows]
    assert get_movie_longest_runtime(rows) == rows[0]
    get_single_comedy(rows)
    get_movie_most_nominations(rows)
    assert rows == before

def test_empty_inputs():
    assert get_movie_data([]) == []
    assert get_single_comedy([]) is None
    assert get_movie_most_nominations([]) is None
    assert get_movie_longest_runtime([]) is None
''', [fault('compare runtime as text', 'key=lambda movie: int(movie["Runtime"].split()[0])',
           'key=lambda movie: movie["Runtime"]'),
      fault('match partial comedy genre', "'Comedy' in [genre.strip() for genre in movie['Genre'].split(',')]",
           "'Comedy' in movie['Genre']"),
      fault('count wins as nominations', "r'(\\d+)\\s+nominations?\\b'", "r'(\\d+)\\s+wins?\\b'")],
    'The premium template and tests are recreated. Tests write small constructed '
    'OMDb-style JSON files locally. Award parsing and empty-input rules are '
    'explicit for this version; no external data download is required.',
    r'''def get_movie_data(files):
    movies = []
    for file in files:
        with open(file, encoding='utf-8') as source:
            movies.append(json.load(source))
    return movies

def get_single_comedy(movies):
    return next((movie for movie in movies
                 if 'Comedy' in [genre.strip() for genre in movie['Genre'].split(',')]), None)

def get_movie_most_nominations(movies):
    def nominations(movie):
        return sum(int(count) for count in re.findall(r'(\d+)\s+nominations?\b', movie['Awards']))
    return max(movies, key=nominations, default=None)

def get_movie_longest_runtime(movies):
    known = [movie for movie in movies if movie['Runtime'] != 'N/A']
    return max(known, key=lambda movie: int(movie["Runtime"].split()[0]), default=None)
''')


_TIMEZONES = ('name,timezone\nAda,Africa/Nairobi\nBo,Europe/Warsaw\n'
              'Cy,Africa/Nairobi\nDi,Pacific/Honolulu\nEli,Africa/Algiers\n')
add(7, 'timezone_chart',
    'Implement `create_bar_chart(data=DATA)`. Input is CSV text with a `timezone` '
    'header and optional other columns. Use CSV parsing to count each nonempty '
    'timezone after stripping surrounding whitespace. Ignore empty timezones '
    'and blank lines. Print one line per distinct timezone in ascending string '
    'order. The line is `timezone left-aligned | plus signs`, with one `+` per '
    'record. Use a timezone column width of max(20, longest timezone length), '
    'then one space, `|`, one space, and the bar. End each line with a newline. '
    'Print nothing for header-only or all-empty input. Return `None`. CSV data '
    'has a header even when it has no records.',
    'import csv\nimport io\nfrom collections import Counter\n\nDATA = ' + repr(_TIMEZONES) + '\n\n',
    'def create_bar_chart(data=DATA):\n    pass\n',
    r'''from timezone_chart import create_bar_chart

def test_default_chart(capsys):
    assert create_bar_chart() is None
    assert capsys.readouterr().out == 'Africa/Algiers       | +\nAfrica/Nairobi       | ++\nEurope/Warsaw        | +\nPacific/Honolulu     | +\n'

def test_sorted_and_counts(capsys):
    create_bar_chart('timezone\nZ\nA\nZ\nZ\n')
    assert capsys.readouterr().out == 'A                    | +\nZ                    | +++\n'

def test_header_only(capsys):
    assert create_bar_chart('timezone\n') is None
    assert capsys.readouterr().out == ''

def test_blank_lines_and_empty_timezones(capsys):
    create_bar_chart('name,timezone\nAda,\n\nBo,   \nCy, UTC \n')
    assert capsys.readouterr().out == 'UTC                  | +\n'

def test_quoted_other_columns(capsys):
    create_bar_chart('name,timezone\n"Last, First",Europe/Warsaw\n"Line\nBreak",Europe/Warsaw\n')
    assert capsys.readouterr().out == 'Europe/Warsaw        | ++\n'

def test_long_timezone_expands_column(capsys):
    create_bar_chart('timezone\nAmerica/Argentina/Buenos_Aires\nUTC\n')
    assert capsys.readouterr().out == ('America/Argentina/Buenos_Aires | +\nUTC                            | +\n')

def test_all_empty_and_separate_calls(capsys):
    create_bar_chart('name,timezone\nA,\nB,\n')
    assert capsys.readouterr().out == ''
    create_bar_chart('timezone\nUTC\n')
    assert capsys.readouterr().out == 'UTC                  | +\n'
    create_bar_chart('timezone\nUTC\n')
    assert capsys.readouterr().out == 'UTC                  | +\n'
''', [fault('use appearance order', 'for timezone in sorted(counts):', 'for timezone in counts:'),
      fault('count each timezone once', 'counts[timezone] += 1', 'counts[timezone] = 1'),
      fault('retain empty timezone', 'if timezone:', 'if True:')],
    'The premium template and tests are recreated. Local CSV text replaces the '
    'requests download. This version supplies the function name, header, column '
    'width, sorting, and empty-record rules because the public description '
    'does not expose the original template or full expected chart.',
    '''def create_bar_chart(data=DATA):
    counts = Counter()
    for row in csv.DictReader(io.StringIO(data)):
        timezone = row['timezone'].strip()
        if timezone:
            counts[timezone] += 1
    width = max(20, max(map(len, counts), default=0))
    for timezone in sorted(counts):
        print(f'{timezone:<{width}} | {"+" * counts[timezone]}')
''')
