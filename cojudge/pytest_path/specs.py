"""Ten test-writing exercises. Targets 2–10 are explicit offline recreations."""
from textwrap import dedent


def code(value):
    return dedent(value).strip() + '\n'


def exercise(number, module, target, reference, mutations, contract, starter=None):
    return {'number': number, 'module': module, 'target': code(target), 'reference': code(reference),
            'mutations': [{'name': name, 'old': old, 'new': new} for name, old, new in mutations],
            'contract': contract, 'starter': starter or f'import pytest\nimport {module}\n\n\ndef test_example():\n    # Replace this with tests of the supplied module.\n    pass\n'}


SPECS = [exercise(1, 'fibonacci', '''
    from functools import cache

    @cache
    def fib(n):
       if n < 0:
            raise ValueError
       elif n in (0, 1):
           return n
       else:
           return(fib(n-1) + fib(n-2))
''', '''
    import pytest
    from fibonacci import fib

    @pytest.mark.parametrize('n, expected', [(0, 0), (1, 1), (2, 1), (3, 2), (10, 55), (50, 12586269025)])
    def test_values(n, expected):
        assert fib(n) == expected

    @pytest.mark.parametrize('n', [-1, -10])
    def test_negative(n):
        with pytest.raises(ValueError):
            fib(n)
''', [
    ('reject zero', 'n < 0', 'n <= 0'),
    ('accept negative input', 'raise ValueError', 'return 0'),
    ('wrong base case', 'return n', 'return 1'),
    ('subtract recursive terms', 'fib(n-1) + fib(n-2)', 'fib(n-1) - fib(n-2)'),
    ('wrong recurrence', 'fib(n-1) + fib(n-2)', 'fib(n-1) + fib(n-1)'),
], 'Pass integer n. Negative n raises ValueError. fib(0)=0 and fib(1)=1. Higher n follows the Fibonacci recurrence. Test n up to 50.',
    starter='from fibonacci import fib\nimport pytest\n\n\n# Write test_ functions below.\n'),
exercise(2, 'digits', '''
    def list_to_decimal(digits):
        result = 0
        for digit in digits:
            if type(digit) is not int:
                raise TypeError('digits must be integers')
            if not 0 <= digit <= 9:
                raise ValueError('digits must be in range 0..9')
            result = result * 10 + digit
        return result
''', '''
    import pytest
    from digits import list_to_decimal

    @pytest.mark.parametrize('digits, expected', [([], 0), ([0], 0), ([9], 9), ([0, 4, 2, 8], 428), ([1, 0, 2], 102)])
    def test_decimal(digits, expected):
        assert list_to_decimal(digits) == expected

    @pytest.mark.parametrize('digit', [True, False, 3.6, '4', None])
    def test_types(digit):
        with pytest.raises(TypeError):
            list_to_decimal([1, digit])

    @pytest.mark.parametrize('digit', [-1, 10, 12])
    def test_range(digit):
        with pytest.raises(ValueError):
            list_to_decimal([digit])
''', [
    ('accept booleans', 'type(digit) is not int', 'not isinstance(digit, int)'),
    ('reject zero digit', '0 <= digit', '0 < digit'),
    ('accept ten', 'digit <= 9', 'digit <= 10'),
    ('wrong place value', 'result * 10 + digit', 'result + digit'),
    ('wrong empty result', 'result = 0', 'result = 1'),
], 'list_to_decimal(digits) accepts a list of integer digits 0..9. Booleans and other types raise TypeError. Out-of-range integers raise ValueError. Empty input returns 0. Leading zeroes are allowed.'),
exercise(3, 'printing', '''
    def print_even_numbers(numbers):
        for number in numbers:
            if number % 2 == 0:
                print(number)
''', '''
    import pytest
    from printing import print_even_numbers

    @pytest.mark.parametrize('numbers, expected', [([], ''), ([1, 3], ''), ([0, 1, 2, 3, 4], '0\\n2\\n4\\n'), ([-4, -3, -2], '-4\\n-2\\n'), ([2, 2], '2\\n2\\n')])
    def test_output(numbers, expected, capsys):
        assert print_even_numbers(numbers) is None
        captured = capsys.readouterr()
        assert captured.out == expected
        assert captured.err == ''
''', [
    ('print odd numbers', 'number % 2 == 0', 'number % 2 != 0'),
    ('omit zero', 'number % 2 == 0', 'number != 0 and number % 2 == 0'),
    ('omit negative numbers', 'number % 2 == 0', 'number >= 0 and number % 2 == 0'),
    ('omit newline', 'print(number)', 'print(number, end="")'),
    ('deduplicate output', 'for number in numbers:', 'for number in dict.fromkeys(numbers):'),
], 'print_even_numbers(numbers) accepts a list of integers. Print each even number on its own line, in input order. Preserve duplicates, zero, and negative values. Return None. Print nothing for empty input or an all-odd list.'),
exercise(4, 'fizzbuzz', '''
    def fizzbuzz(n):
        if n % 15 == 0:
            return 'FizzBuzz'
        if n % 3 == 0:
            return 'Fizz'
        if n % 5 == 0:
            return 'Buzz'
        return n
''', '''
    import pytest
    from fizzbuzz import fizzbuzz

    @pytest.mark.parametrize('n, expected', [(1, 1), (2, 2), (3, 'Fizz'), (6, 'Fizz'), (5, 'Buzz'), (10, 'Buzz'), (15, 'FizzBuzz'), (30, 'FizzBuzz'), (0, 'FizzBuzz'), (-3, 'Fizz'), (-5, 'Buzz'), (-15, 'FizzBuzz')])
    def test_fizzbuzz(n, expected):
        assert fizzbuzz(n) == expected
''', [
    ('wrong combined divisor', 'n % 15 == 0', 'n % 15 == 1'),
    ('wrong fizz divisor', 'n % 3 == 0', 'n % 3 == 1'),
    ('wrong buzz divisor', 'n % 5 == 0', 'n % 5 == 1'),
    ('wrong combined text', "return 'FizzBuzz'", "return 'BuzzFizz'"),
    ('convert plain integers to text', 'return n', 'return str(n)'),
], 'fizzbuzz(n) accepts any integer, including zero and negatives. Multiples of 15 return FizzBuzz. Other multiples of 3 return Fizz. Other multiples of 5 return Buzz. Return the original integer otherwise.'),
exercise(5, 'ips', '''
    import json
    from dataclasses import dataclass
    from ipaddress import IPv4Network

    @dataclass(frozen=True)
    class IPRange:
        network: IPv4Network
        region: str
        service: str

    def parse_ranges(text):
        return [IPRange(IPv4Network(item['ip_prefix']), item['region'], item['service'])
                for item in json.loads(text)['prefixes']]

    def get_ranges(path):
        with open(path, encoding='utf-8') as stream:
            return parse_ranges(stream.read())

    def filter_ranges(ranges, region=None, service=None):
        return [item for item in ranges
                if (region is None or item.region == region)
                and (service is None or item.service == service)]
''', '''
    import json
    from ipaddress import IPv4Network
    import pytest
    from ips import IPRange, parse_ranges, get_ranges, filter_ranges

    @pytest.fixture
    def ranges(tmp_path):
        path = tmp_path / 'ranges.json'
        path.write_text(json.dumps({'prefixes': [
            {'ip_prefix': '10.0.0.0/24', 'region': 'west', 'service': 'EC2'},
            {'ip_prefix': '192.0.2.0/24', 'region': 'east', 'service': 'S3'},
            {'ip_prefix': '198.51.100.0/24', 'region': 'west', 'service': 'S3'}]}))
        return get_ranges(path)

    def test_parse(ranges):
        assert ranges[0] == IPRange(IPv4Network('10.0.0.0/24'), 'west', 'EC2')
        assert len(ranges) == 3
        assert parse_ranges('{"prefixes": []}') == []
        assert len(filter_ranges(ranges)) == 3
        assert filter_ranges(ranges, region='west') == [ranges[0], ranges[2]]
        assert filter_ranges(ranges, service='S3') == [ranges[1], ranges[2]]
        assert filter_ranges(ranges, region='west', service='S3') == [ranges[2]]
        assert filter_ranges(ranges, region='missing') == []

    def test_errors():
        with pytest.raises(ValueError):
            parse_ranges('broken')
        with pytest.raises(KeyError):
            parse_ranges('{}')
        with pytest.raises(ValueError):
            parse_ranges('{"prefixes": [{"ip_prefix": "invalid", "region": "x", "service": "y"}]}')
''', [
    ('swap region and service', "item['region'], item['service']", "item['service'], item['region']"),
    ('skip the first range', "json.loads(text)['prefixes']", "json.loads(text)['prefixes'][1:]"),
    ('invert region filter', 'item.region == region', 'item.region != region'),
    ('invert service filter', 'item.service == service', 'item.service != service'),
    ('combine filters with or', 'and (service is None', 'or (service is None'),
], 'parse_ranges(text) parses a JSON object with a prefixes list. Each item has ip_prefix, region, and service. Return frozen IPRange dataclass objects in input order. Use strict IPv4Network parsing. get_ranges(path) reads UTF-8 JSON from a local file. filter_ranges applies optional exact region and service filters together. Propagate JSON, key, IP, and file errors.'),
exercise(6, 'colors', '''
    from random import sample

    HEX = '0123456789ABCDEF'

    def gen_hex_color():
        while True:
            yield '#' + ''.join(sample(HEX, 6))
''', '''
    from unittest.mock import patch
    import pytest
    from colors import gen_hex_color, HEX

    @pytest.fixture
    def gen():
        return gen_hex_color()

    def test_colors(gen):
        with patch('colors.sample', side_effect=[list('A1B2C3'), list('FEDCBA')]) as sample:
            assert next(gen) == '#A1B2C3'
            assert next(gen) == '#FEDCBA'
            assert sample.call_count == 2
            sample.assert_called_with('0123456789ABCDEF', 6)
''', [
    ('missing hash prefix', "yield '#' +", "yield '' +"),
    ('wrong sample size', 'sample(HEX, 6)', 'sample(HEX, 5)'),
    ('lowercase output', "''.join(sample(HEX, 6))", "''.join(sample(HEX, 6)).lower()"),
    ('generator stops early', 'while True:', 'for _ in range(1):'),
    ('wrong character alphabet', "HEX = '0123456789ABCDEF'", "HEX = '0123456789ABCDE'"),
], 'gen_hex_color() yields indefinitely. Each next() calls colors.sample(HEX, 6), where HEX is 0123456789ABCDEF. Join the sampled characters without changes and prepend #. Patch colors.sample to make tests deterministic. Check successive yields and the sample arguments.'),
]
SPECS += [exercise(7, 'account', '''
    class Account:
        def __init__(self, owner, amount=0):
            if type(amount) is not int:
                raise TypeError('amount must be an integer')
            self.owner, self.amount = owner, amount
            self._transactions = []

        @property
        def balance(self):
            return self.amount + sum(self._transactions)

        def add_transaction(self, amount):
            if type(amount) is not int:
                raise TypeError('amount must be an integer')
            self._transactions.append(amount)

        def __len__(self):
            return len(self._transactions)

        def __getitem__(self, index):
            return self._transactions[index]

        def __str__(self):
            return f'Account of {self.owner} with starting amount: {self.amount}'

        def __repr__(self):
            return f'Account({self.owner!r}, {self.amount!r})'

        def __eq__(self, other):
            if not isinstance(other, Account):
                return NotImplemented
            return self.balance == other.balance

        def __lt__(self, other):
            if not isinstance(other, Account):
                return NotImplemented
            return self.balance < other.balance
''', '''
    import pytest
    from account import Account

    def test_initial_and_representation():
        default = Account('Ada')
        assert default.balance == 0
        assert len(default) == 0
        account = Account('Bob', 10)
        assert account.owner == 'Bob'
        assert account.amount == 10
        assert str(account) == 'Account of Bob with starting amount: 10'
        assert repr(account) == "Account('Bob', 10)"

    def test_transactions():
        account = Account('Ada', 10)
        account.add_transaction(5)
        account.add_transaction(-3)
        account.add_transaction(0)
        assert account.balance == 12
        assert len(account) == 3
        assert list(account) == [5, -3, 0]
        assert account[-1] == 0
        assert account[:2] == [5, -3]
        with pytest.raises(IndexError):
            _ = account[3]
        assert Account('Other').balance == 0

    @pytest.mark.parametrize('value', [True, 1.5, '2', None])
    def test_invalid_amounts(value):
        with pytest.raises(TypeError, match='integer'):
            Account('Ada', value)
        with pytest.raises(TypeError, match='integer'):
            Account('Ada').add_transaction(value)

    def test_comparisons():
        first, second = Account('A', 3), Account('B', 8)
        first.add_transaction(5)
        assert first == second
        assert not first < second
        second.add_transaction(1)
        assert first < second
        assert first != object()
        with pytest.raises(TypeError):
            _ = first < object()
''', [
    ('ignore starting amount', 'self.amount + sum(self._transactions)', 'sum(self._transactions)'),
    ('subtract transactions', 'self.amount + sum(self._transactions)', 'self.amount - sum(self._transactions)'),
    ('reject zero transactions', 'self._transactions.append(amount)', "self._transactions.append(amount) if amount else None"),
    ('accept booleans as amounts', 'type(amount) is not int', 'not isinstance(amount, int)'),
    ('count starting amount as a transaction', 'return len(self._transactions)', 'return len(self._transactions) + 1'),
    ('compare initial amounts', 'return self.balance == other.balance', 'return self.amount == other.amount'),
    ('less than includes equality', 'return self.balance < other.balance', 'return self.balance <= other.balance'),
], 'Account(owner, amount=0) stores a name and an integer initial amount. Reject non-integers including booleans. add_transaction accepts positive, negative, or zero integers. balance includes the initial amount and all transactions. len counts transactions. Indexing, slicing, and iteration expose transactions. str and repr use the exact formats in the supplied code. Compare Accounts by current balance, and return NotImplemented for unrelated types.'),
exercise(8, 'zodiac', '''
    from datetime import date

    # Small static data set for offline parsing and date-boundary practice.
    DATA = [
        {'name': 'Aries', 'start': (3, 21), 'end': (4, 19), 'famous_people': ['A', 'B'], 'compatible': ['Leo']},
        {'name': 'Taurus', 'start': (4, 20), 'end': (5, 20), 'famous_people': ['C'], 'compatible': ['Virgo']},
        {'name': 'Gemini', 'start': (5, 21), 'end': (6, 20), 'famous_people': ['D'], 'compatible': ['Libra']},
        {'name': 'Cancer', 'start': (6, 21), 'end': (7, 22), 'famous_people': ['E'], 'compatible': ['Pisces']},
        {'name': 'Leo', 'start': (7, 23), 'end': (8, 22), 'famous_people': ['F', 'G', 'H'], 'compatible': ['Aries']},
        {'name': 'Virgo', 'start': (8, 23), 'end': (9, 22), 'famous_people': [], 'compatible': ['Taurus']},
        {'name': 'Libra', 'start': (9, 23), 'end': (10, 22), 'famous_people': [], 'compatible': []},
        {'name': 'Scorpio', 'start': (10, 23), 'end': (11, 21), 'famous_people': [], 'compatible': []},
        {'name': 'Sagittarius', 'start': (11, 22), 'end': (12, 21), 'famous_people': [], 'compatible': []},
        {'name': 'Capricorn', 'start': (12, 22), 'end': (1, 19), 'famous_people': [], 'compatible': []},
        {'name': 'Aquarius', 'start': (1, 20), 'end': (2, 18), 'famous_people': [], 'compatible': []},
        {'name': 'Pisces', 'start': (2, 19), 'end': (3, 20), 'famous_people': [], 'compatible': ['Cancer']},
    ]

    def get_signs():
        from copy import deepcopy
        return deepcopy(DATA)

    def get_sign_with_most_famous_people(signs):
        return max(signs, key=lambda sign: len(sign['famous_people']))['name']

    def signs_are_mutually_compatible(signs, first, second):
        by_name = {sign['name']: sign for sign in signs}
        return (second in by_name[first]['compatible']
                and first in by_name[second]['compatible'])

    def get_sign_by_date(signs, day):
        value = (day.month, day.day)
        for sign in signs:
            start, end = sign['start'], sign['end']
            if start <= end:
                matches = start <= value <= end
            else:
                matches = value >= start or value <= end
            if matches:
                return sign['name']
        raise ValueError('date has no matching sign')
''', '''
    from datetime import date
    import pytest
    from zodiac import get_signs, get_sign_with_most_famous_people, signs_are_mutually_compatible, get_sign_by_date

    @pytest.fixture
    def signs():
        return get_signs()

    def test_most_and_independent_data(signs):
        assert get_sign_with_most_famous_people(signs) == 'Leo'
        signs[0]['famous_people'].append('Extra')
        assert len(get_signs()[0]['famous_people']) == 2
        assert get_sign_with_most_famous_people([signs[1], signs[2]]) == 'Taurus'
        with pytest.raises(ValueError):
            get_sign_with_most_famous_people([])

    def test_compatibility(signs):
        assert signs_are_mutually_compatible(signs, 'Aries', 'Leo') is True
        assert signs_are_mutually_compatible(signs, 'Gemini', 'Libra') is False
        assert signs_are_mutually_compatible(signs, 'Aries', 'Taurus') is False
        with pytest.raises(KeyError):
            signs_are_mutually_compatible(signs, 'Unknown', 'Leo')

    @pytest.mark.parametrize('month, day, expected', [(3, 21, 'Aries'), (4, 19, 'Aries'), (4, 20, 'Taurus'), (12, 22, 'Capricorn'), (12, 31, 'Capricorn'), (1, 1, 'Capricorn'), (1, 19, 'Capricorn'), (1, 20, 'Aquarius'), (2, 29, 'Pisces')])
    def test_dates(signs, month, day, expected):
        assert get_sign_by_date(signs, date(2024, month, day)) == expected

    def test_no_match():
        with pytest.raises(ValueError, match='no matching'):
            get_sign_by_date([], date(2024, 1, 1))
''', [
    ('return fewest famous people', 'max(signs, key=', 'min(signs, key='),
    ('one way compatibility', "and first in by_name[second]['compatible']", "or first in by_name[second]['compatible']"),
    ('exclude start date', 'start <= value <= end', 'start < value <= end'),
    ('exclude end date', 'start <= value <= end', 'start <= value < end'),
    ('break year wrap', 'value >= start or value <= end', 'value >= start and value <= end'),
    ('return shared static data', 'return deepcopy(DATA)', 'return DATA'),
], 'Use the supplied static 12-sign data. get_signs() returns independent copies. get_sign_with_most_famous_people(signs) returns the name with the largest list; ties use the first item; empty input raises ValueError. signs_are_mutually_compatible requires both directions and exact names; unknown names raise KeyError. get_sign_by_date(signs, day) accepts datetime.date. Endpoints are inclusive. Capricorn spans the year boundary. No matching date raises ValueError. The data is constructed for practice.'),
exercise(9, 'guessing', '''
    class GuessingGame:
        def __init__(self, secret, max_guesses=5):
            if type(secret) is not int or not 1 <= secret <= 20:
                raise ValueError('secret must be an integer from 1 to 20')
            if type(max_guesses) is not int or max_guesses < 1:
                raise ValueError('max_guesses must be a positive integer')
            self.secret, self.max_guesses = secret, max_guesses

        def play(self):
            for _ in range(self.max_guesses):
                text = input('Guess a number: ')
                try:
                    guess = int(text)
                except ValueError:
                    print('Enter a number')
                    continue
                if guess == self.secret:
                    print('You win!')
                    return True
                if guess < self.secret:
                    print('Too low')
                else:
                    print('Too high')
            print(f'You lose! The number was {self.secret}')
            return False
''', '''
    from unittest.mock import patch
    import pytest
    from guessing import GuessingGame

    @pytest.mark.parametrize('secret', [0, 21, True, '2', 1.5])
    def test_secret_validation(secret):
        with pytest.raises(ValueError, match='secret must be an integer from 1 to 20'):
            GuessingGame(secret)

    @pytest.mark.parametrize('limit', [0, -1, True, '2', 1.5])
    def test_limit_validation(limit):
        with pytest.raises(ValueError, match='max_guesses must be a positive integer'):
            GuessingGame(10, limit)

    @pytest.mark.parametrize('secret', [1, 20])
    def test_endpoints(secret, capsys):
        game = GuessingGame(secret)
        assert game.max_guesses == 5
        with patch('builtins.input', return_value=str(secret)):
            assert game.play() is True
        assert capsys.readouterr().out == 'You win!\\n'

    def test_win_on_last_guess(capsys):
        with patch('builtins.input', side_effect=['x', '9', '11', '10']) as read:
            assert GuessingGame(10, 4).play() is True
            assert read.call_count == 4
        assert capsys.readouterr().out == 'Enter a number\\nToo low\\nToo high\\nYou win!\\n'

    def test_loss(capsys):
        with patch('builtins.input', side_effect=['1', '20']) as read:
            assert GuessingGame(10, 2).play() is False
            assert read.call_count == 2
        assert capsys.readouterr().out == 'Too low\\nToo high\\nYou lose! The number was 10\\n'
''', [
    ('reject lower endpoint', '1 <= secret <= 20', '1 < secret <= 20'),
    ('reject upper endpoint', '1 <= secret <= 20', '1 <= secret < 20'),
    ('accept boolean secret', 'type(secret) is not int', 'not isinstance(secret, int)'),
    ('omit last attempt', 'range(self.max_guesses)', 'range(self.max_guesses - 1)'),
    ('swap high and low', 'guess < self.secret', 'guess > self.secret'),
    ('wrong winning result', 'return True', 'return False'),
    ('wrong losing result', 'return False', 'return True'),
], 'GuessingGame(secret, max_guesses=5) accepts an integer secret in 1..20 and a positive integer limit; reject booleans. Use the exact validation messages in the supplied code. play() reads input for at most max_guesses attempts. Non-numeric input consumes an attempt. Print Enter a number, Too low, Too high, or You win! as applicable. A win returns True immediately. Exhausted attempts print You lose! The number was N and return False. Mock builtins.input. The default prompt is Guess a number: .'),
exercise(10, 'movies', '''
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
''', '''
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
''', [
    ('exclude exact score threshold', 'WHERE score >= ?', 'WHERE score > ?'),
    ('wrong year filter', 'AND year = ?', 'AND year != ?'),
    ('exact title instead of substring', "args.append('%' + title + '%')", 'args.append(title)'),
    ('reverse title ordering', 'ORDER BY title', 'ORDER BY title DESC'),
    ('wrong deletion count', 'return cursor.rowcount', 'return 0'),
    ('omit insert commit', "(title, year, score))\n        self.connection.commit()", '(title, year, score))'),
    ('omit delete commit', "(title,))\n        self.connection.commit()", '(title,))'),
], 'MovieDB(path=":memory:") opens SQLite. init() creates and seeds the table with the three supplied rows. query(title=None, min_score=0, year=None) returns (title, year, score) tuples sorted by title. title is a case-insensitive SQL LIKE substring; min_score is inclusive; all filters combine. add inserts and commits; duplicate titles raise sqlite3.IntegrityError. delete removes an exact title, commits, and returns its row count. drop_table removes the table. close closes the connection. Use a yield fixture with teardown. Use tmp_path to test file persistence.'),
]
