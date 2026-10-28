"""Data Formats exercises 9–13, recreated from public descriptions."""
import json
from pathlib import Path

PAGES = {page['n']: page for page in json.loads(
    (Path(__file__).parent / 'source-pages.json').read_text())}
SPECS = []


def add(number, module, contract, header, template, reference, tests, mutations, **extra):
    SPECS.append(dict(number=number, title=PAGES[number]['title'], module=module,
                      contract=contract, template=header + template,
                      reference=header + reference, tests=tests,
                      mutations=mutations, **extra))


def fault(name, old, new):
    return dict(name=name, old=old, new=new)


IP_HEADER = '''IPINFO_URL = 'https://ipinfo.io/{ip}/json'


class LocalResponse:
    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return dict(self.payload)


class LocalClient:
    """A requests-compatible client. It uses local records and makes no network calls."""
    def __init__(self):
        self.records = {'8.8.8.8': {'country': 'US', 'city': 'Mountain View'},
                        '1.1.1.1': {'country': 'AU', 'city': 'Sydney'},
                        '2001:db8::1': {'country': 'MX'}}

    def get(self, url):
        prefix, suffix = 'https://ipinfo.io/', '/json'
        if not url.startswith(prefix) or not url.endswith(suffix):
            raise ValueError('Unexpected local URL')
        ip = url[len(prefix):-len(suffix)]
        return LocalResponse(self.records[ip])


requests = LocalClient()


'''
add(9, 'ip_country',
    'Implement `get_country(ip="8.8.8.8", client=None)`. Format `IPINFO_URL` with the '
    'given IP address. Call `client.get(url)`, call `json()` on its response, and return '
    'the `country` field. When `client` is None, use the supplied `requests` object. '
    'The field contains a two-character country code. Preserve its case. IP addresses '
    'are strings; IPv4 and IPv6 are accepted without validation. Make exactly one GET '
    'call per invocation. Missing country fields raise KeyError. Client and JSON errors '
    'pass through unchanged. Do not modify the response data. No network call is needed: '
    '`requests` is a local requests-compatible client with three sample records. Tests '
    'also inject clients with other records.',
    IP_HEADER,
    'def get_country(ip="8.8.8.8", client=None):\n    pass\n',
    '''def get_country(ip="8.8.8.8", client=None):
    if client is None:
        client = requests
    response = client.get(IPINFO_URL.format(ip=ip))
    return response.json()['country']
''',
    '''import pytest
import ip_country
from ip_country import get_country


class Client:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []
        self.json_calls = 0

    def get(self, url):
        self.calls.append(url)
        return self

    def json(self):
        self.json_calls += 1
        return self.payload


def test_default_local_country():
    assert get_country() == 'US'
    assert get_country('1.1.1.1') == 'AU'


def test_injected_client_and_exact_url():
    client = Client({'country': 'NZ', 'city': 'Wellington'})
    assert get_country('203.0.113.7', client) == 'NZ'
    assert client.calls == ['https://ipinfo.io/203.0.113.7/json']
    assert client.json_calls == 1


def test_ipv6_address():
    client = Client({'country': 'DE'})
    assert get_country('2001:db8::123', client) == 'DE'
    assert client.calls == ['https://ipinfo.io/2001:db8::123/json']
    assert get_country('2001:db8::1') == 'MX'


def test_preserve_code_and_response():
    payload = {'country': 'gb', 'region': 'England'}
    client = Client(payload)
    assert get_country('192.0.2.1', client) == 'gb'
    assert payload == {'country': 'gb', 'region': 'England'}


def test_missing_country():
    with pytest.raises(KeyError):
        get_country('192.0.2.1', Client({'city': 'Unknown'}))


def test_client_errors_propagate():
    class Broken:
        def get(self, url):
            raise RuntimeError('local transport failure')
    with pytest.raises(RuntimeError, match='local transport failure'):
        get_country('192.0.2.1', Broken())


def test_json_errors_propagate():
    class Broken(Client):
        def json(self):
            raise ValueError('invalid JSON')
    with pytest.raises(ValueError, match='invalid JSON'):
        get_country('192.0.2.1', Broken({}))


def test_default_client_can_be_replaced(monkeypatch):
    client = Client({'country': 'JP'})
    monkeypatch.setattr(ip_country, 'requests', client)
    assert get_country('198.51.100.4') == 'JP'
    assert client.calls == ['https://ipinfo.io/198.51.100.4/json']
''',
    [fault('ignore requested address', 'IPINFO_URL.format(ip=ip)', 'IPINFO_URL.format(ip="8.8.8.8")'),
     fault('normalize country case', "response.json()['country']", "response.json()['country'].upper()"),
     fault('hide a missing country', "response.json()['country']", "response.json().get('country')")],
    notes='The public exercise uses requests. This version supplies a local object with the '
          'same get()/response.json() interface. An optional client parameter supports injection. '
          'The original premium template and tests are unavailable; these interfaces and tests are recreated.')


STOCKS = [
    {'id': 1, 'name': 'Harbor Trust', 'symbol': 'HBR', 'industry': 'REIT',
     'sector': 'Consumer Services', 'market': 'NYSE', 'cap': '$600.57M'},
    {'id': 2, 'name': 'Medical Tools', 'symbol': 'MED', 'industry': 'Instruments',
     'sector': 'Health Care', 'market': 'NASDAQ', 'cap': '$21.78M'},
    {'id': 3, 'name': 'Cloud Works', 'symbol': 'CLD', 'industry': 'Software',
     'sector': 'Technology', 'market': 'NASDAQ', 'cap': '$2.1B'},
    {'id': 4, 'name': 'Care Group', 'symbol': 'CARE', 'industry': 'Services',
     'sector': 'Health Care', 'market': 'NYSE', 'cap': 'n/a'},
    {'id': 5, 'name': 'Chip Works', 'symbol': 'CHP', 'industry': 'Semiconductors',
                'sector': 'Technology', 'market': 'NASDAQ', 'cap': '$950M'},
]
STOCK_HEADER = ('import json\nfrom collections import Counter\nfrom fractions import Fraction\n\n'
                f'STOCK_DATA = {json.dumps(STOCKS)!r}\n\n\n')
add(10, 'stock_data',
    'Implement four functions. `get_stock_data(data=STOCK_DATA)` parses a JSON string '
    'and returns its list of stock dictionaries. `get_stocks_by_sector(stocks, sector)` '
    'returns matching dictionaries in input order; compare sector names exactly. '
    '`get_largest_stock(stocks)` returns the dictionary with the largest numeric market '
    'capitalization (`cap`). Caps have a leading `$`, a nonnegative decimal number, and '
    'an optional M, B, or T suffix (million, billion, trillion). A cap of `n/a` is unknown '
    'and is excluded. With a tie, return the first stock. If no stock has a known cap, '
    'return None. `get_market_distribution(stocks)` returns a Counter mapping each '
    '`market` to its number of records. Count duplicate records. All required fields '
    'are present. Do not modify the input. Empty input produces an empty list, None, '
    'or an empty Counter as appropriate. The supplied JSON is a small local sample '
    'with the fields shown in the public description. The public description does '
    'not give the four original function contracts; these four queries define this recreation.',
    STOCK_HEADER,
    '''def get_stock_data(data=STOCK_DATA):
    pass


def get_stocks_by_sector(stocks, sector):
    pass


def get_largest_stock(stocks):
    pass


def get_market_distribution(stocks):
    pass
''',
    '''def get_stock_data(data=STOCK_DATA):
    return json.loads(data)


def get_stocks_by_sector(stocks, sector):
    return [stock for stock in stocks if stock['sector'] == sector]


def get_largest_stock(stocks):
    largest, highest = None, Fraction(-1)
    multipliers = {'M': 10**6, 'B': 10**9, 'T': 10**12}
    for stock in stocks:
        cap = stock['cap']
        if cap == 'n/a':
            continue
        suffix = cap[-1]
        value = Fraction(cap[1:-1]) * multipliers[suffix] if suffix in multipliers else Fraction(cap[1:])
        if value > highest:
            largest, highest = stock, value
    return largest


def get_market_distribution(stocks):
    return Counter(stock['market'] for stock in stocks)
''',
    '''from collections import Counter
import json
from stock_data import (get_stock_data, get_stocks_by_sector,
                        get_largest_stock, get_market_distribution)


def test_default_json_and_types():
    stocks = get_stock_data()
    assert isinstance(stocks, list) and len(stocks) == 5
    assert stocks[0]['symbol'] == 'HBR'
    assert stocks[1]['id'] == 2


def test_custom_json_and_empty():
    assert get_stock_data('[]') == []
    assert get_stock_data('[{"symbol": "CAFÉ", "id": 7}]') == [{'symbol': 'CAFÉ', 'id': 7}]


def test_sector_filter_order_and_exact_case():
    stocks = get_stock_data()
    assert [s['symbol'] for s in get_stocks_by_sector(stocks, 'Health Care')] == ['MED', 'CARE']
    assert get_stocks_by_sector(stocks, 'health care') == []
    assert get_stocks_by_sector([], 'Technology') == []


def test_largest_default_and_numeric_units():
    assert get_largest_stock(get_stock_data())['symbol'] == 'CLD'
    stocks = [{'cap': '$999B'}, {'cap': '$1T'}, {'cap': '$999999M'}]
    assert get_largest_stock(stocks) is stocks[1]
    stocks = [{'cap': '$99M'}, {'cap': '$100M'}, {'cap': '$9M'}]
    assert get_largest_stock(stocks) is stocks[1]


def test_known_zero_and_unknown_caps():
    zero = {'cap': '$0'}
    assert get_largest_stock([{'cap': 'n/a'}, zero]) is zero
    assert get_largest_stock([{'cap': 'n/a'}]) is None
    assert get_largest_stock([]) is None


def test_equal_cap_keeps_first_and_decimal_precision():
    stocks = [{'cap': '$1.25B'}, {'cap': '$1250M'}, {'cap': '$1250000000'}]
    assert get_largest_stock(stocks) is stocks[0]
    stocks = [{'cap': '$1000000000000000000'}, {'cap': '$1000000000000000001'}]
    assert get_largest_stock(stocks) is stocks[1]
    stocks = [{'cap': '$10000000000000000000000000000M'},
              {'cap': '$10000000000000000000000000001M'}]
    assert get_largest_stock(stocks) is stocks[1]


def test_market_counts_and_duplicate_records():
    assert get_market_distribution(get_stock_data()) == Counter({'NASDAQ': 3, 'NYSE': 2})
    stock = {'market': 'OTHER'}
    result = get_market_distribution([stock, stock, {'market': 'NYSE'}])
    assert isinstance(result, Counter) and result == Counter({'OTHER': 2, 'NYSE': 1})
    assert get_market_distribution([]) == Counter()


def test_independent_loads_and_unchanged_inputs():
    stocks = get_stock_data()
    before = json.dumps(stocks, sort_keys=True)
    get_stocks_by_sector(stocks, 'Technology')
    get_largest_stock(stocks)
    get_market_distribution(stocks)
    assert json.dumps(stocks, sort_keys=True) == before
    stocks[0]['symbol'] = 'changed'
    assert get_stock_data()[0]['symbol'] == 'HBR'
''',
    [fault('reverse sector results', "return [stock for stock in stocks if stock['sector'] == sector]",
           "return [stock for stock in stocks if stock['sector'] == sector][::-1]"),
     fault('treat billions as millions', "'B': 10**9", "'B': 10**6"),
     fault('replace first equal capitalization', 'if value > highest:', 'if value >= highest:'),
     fault('count each market once', "Counter(stock['market'] for stock in stocks)",
           "Counter(set(stock['market'] for stock in stocks))")])


MEMBERS = '''id,first_name,last_name,email
1,Junie|Kybert;jkybert0@army.mil
2|Sid;Churching,schurching1@tumblr.com
3;Cherry,Dudbridge|cdudbridge2@nifty.com
4,Ada|Stone;ada@example.test
5|Lin;River,lin@example.test
6;Sam,Oak|sam@example.test
7,Noor|Vale;noor@example.test
8|Eli;Moon,eli@example.test
9;Luz,Sun|luz@example.test
10,Bo|Lake;bo@example.test
'''
add(11, 'messy_csv',
    'Implement `convert_to_json(data=members)`. `data` is a multiline string. The first '
    'nonblank line contains comma-separated column names. Each data row can use any '
    'mix of comma, pipe (`|`), and semicolon delimiters. Split all three delimiters. '
    'Return a JSON string containing a list of dictionaries in row order. Keep all '
    'field values as strings, including IDs, leading zeroes, whitespace, and empty '
    'fields. Ignore blank lines. Fields are unquoted and cannot contain delimiter '
    'characters or newlines. Column names are nonempty and unique. Each data row must '
    'have the same number of fields as the header; otherwise raise ValueError. Empty '
    'or header-only input returns the JSON representation of an empty list. The local '
    'sample has ten records; the first three follow the public example.',
    f'import json\nimport re\n\nmembers = {MEMBERS!r}\n\n\n',
    'def convert_to_json(data=members):\n    pass\n',
    '''def convert_to_json(data=members):
    lines = [line for line in data.splitlines() if line.strip()]
    if not lines:
        return json.dumps([])
    header = lines[0].split(',')
    rows = []
    for line in lines[1:]:
        values = re.split(r'[,|;]', line)
        if len(values) != len(header):
            raise ValueError('Row has a different field count from the header')
        rows.append(dict(zip(header, values)))
    return json.dumps(rows)
''',
    '''import json
import pytest
from messy_csv import convert_to_json


def test_default_all_records():
    output = convert_to_json()
    assert isinstance(output, str)
    rows = json.loads(output)
    assert len(rows) == 10
    assert rows[0] == {'id': '1', 'first_name': 'Junie', 'last_name': 'Kybert', 'email': 'jkybert0@army.mil'}
    assert rows[2]['last_name'] == 'Dudbridge' and rows[-1]['id'] == '10'


def test_mixed_delimiters_in_one_row():
    assert json.loads(convert_to_json('a,b,c,d\\n1|2;3,4')) == [{'a': '1', 'b': '2', 'c': '3', 'd': '4'}]


def test_strings_preserve_zeroes_and_spaces():
    assert json.loads(convert_to_json('id,name\\n001; Ada ')) == [{'id': '001', 'name': ' Ada '}]


def test_empty_fields_are_retained():
    assert json.loads(convert_to_json('a,b,c\\n|middle;\\nleft,,right')) == [
        {'a': '', 'b': 'middle', 'c': ''}, {'a': 'left', 'b': '', 'c': 'right'}]


def test_blank_lines_crlf_and_empty_input():
    assert json.loads(convert_to_json('\\r\\na,b\\r\\n\\r\\n1;2\\r\\n   \\r\\n3|4\\r\\n')) == [
        {'a': '1', 'b': '2'}, {'a': '3', 'b': '4'}]
    assert json.loads(convert_to_json('')) == []
    assert json.loads(convert_to_json('a,b\\n')) == []


def test_unicode_and_json_escaping():
    data = 'id,name\\n1;Zoë "Z"\\n2|back\\\\slash'
    assert json.loads(convert_to_json(data)) == [
        {'id': '1', 'name': 'Zoë "Z"'}, {'id': '2', 'name': 'back\\\\slash'}]


def test_wrong_field_counts():
    with pytest.raises(ValueError):
        convert_to_json('a,b\\n1')
    with pytest.raises(ValueError):
        convert_to_json('a,b\\n1;2;3')


def test_single_column_duplicate_rows_and_fresh_result():
    text = 'value\\nalpha\\nalpha'
    assert json.loads(convert_to_json(text)) == [{'value': 'alpha'}, {'value': 'alpha'}]
    assert convert_to_json(text) == convert_to_json(text)
''',
    [fault('ignore semicolons', "r'[,|;]'", "r'[,|]'"),
     fault('trim field whitespace', "values = re.split(r'[,|;]', line)",
           "values = [value.strip() for value in re.split(r'[,|;]', line)]"),
     fault('silently truncate malformed rows', 'if len(values) != len(header):', 'if False:')])


LOG_DATA = '''bite,user,completed
102,alex,False
101,alex,True
29,bea,True
9,cy,False
101,bea,True
29,alex,False
'''
STATS_HEADER = f'import csv\nfrom collections import Counter\nfrom io import StringIO\n\nLOG_DATA = {LOG_DATA!r}\n\n\n'
STATS_TEMPLATE = '''class BiteStats:
    def __init__(self, data=LOG_DATA):
        pass

    @property
    def total_attempts(self):
        pass

    @property
    def total_users(self):
        pass

    @property
    def total_bites(self):
        pass

    @property
    def total_completed(self):
        pass

    @property
    def most_active_user(self):
        pass

    @property
    def most_popular_bite(self):
        pass
'''
add(12, 'bite_stats',
    'Implement `BiteStats(data=LOG_DATA)`. `data` is CSV text with columns '
    '`bite,user,completed`. Read it with csv.DictReader and store the list of string '
    'dictionaries in `self.rows`. Bite IDs are positive integer strings. User names '
    'are nonempty strings. The completed field is exactly `True` or `False`. Implement '
    'six read-only properties. `total_attempts` counts all rows. `total_users` counts '
    'distinct user names. `total_bites` counts distinct bite IDs. `total_completed` '
    'counts rows whose completed field is `True`. Each row is one attempt, so repeated '
    'attempts and repeated completions count. `most_active_user` returns the name with '
    'the most rows; ties use alphabetical order. `most_popular_bite` returns the integer '
    'bite ID with the most rows; ties use the smallest integer ID. Header-only data '
    'has all four counts equal to zero and both most-popular values equal to None. '
    'Do not change self.rows when reading properties. The public description does '
    'not list the original six property names; these six statistics define this recreation.',
    STATS_HEADER, STATS_TEMPLATE,
    '''class BiteStats:
    def __init__(self, data=LOG_DATA):
        self.rows = list(csv.DictReader(StringIO(data)))

    @property
    def total_attempts(self):
        return len(self.rows)

    @property
    def total_users(self):
        return len({row['user'] for row in self.rows})

    @property
    def total_bites(self):
        return len({int(row['bite']) for row in self.rows})

    @property
    def total_completed(self):
        return sum(row['completed'] == 'True' for row in self.rows)

    @property
    def most_active_user(self):
        counts = Counter(row['user'] for row in self.rows)
        return min(counts, key=lambda user: (-counts[user], user)) if counts else None

    @property
    def most_popular_bite(self):
        counts = Counter(int(row['bite']) for row in self.rows)
        return min(counts, key=lambda bite: (-counts[bite], bite)) if counts else None
''',
    '''import json
import pytest
from bite_stats import BiteStats


def test_default_six_statistics():
    stats = BiteStats()
    assert (stats.total_attempts, stats.total_users, stats.total_bites, stats.total_completed) == (6, 3, 4, 3)
    assert stats.most_active_user == 'alex'
    assert stats.most_popular_bite == 29


def test_rows_are_string_dictionaries_and_csv_quotes():
    stats = BiteStats('bite,user,completed\\n7,"Lee, Ada",False\\n')
    assert stats.rows == [{'bite': '7', 'user': 'Lee, Ada', 'completed': 'False'}]
    assert stats.most_active_user == 'Lee, Ada'
    assert stats.most_popular_bite == 7


def test_empty_data():
    stats = BiteStats('bite,user,completed\\n')
    assert stats.rows == []
    assert (stats.total_attempts, stats.total_users, stats.total_bites, stats.total_completed) == (0, 0, 0, 0)
    assert stats.most_active_user is None
    assert stats.most_popular_bite is None


def test_single_false_is_not_truthy_completion():
    stats = BiteStats('bite,user,completed\\n42,solo,False\\n')
    assert stats.total_completed == 0
    assert stats.total_attempts == stats.total_users == stats.total_bites == 1
    assert stats.most_active_user == 'solo' and stats.most_popular_bite == 42


def test_duplicate_completions_are_attempts():
    stats = BiteStats('bite,user,completed\\n1,a,True\\n1,a,True\\n1,a,False\\n')
    assert stats.total_attempts == 3 and stats.total_completed == 2
    assert stats.total_users == stats.total_bites == 1


def test_ties_use_alphabetical_user_and_numeric_bite():
    stats = BiteStats('bite,user,completed\\n10,zulu,True\\n2,alpha,False\\n')
    assert stats.most_active_user == 'alpha'
    assert stats.most_popular_bite == 2


def test_frequency_wins_before_tie_rule():
    stats = BiteStats('bite,user,completed\\n2,alpha,False\\n10,zulu,False\\n10,zulu,False\\n')
    assert stats.most_active_user == 'zulu' and stats.most_popular_bite == 10


def test_properties_do_not_change_rows_and_instances_are_independent():
    stats = BiteStats()
    before = json.dumps(stats.rows, sort_keys=True)
    for name in ('total_attempts', 'total_users', 'total_bites', 'total_completed',
                 'most_active_user', 'most_popular_bite'):
        getattr(stats, name)
        assert isinstance(getattr(BiteStats, name), property)
        with pytest.raises(AttributeError):
            setattr(stats, name, 0)
    assert json.dumps(stats.rows, sort_keys=True) == before
    stats.rows.clear()
    assert len(BiteStats().rows) == 6
''',
    [fault('treat False text as true', "row['completed'] == 'True'", "bool(row['completed'])"),
     fault('count attempts as unique users', "len({row['user'] for row in self.rows})", 'len(self.rows)'),
     fault('choose least frequent user', '(-counts[user], user)', '(counts[user], user)'),
     fault('compare bite IDs as text', "Counter(int(row['bite']) for row in self.rows)",
           "Counter(row['bite'] for row in self.rows)")])


COUNTRIES_XML = '''<?xml version="1.0" encoding="utf-8"?>
<wb:countries xmlns:wb="http://www.worldbank.org" page="1" pages="1">
  <wb:country id="ARG"><wb:name>Argentina</wb:name><wb:incomeLevel id="UMC">Upper middle income</wb:incomeLevel></wb:country>
  <wb:country id="CHL"><wb:name>Chile</wb:name><wb:incomeLevel id="HIC">High income</wb:incomeLevel></wb:country>
  <wb:country id="BOL"><wb:name>Bolivia</wb:name><wb:incomeLevel id="LMC">Lower middle income</wb:incomeLevel></wb:country>
  <wb:country id="BRA"><wb:name>Brazil</wb:name><wb:incomeLevel id="UMC">Upper middle income</wb:incomeLevel></wb:country>
  <wb:country id="URY"><wb:name>Uruguay</wb:name><wb:incomeLevel id="HIC">High income</wb:incomeLevel></wb:country>
</wb:countries>
'''
XML_HEADER = ('from collections import defaultdict\nimport xml.etree.ElementTree as ET\n\n'
              "NAMESPACE = {'wb': 'http://www.worldbank.org'}\n"
              f'COUNTRIES_XML = {COUNTRIES_XML!r}\n\n\n')
add(13, 'income_distribution',
    'Implement `get_income_distribution(path=None)`. When path is given, read that '
    'XML file (a string path or pathlib.Path). Otherwise parse COUNTRIES_XML, the '
    'supplied local sample. The root is a World Bank countries element. Its direct '
    'country children each have direct name and incomeLevel children in namespace '
    '`http://www.worldbank.org`. Return a dictionary mapping incomeLevel text labels '
    'to lists of country names. Strip surrounding whitespace from names and labels. '
    'Use the label text, not the incomeLevel id attribute. Preserve country order '
    'within each list and retain duplicate entries. A root without countries returns '
    'an empty dictionary. Return fresh dictionaries and lists on each call. A dict '
    'or defaultdict(list) is accepted. Namespace prefixes can differ. All country '
    'entries have nonempty names and income labels. Propagate XML parse and file '
    'errors. The original remote file is replaced by a small synthetic sample; these '
    'labels are exercise data, not current financial classifications.',
    XML_HEADER,
    'def get_income_distribution(path=None):\n    pass\n',
    '''def get_income_distribution(path=None):
    root = ET.fromstring(COUNTRIES_XML) if path is None else ET.parse(path).getroot()
    distribution = defaultdict(list)
    for country in root.findall('wb:country', NAMESPACE):
        name = country.find('wb:name', NAMESPACE).text.strip()
        income = country.find('wb:incomeLevel', NAMESPACE).text.strip()
        distribution[income].append(name)
    return dict(distribution)
''',
    '''import pytest
import xml.etree.ElementTree as ET
from income_distribution import get_income_distribution


def save(tmp_path, text):
    path = tmp_path / 'countries.xml'
    path.write_text(text, encoding='utf-8')
    return path


def test_default_local_sample():
    assert get_income_distribution() == {
        'Upper middle income': ['Argentina', 'Brazil'],
        'High income': ['Chile', 'Uruguay'], 'Lower middle income': ['Bolivia']}


def test_custom_file_and_namespace_prefix(tmp_path):
    text = '<x:countries xmlns:x="http://www.worldbank.org"><x:country>'
    text += '<x:name>Example</x:name><x:incomeLevel id="OTHER">Custom label</x:incomeLevel>'
    text += '</x:country></x:countries>'
    path = save(tmp_path, text)
    assert get_income_distribution(path) == {'Custom label': ['Example']}
    assert get_income_distribution(str(path)) == {'Custom label': ['Example']}


def test_empty_root(tmp_path):
    path = save(tmp_path, '<countries xmlns="http://www.worldbank.org"/>')
    assert get_income_distribution(path) == {}


def test_strip_text_and_decode_entities(tmp_path):
    text = '<countries xmlns="http://www.worldbank.org"><country>'
    text += '<name>  São Tomé &amp; Príncipe  </name><incomeLevel id="L"> Low income </incomeLevel>'
    text += '</country></countries>'
    assert get_income_distribution(save(tmp_path, text)) == {'Low income': ['São Tomé & Príncipe']}


def test_order_duplicates_and_labels_not_ids(tmp_path):
    text = '<countries xmlns="http://www.worldbank.org">'
    for name, code, label in [('Zed', 'X', 'Group'), ('Other', 'X', 'Other group'),
                              ('Alpha', 'Y', 'Group'), ('Zed', 'X', 'Group')]:
        text += '<country><name>' + name + '</name><incomeLevel id="' + code + '">' + label + '</incomeLevel></country>'
    text += '</countries>'
    assert get_income_distribution(save(tmp_path, text)) == {'Group': ['Zed', 'Alpha', 'Zed'], 'Other group': ['Other']}


def test_only_direct_country_name(tmp_path):
    text = '<countries xmlns="http://www.worldbank.org"><country>'
    text += '<region><name>Ignore this nested name</name></region><name>Country name</name>'
    text += '<incomeLevel id="X">Label</incomeLevel></country></countries>'
    assert get_income_distribution(save(tmp_path, text)) == {'Label': ['Country name']}


def test_fresh_results():
    first = get_income_distribution()
    first['High income'].append('extra')
    first['new'] = ['extra']
    assert get_income_distribution()['High income'] == ['Chile', 'Uruguay']
    assert 'new' not in get_income_distribution()


def test_parse_and_file_errors(tmp_path):
    with pytest.raises(ET.ParseError):
        get_income_distribution(save(tmp_path, '<broken>'))
    with pytest.raises(FileNotFoundError):
        get_income_distribution(tmp_path / 'missing.xml')
''',
    [fault('group by income ID', "country.find('wb:incomeLevel', NAMESPACE).text.strip()",
           "country.find('wb:incomeLevel', NAMESPACE).get('id')"),
     fault('replace earlier countries in a group', 'distribution[income].append(name)',
           'distribution[income] = [name]'),
     fault('keep surrounding text whitespace', ".text.strip()", '.text')])
