"""Eleven exercise specifications. Premium exercises are explicit recreations."""
import json
from pathlib import Path

PAGES = json.loads((Path(__file__).parent / 'source-pages.json').read_text())
SPECS = []


def add(number, module, contract, header, template, reference, tests, mutations, **extra):
    page = PAGES[number - 1]
    SPECS.append(dict(number=number, title=page['title'], module=module, contract=contract,
                      template=header + template, reference=header + reference,
                      tests=tests, mutations=mutations, **extra))


def fault(name, old, new):
    return dict(name=name, old=old, new=new)


# 1: Original free template and tests.
add(1, 'belts',
    'Implement `get_total_points(belts=ninja_belts)`. Each value is a `BeltStats(score, ninjas)` '
    'namedtuple. Return the sum of score multiplied by the number of ninjas. Scores and counts '
    'are nonnegative integers. An empty dictionary returns 0. Do not change the input.',
    '', PAGES[0]['template'],
    PAGES[0]['template'].rsplit('    pass', 1)[0] + '    return sum(b.score * b.ninjas for b in belts.values())\n',
    PAGES[0]['tests'] + '''

# Added boundary tests.
def test_default_belts():
    assert get_total_points() == 2675

def test_empty_belts():
    assert get_total_points({}) == 0

def test_zero_values():
    assert get_total_points({'a': BeltStats(0, 8), 'b': BeltStats(100, 0)}) == 0

def test_unfamiliar_belts_and_unchanged_input():
    belts = {'new': BeltStats(7, 9), 'other': BeltStats(3, 4)}
    before = dict(belts)
    assert get_total_points(belts) == 75
    assert belts == before
''', [fault('ignore belt owners', 'b.score * b.ninjas', 'b.score')], original=True)

# 2: A bounded deque must remain bounded after new appends.
add(2, 'myqueue',
    'Implement `my_queue(n=5)`. Return an empty `collections.deque` with maximum length `n`. '
    '`n` is a nonnegative integer. Appends keep the newest `n` items in insertion order. '
    'A length of 0 discards every appended item.',
    'from collections import deque\n\n',
    'def my_queue(n=5):\n    pass\n',
    'def my_queue(n=5):\n    return deque(maxlen=n)\n',
    r'''from collections import deque
import pytest
from myqueue import my_queue

def test_default():
    q = my_queue()
    assert isinstance(q, deque) and q.maxlen == 5 and list(q) == []

@pytest.mark.parametrize('n', [0, 1, 2, 5, 20])
def test_bounded_appends(n):
    q = my_queue(n)
    for i in range(12):
        q.append(i)
    assert list(q) == (list(range(12))[-n:] if n else [])
    assert q.maxlen == n

def test_queue_remains_bounded():
    q = my_queue(2)
    q.extend(['first', 'second', 'third'])
    assert q.popleft() == 'second'
    q.append('fourth')
    q.append('fifth')
    assert list(q) == ['fourth', 'fifth']

def test_independent_queues():
    a, b = my_queue(1), my_queue(1)
    a.append('a')
    assert list(b) == []
''', [fault('unbounded queue', 'deque(maxlen=n)', 'deque()')])

# 3: CSV input from the public description; the function uses any valid CSV.
_GROUP_DATA = 'last_name,first_name,country_code\nWatsham,Husain,ID\nHarrold,Alphonso,BR\nApdell,Margo,CN\nTomblings,Deerdre,RU\nWasielewski,Sula,ID\n'
add(3, 'countries',
    'Implement `group_names_by_country(data=data)`. The input is CSV text with headers '
    '`last_name,first_name,country_code`. Return a `defaultdict(list)` mapping each country '
    'to full names in `first_name last_name` form. Quoted fields are valid. Ignore blank lines. '
    'Keep duplicate people. Country and name order does not matter. Header-only input returns '
    'an empty defaultdict. All nonblank records have the three required fields.',
    'import csv\nimport io\nfrom collections import defaultdict\n\ndata = ' + repr(_GROUP_DATA) + '\n\n',
    'def group_names_by_country(data=data):\n    pass\n',
    '''def group_names_by_country(data=data):
    groups = defaultdict(list)
    for row in csv.DictReader(io.StringIO(data)):
        groups[row['country_code']].append(row['first_name'] + ' ' + row['last_name'])
    return groups
''',
    r'''from collections import defaultdict
from countries import group_names_by_country

def test_example():
    groups = group_names_by_country()
    assert sorted(groups['ID']) == ['Husain Watsham', 'Sula Wasielewski']
    assert groups['BR'] == ['Alphonso Harrold']
    assert groups['CN'] == ['Margo Apdell']

def test_default_factory():
    groups = group_names_by_country()
    assert isinstance(groups, defaultdict) and groups.default_factory is list
    assert groups['ZZ'] == []

def test_header_only():
    assert dict(group_names_by_country('last_name,first_name,country_code\n')) == {}

def test_quoted_comma_and_blank_lines():
    text = 'last_name,first_name,country_code\n"Smith, Jr.",Ada,US\n\nLee,Bo,KR\n'
    result = group_names_by_country(text)
    assert result['US'] == ['Ada Smith, Jr.'] and result['KR'] == ['Bo Lee']

def test_duplicates_and_custom_country():
    text = 'last_name,first_name,country_code\nDoe,Jo,XX\nDoe,Jo,XX\n'
    assert group_names_by_country(text)['XX'] == ['Jo Doe', 'Jo Doe']

def test_instances_are_independent():
    first = group_names_by_country()
    first['ID'].append('extra')
    assert 'extra' not in group_names_by_country()['ID']
''', [fault('reverse full name', "row['first_name'] + ' ' + row['last_name']", "row['last_name'] + ' ' + row['first_name']")])

# 4: Deterministic, constructed RSS data instead of a network request.
_TAGS = '<rss><channel><item><category>Python</category><category>learning</category></item><item><category>Python</category><category>Flask</category><category>learning</category><category>Python</category></item></channel></rss>'
add(4, 'tags',
    'Implement `get_top_tags(xml=XML, n=10)`. Count the text of each RSS `<category>` element '
    'with `Counter`. Return `Counter.most_common(n)`: a list of `(tag, count)` tuples. '
    'Strip surrounding whitespace. Ignore empty categories. Keep case. Ties keep the first '
    'appearance order. `n` is a nonnegative integer. The XML is well formed and has no namespaces.',
    'from collections import Counter\nimport xml.etree.ElementTree as ET\n\nXML = ' + repr(_TAGS) + '\n\n',
    'def get_top_tags(xml=XML, n=10):\n    pass\n',
    '''def get_top_tags(xml=XML, n=10):
    counts = Counter()
    for node in ET.fromstring(xml).iter('category'):
        tag = (node.text or '').strip()
        if tag:
            counts[tag] += 1
    return counts.most_common(n)
''',
    '''import pytest
from tags import get_top_tags

def test_default_feed():
    assert get_top_tags() == [('Python', 3), ('learning', 2), ('Flask', 1)]

def test_limit():
    assert get_top_tags(n=1) == [('Python', 3)]

def test_default_limit_is_ten():
    xml = '<rss>' + ''.join(f'<category>tag{i}</category>' for i in range(12)) + '</rss>'
    assert get_top_tags(xml) == [(f'tag{i}', 1) for i in range(10)]

def test_empty_and_zero():
    assert get_top_tags('<rss/>') == []
    assert get_top_tags(n=0) == []

def test_strip_entities_empty_and_tie_order():
    xml = '<rss><category> z </category><category>a &amp; b</category><category/><category> </category></rss>'
    assert get_top_tags(xml) == [('z', 1), ('a & b', 1)]

def test_case_and_repeat():
    xml = '<rss><category>Python</category><category>python</category><category>python</category></rss>'
    assert get_top_tags(xml) == [('python', 2), ('Python', 1)]
''', [fault('count each tag only once', 'counts[tag] += 1', 'counts[tag] = 1')],
    notes='The supplied RSS example is constructed for this offline version.')

# 5: One path means one challenge contribution; core-team accounts are excluded.
_FILES = ('22/wonderfulboyx', '25/bbelderbos', '25/clamytoe', '21/wonderfulboyx',
          '25/santiagobenitez', '23/santiagobenitez', '07/santiagobenitez')
add(5, 'pcc_stats',
    'Implement `gen_files(tempfile)` and `diehard_pybites(files=FILES)`. The first function '
    'is a generator that reads a local UTF-8 file, strips each line, skips blank lines, and '
    'yields `NN/user` paths. The listing contains only valid two-digit challenge paths. '
    'The second function accepts any iterable of paths. Exclude `bbelderbos`, `juliansequeira`, '
    'and `pybites` from both counts. Each remaining path counts once. Return '
    '`Stats(user, challenge)` where challenge is `(challenge_id, count)`. Ties keep first '
    'appearance order. With no eligible paths, return `Stats(None, (None, 0))`.',
    'from collections import Counter, namedtuple\n\nStats = namedtuple("Stats", "user challenge")\n'
    'EXCLUDED = {"bbelderbos", "juliansequeira", "pybites"}\nFILES = ' + repr(_FILES) + '\n\n',
    'def gen_files(tempfile):\n    pass\n\ndef diehard_pybites(files=FILES):\n    pass\n',
    '''def gen_files(tempfile):
    with open(tempfile, encoding='utf-8') as source:
        for line in source:
            if line.strip():
                yield line.strip()

def diehard_pybites(files=FILES):
    users, challenges = Counter(), Counter()
    for path in files:
        challenge, user = path.strip().split('/')
        if user in EXCLUDED:
            continue
        users[user] += 1
        challenges[challenge] += 1
    return Stats(users.most_common(1)[0][0] if users else None,
                 challenges.most_common(1)[0] if challenges else (None, 0))
''',
    r'''import inspect
from pcc_stats import gen_files, diehard_pybites, Stats

def test_public_example():
    assert diehard_pybites() == Stats('santiagobenitez', ('25', 2))

def test_generator_and_local_file(tmp_path):
    path = tmp_path / 'paths.txt'
    path.write_text(' 01/ana  \n\n02/bob\n', encoding='utf-8')
    assert inspect.isgeneratorfunction(gen_files)
    result = gen_files(path)
    assert inspect.isgenerator(result)
    assert list(result) == ['01/ana', '02/bob']

def test_exclude_team_from_both_counts():
    paths = ['99/bbelderbos', '99/juliansequeira', '99/pybites', '02/ana']
    assert diehard_pybites(paths) == Stats('ana', ('02', 1))

def test_first_seen_ties():
    assert diehard_pybites(['09/zoe', '01/ana']) == Stats('zoe', ('09', 1))

def test_single_pass_iterable():
    assert diehard_pybites(iter(['01/ana', '02/ana', '02/bob'])) == Stats('ana', ('02', 2))

def test_no_eligible_paths():
    assert diehard_pybites([]) == Stats(None, (None, 0))
    assert diehard_pybites(['01/pybites']) == Stats(None, (None, 0))
''', [fault('include core team', 'if user in EXCLUDED:', 'if False:')])

# 6: Original free template and tests, including the blog's datetime.
add(6, 'dict_convert',
    'Implement `dict2nt(dict_)` and `nt2json(nt)`. Convert a dictionary to a namedtuple with '
    'matching field names, field order, and values. Keys are valid unique namedtuple field names: '
    'Python identifiers that do not start with an underscore and are not keywords. '
    'An empty dictionary is valid. Return JSON text for the namedtuple fields. Convert values '
    'that JSON cannot encode directly, such as datetime, with `str`. Do not change the input.',
    '', PAGES[5]['template'],
    PAGES[5]['template'].split('# define namedtuple here')[0] + '''
def dict2nt(dict_):
    return namedtuple('Record', dict_)(**dict_)

def nt2json(nt):
    return json.dumps(nt._asdict(), default=str)
''',
    PAGES[5]['tests'] + '''

# Added boundary tests.
def test_custom_fields_and_order():
    data = {'z': 3, 'a': ['x']}
    record = dict2nt(data)
    assert record._fields == ('z', 'a') and record.z == 3 and record.a == ['x']
    assert data == {'z': 3, 'a': ['x']}

def test_empty_record():
    record = dict2nt({})
    assert record._fields == () and json.loads(nt2json(record)) == {}

def test_json_types():
    data = {'active': True, 'missing': None, 'nested': {'x': [1, 2]}}
    assert json.loads(nt2json(dict2nt(data))) == data

def test_distinct_schemas():
    one, two = dict2nt({'x': 1}), dict2nt({'y': 2})
    assert one.x == 1 and two.y == 2 and not hasattr(two, 'x')
''', [fault('omit JSON datetime conversion', 'default=str', 'default=lambda value: None')], original=True)

# 7: Constructed text avoids a network dependency or a book-length fixture.
add(7, 'common_word',
    'Implement `get_most_common_word(text=TEXT, stopwords=STOPWORDS)`. Lowercase the text. '
    'Split on whitespace. Remove non-alphanumeric characters from each token, so `can\'t` '
    'becomes `cant`. Ignore empty tokens and stopwords, matched without case. Count digits '
    'as alphanumeric. Return `(word, frequency)`. Ties keep first appearance order. '
    'Return `(None, 0)` if no words remain. Do not change the stopword collection.',
    'from collections import Counter\n\nTEXT = "The wizard met the owl. The wizard waved."\n'
    'STOPWORDS = {"the", "a", "and"}\n\n',
    'def get_most_common_word(text=TEXT, stopwords=STOPWORDS):\n    pass\n',
    '''def get_most_common_word(text=TEXT, stopwords=STOPWORDS):
    ignored = {word.lower() for word in stopwords}
    counts = Counter()
    for token in text.lower().split():
        word = ''.join(char for char in token if char.isalnum())
        if word and word not in ignored:
            counts[word] += 1
    return counts.most_common(1)[0] if counts else (None, 0)
''',
    '''from common_word import get_most_common_word

def test_default():
    assert get_most_common_word() == ('wizard', 2)

def test_lowercase_and_punctuation():
    assert get_most_common_word('Owl, OWL! owl?', []) == ('owl', 3)

def test_stopwords_and_digits():
    assert get_most_common_word('THE the 42 42 owl', ['The']) == ('42', 2)

def test_empty_and_all_excluded():
    assert get_most_common_word('', []) == (None, 0)
    assert get_most_common_word('!!! ---', []) == (None, 0)
    assert get_most_common_word('the THE', ['the']) == (None, 0)

def test_first_appearance_breaks_tie():
    assert get_most_common_word('zebra apple', []) == ('zebra', 1)

def test_internal_punctuation_is_removed():
    assert get_most_common_word("can't cant can-t", []) == ('cant', 3)

def test_stopwords_not_changed():
    words = ['THE']
    get_most_common_word('the owl', words)
    assert words == ['THE']
''', [fault('keep original case', 'text.lower().split()', 'text.split()')])

from cojudge.collections_path.fixtures import MOVIE_HEADER, HOLIDAY_HEADER, SOUP

# 8: Free tests preserved. The original CSV is supplied as a compressed local fixture.
add(8, 'directors',
    'Implement `get_movies_by_director()`, `calc_mean_score(movies)`, and '
    '`get_average_scores(directors)`. `MOVIE_DATA` is a supplied local CSV path. Read it with '
    '`csv.DictReader`. Ignore rows missing director_name, movie_title, title_year, or imdb_score. '
    'Convert year to int and score to float. Include years >= MIN_YEAR (1960). Strip title '
    'whitespace. Return `defaultdict(list)` values containing `Movie(title, year, score)` records. '
    '`calc_mean_score` accepts a nonempty list of Movie records and rounds the mean to one '
    'decimal place. `get_average_scores` returns `(director, mean)` tuples for directors with '
    'at least MIN_MOVIES (4) films, highest rounded score first. Ties keep director insertion '
    'order. Present numeric CSV values are valid. An empty CSV produces an empty defaultdict.',
    MOVIE_HEADER,
    '''def get_movies_by_director():
    pass

def calc_mean_score(movies):
    pass

def get_average_scores(directors):
    pass
''',
    '''def get_movies_by_director():
    directors = defaultdict(list)
    with open(MOVIE_DATA, encoding='utf-8', newline='') as source:
        for row in csv.DictReader(source):
            if not all(row.get(key, '').strip() for key in ('director_name', 'movie_title', 'title_year', 'imdb_score')):
                continue
            year = int(row['title_year'])
            if year >= MIN_YEAR:
                directors[row['director_name']].append(Movie(row['movie_title'].strip(), year, float(row['imdb_score'])))
    return directors

def calc_mean_score(movies):
    return round(sum(movie.score for movie in movies) / len(movies), 1)

def get_average_scores(directors):
    scores = [(name, calc_mean_score(movies)) for name, movies in directors.items() if len(movies) >= MIN_MOVIES]
    return sorted(scores, key=lambda pair: pair[1], reverse=True)
''',
    PAGES[7]['tests'] + r'''

# Added boundary tests use their own local CSV.
def test_year_boundary_missing_fields_and_quotes(tmp_path, monkeypatch):
    import directors
    path = tmp_path / 'movies.csv'
    path.write_text('director_name,movie_title,title_year,imdb_score\n'
                    'A,Old,1959,9.9\nA," Title, One ",1960,7.1\n'
                    ',No director,2020,9\nA,,2020,9\nA,No year,,9\nA,No score,2020,\n')
    monkeypatch.setattr(directors, 'MOVIE_DATA', str(path))
    assert get_movies_by_director() == {'A': [Movie('Title, One', 1960, 7.1)]}

def test_empty_dataset(tmp_path, monkeypatch):
    import directors
    path = tmp_path / 'empty.csv'
    path.write_text('director_name,movie_title,title_year,imdb_score\n')
    monkeypatch.setattr(directors, 'MOVIE_DATA', str(path))
    assert dict(get_movies_by_director()) == {}

def test_minimum_count_and_stable_ties():
    directors = {'Z': [Movie('z', 2000, 8.0)] * 4,
                 'A': [Movie('a', 2001, 8.0)] * 5,
                 'Too few': [Movie('x', 2002, 10.0)] * 3}
    assert get_average_scores(directors) == [('Z', 8.0), ('A', 8.0)]
    assert get_average_scores({}) == []

def test_mean_rounding():
    assert calc_mean_score([Movie('a', 2000, 7.0), Movie('b', 2000, 7.3)]) == 7.2
''', [fault('drop year boundary', 'year >= MIN_YEAR', 'year > MIN_YEAR'),
      fault('exclude exact minimum count', 'len(movies) >= MIN_MOVIES', 'len(movies) > MIN_MOVIES')],
    adapted='The original free tests are retained, with added boundary tests. The template replaces '
            'the network download with a compressed copy of the original movie CSV. Only the four '
            'columns used in this exercise are retained. The public function signatures are unchanged.')

# 9: Standard CSV parsing handles commas, quotes, and multiline dialogue.
_SOUTH = 'Season,Episode,Character,Line\n1,1,Cartman,Hello there\n1,1,Stan,Hey\n1,2,Cartman,One two three\n1,1,Cartman,Again\n'
add(9, 'southpark',
    'Implement `get_num_words_spoken_by_character_per_episode(data=DATA)`. The input is CSV text '
    'with `Season,Episode,Character,Line` headers. Return a `defaultdict(Counter)` mapping each '
    'character to word counts per episode. Episode keys stay strings. Count words by splitting '
    'dialogue on whitespace. Add counts across rows. Quoted commas, quotes, and newlines are '
    'valid CSV. Include a zero count for an empty dialogue. Header-only input returns an empty '
    'defaultdict. All records belong to one season and contain the four fields.',
    'import csv\nimport io\nfrom collections import Counter, defaultdict\n\nDATA = ' + repr(_SOUTH) + '\n\n',
    'def get_num_words_spoken_by_character_per_episode(data=DATA):\n    pass\n',
    '''def get_num_words_spoken_by_character_per_episode(data=DATA):
    counts = defaultdict(Counter)
    for row in csv.DictReader(io.StringIO(data)):
        counts[row['Character']][row['Episode']] += len(row['Line'].split())
    return counts
''',
    r'''from collections import Counter, defaultdict
from southpark import get_num_words_spoken_by_character_per_episode as count

def test_default_data():
    result = count()
    assert result['Cartman'] == Counter({'1': 3, '2': 3})
    assert result['Stan'] == Counter({'1': 1})

def test_nested_types():
    result = count()
    assert isinstance(result, defaultdict) and result.default_factory is Counter
    assert isinstance(result['new'], Counter)
    assert result['new']['99'] == 0

def test_quoted_and_multiline_dialogue():
    text = 'Season,Episode,Character,Line\n2,03,A,"hello, dear friend\nnext line"\n'
    assert count(text)['A'] == Counter({'03': 5})

def test_accumulate_multiple_lines():
    text = 'Season,Episode,Character,Line\n1,1,A,one two\n1,1,A,three four five\n'
    assert count(text)['A']['1'] == 5

def test_empty_line_and_empty_dataset():
    assert dict(count('Season,Episode,Character,Line\n')) == {}
    assert count('Season,Episode,Character,Line\n1,1,A,\n')['A'] == Counter({'1': 0})

def test_quoted_character_and_whitespace():
    text = 'Season,Episode,Character,Line\n1,1,"Agent, One","one   two\tthree"\n'
    assert count(text)['Agent, One']['1'] == 3
''', [fault('overwrite earlier dialogue counts', "counts[row['Character']][row['Episode']] +=", "counts[row['Character']][row['Episode']] =")])

# 10: Original holiday table; a supplied standard-library BeautifulSoup subset.
add(10, 'holidays',
    'Implement `get_us_bank_holidays(html=HTML)`. Use the supplied BeautifulSoup interface '
    'to find the first table with CSS class `list-table`. For each data row, read the '
    '`datetime` attribute of its `time` element (YYYY-MM-DD) and the fourth `td` cell as the '
    'holiday name. Return a new `defaultdict(list)` mapping two-digit month strings to holiday '
    'names in document order. Strip name whitespace. Include every listed holiday, including '
    'regional and observance rows. Skip header rows and rows with fewer than four cells or no '
    'time element. Return an empty defaultdict when the table is absent. The supplied HTML '
    'is well formed, has no nested tables, and all present dates use YYYY-MM-DD.',
    HOLIDAY_HEADER + SOUP + '\n',
    'def get_us_bank_holidays(html=HTML):\n    pass\n',
    '''def get_us_bank_holidays(html=HTML):
    holidays = defaultdict(list)
    table = BeautifulSoup(html, 'html.parser').find('table', class_='list-table')
    if table is None:
        return holidays
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        time = row.find('time')
        if len(cells) >= 4 and time is not None:
            month = time.get('datetime')[5:7]
            holidays[month].append(cells[3].get_text(strip=True))
    return holidays
''',
    r'''from collections import defaultdict
from holidays import get_us_bank_holidays

def test_original_table():
    result = get_us_bank_holidays()
    assert result == {'01': ["New Year's Day", 'Martin Luther King Jr. Day'],
                      '02': ["Presidents' Day"], '04': ['Emancipation Day'],
                      '05': ["Mother's Day", 'Memorial Day'], '06': ["Father's Day"],
                      '07': ['Independence Day'], '09': ['Labor Day'], '10': ['Columbus Day'],
                      '11': ['Veterans Day', 'Thanksgiving', 'Day after Thanksgiving'],
                      '12': ['Christmas Day']}

def test_missing_table_and_default_factory():
    result = get_us_bank_holidays('<table><tr><td>unrelated</td></tr></table>')
    assert isinstance(result, defaultdict) and result.default_factory is list
    assert dict(result) == {} and result['03'] == []

def test_select_class_and_strip_nested_text():
    html = '<table><tr><td>ignore</td></tr></table><table class="other list-table wide">'
    html += '<tr><td>Day</td><td><time datetime="2024-03-01">March</time></td><td>2024</td><td> <a>Spring &amp; Sun</a> </td></tr></table>'
    assert get_us_bank_holidays(html) == {'03': ['Spring & Sun']}

def test_skip_header_missing_time_and_short_rows():
    html = '<table class="list-table"><tr><th>Header</th></tr>'
    html += '<tr><td>A</td><td>B</td><td>C</td><td>D</td></tr>'
    html += '<tr><td><time datetime="2024-01-01">Date</time></td></tr></table>'
    assert dict(get_us_bank_holidays(html)) == {}

def test_input_order_and_fresh_result():
    first = get_us_bank_holidays()
    first['01'].append('extra')
    assert get_us_bank_holidays()['01'] == ["New Year's Day", 'Martin Luther King Jr. Day']
''', [fault('read day instead of month', "time.get('datetime')[5:7]", "time.get('datetime')[8:10]"),
      fault('keep surrounding spaces', 'get_text(strip=True)', 'get_text(strip=False)')],
    adapted='This premium exercise uses recreated tests and the original cached holiday table. '
            'The judge has no BeautifulSoup package. The template supplies a small standard-library '
            'adapter named BeautifulSoup. It supports find/find_all(name, class_=...), get, '
            'get_text(strip=...), and text. It is limited to the well-formed HTML in this version.')

# 11: Whole words and aliases, with physical line numbers and no duplicate lines.
add(11, 'story_index',
    'Implement `make_character_index(text, characters)`. `text` is a multiline string. Each '
    'character is a nonempty string or nonempty tuple of aliases. The first alias is the output '
    'key. Match all aliases without case, with whole-word boundaries. Punctuation around a name '
    'is allowed. A name inside a longer word does not match. Treat alias text literally. Return '
    'a dictionary of characters that appear, with sorted unique 1-based physical line numbers. '
    'Blank lines count. One line appears only once per character, even if several aliases match. '
    'Return an empty dictionary for empty text or characters. Canonical keys are unique. Alias '
    'endpoints are word characters. Keep input collections unchanged.',
    'import re\nfrom collections import defaultdict\n\n',
    'def make_character_index(text, characters):\n    pass\n',
    r'''def make_character_index(text, characters):
    index = defaultdict(list)
    for character in characters:
        aliases = (character,) if isinstance(character, str) else character
        pattern = re.compile(r'\b(?:' + '|'.join(re.escape(alias) for alias in aliases) + r')\b', re.I)
        for number, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                index[aliases[0]].append(number)
    return dict(index)
''',
    r'''from story_index import make_character_index

def test_case_and_line_numbers():
    text = 'Red met the wolf.\nThe WOLF spoke.\nRed ran home.'
    assert make_character_index(text, ['Red', 'wolf']) == {'Red': [1, 3], 'wolf': [1, 2]}

def test_synonyms_use_first_alias_once_per_line():
    text = 'Grandma met Granny and Grandmother.\nGranny waved.'
    assert make_character_index(text, [('Grandmother', 'Grandma', 'Granny')]) == {'Grandmother': [1, 2]}

def test_whole_word_matching():
    assert make_character_index('Wolfgang and werewolf\nwolf!', ['wolf']) == {'wolf': [2]}

def test_blank_lines_count():
    assert make_character_index('\n\nRed\n\nred', ['Red']) == {'Red': [3, 5]}

def test_missing_and_empty():
    assert make_character_index('', ['Red']) == {}
    assert make_character_index('Red', []) == {}
    assert make_character_index('Red', ['wolf']) == {}

def test_literal_names_and_phrases():
    text = 'A.B and Little Red Riding Hood\nAxB and Hood'
    assert make_character_index(text, ['A.B', 'Little Red Riding Hood']) == {
        'A.B': [1], 'Little Red Riding Hood': [1]}

def test_inputs_unchanged():
    names = [('Grandmother', 'Granny'), 'wolf']
    before = list(names)
    make_character_index('Granny and wolf', names)
    assert names == before
''', [fault('zero based line numbers', 'enumerate(text.splitlines(), 1)', 'enumerate(text.splitlines(), 0)'),
      fault('case sensitive names', ', re.I)', ', 0)')])
