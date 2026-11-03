"""Guided starters (the Pybites OOP bite 15 pattern) for the selected exercises.

In this course the learner writes tests. Each starter explains the pytest
feature, how the judge grades a test suite, which faults the suite must catch,
and gives test skeletons with TODO comments. Targets, faults and reference
tests do not change.
"""

_JUDGE = r'''# How the judge grades your tests
# -------------------------------
#   baseline  -> every test you write PASSES on the correct code, and your
#                tests run at least 90% of its lines.
#   one check per FAULT -> the judge swaps in a broken copy of the code. At
#                least one of your tests must FAIL on it. If none fails, the
#                result is SURVIVED <fault name>.
'''

STARTERS = {
    1: r'''import pytest
from fibonacci import fib

# What you practise
# -----------------
# 1. A pytest test is a function whose name starts with test_. It uses plain
#    assert. A failed assert fails the test.
# 2. @pytest.mark.parametrize runs one test function once per row of data:
#
#        @pytest.mark.parametrize('n, expected', [(0, 0), (1, 1)])
#        def test_values(n, expected):      <- runs twice
#            assert fib(n) == expected
#
# 3. pytest.raises checks that code raises an exception:
#
#        with pytest.raises(ValueError):
#            fib(-1)
#
# The code under test (fib) is in the supplied section above. Rules:
#     fib(n) for n < 0 raises ValueError. fib(0) == 0, fib(1) == 1.
#     fib(n) == fib(n - 1) + fib(n - 2) for larger n.
#
''' + _JUDGE + r'''#
# Faults to catch: reject zero, accept negative input, wrong base case,
#                  subtract recursive terms, wrong recurrence.
#
# Work in two steps.
#
#   Step 1 (test_values)    -> wrong base case, subtract recursive terms,
#                              wrong recurrence, reject zero
#   Step 2 (test_negative)  -> accept negative input


# Step 1: known values. Include 0 and 1 (the base cases) and values that need
# the recurrence. Known values: fib(2) == 1, fib(3) == 2, fib(10) == 55,
# fib(50) == 12586269025.
@pytest.mark.parametrize('n, expected', [
    (0, 0),
    # TODO: add more (n, expected) rows.
])
def test_values(n, expected):
    assert fib(n) == expected


# Step 2: negative n raises ValueError.
@pytest.mark.parametrize('n', [-1])  # TODO: add one more negative number.
def test_negative(n):
    # TODO: with pytest.raises(ValueError): call fib(n).
    ...
''',

    2: r'''import pytest
from digits import list_to_decimal

# What you practise
# -----------------
# Writing one small test per rule, with @pytest.mark.parametrize for the
# data and pytest.raises for the errors:
#
#     @pytest.mark.parametrize('digits, expected', [([1, 2], 12)])
#     def test_decimal(digits, expected):
#         assert list_to_decimal(digits) == expected
#
#     with pytest.raises(TypeError):
#         list_to_decimal([True])
#
# The rules of list_to_decimal (the supplied code above):
#     list_to_decimal([0, 4, 2, 8])  -> 428   (leading zeroes are allowed)
#     list_to_decimal([])            -> 0
#     a digit that is not an int (also True/False) -> TypeError
#     an int outside 0..9 (-1, 10)   -> ValueError
#
''' + _JUDGE + r'''#
# Faults to catch: accept booleans, reject zero digit, accept ten,
#                  wrong place value, wrong empty result.
#
# Work in three steps.
#
#   Step 1 (test_decimal)  -> wrong place value, wrong empty result, reject zero digit
#   Step 2 (test_types)    -> accept booleans
#   Step 3 (test_range)    -> accept ten


# Step 1: valid lists. Include [], a list with 0, and digits in different
# places such as [1, 0, 2] -> 102.
@pytest.mark.parametrize('digits, expected', [
    ([9], 9),
    # TODO: add more (digits, expected) rows.
])
def test_decimal(digits, expected):
    assert list_to_decimal(digits) == expected


# Step 2: wrong types raise TypeError. bool is a subclass of int, so test
# True and False too.
@pytest.mark.parametrize('digit', [
    3.6,
    # TODO: add True, False and a str such as '4'.
])
def test_types(digit):
    with pytest.raises(TypeError):
        list_to_decimal([1, digit])


# Step 3: ints outside 0..9 raise ValueError. Test both sides: -1 and 10.
# TODO: write test_range with @pytest.mark.parametrize and pytest.raises(ValueError).
''',

    3: r'''import pytest
from printing import print_even_numbers

# What you practise
# -----------------
# The capsys fixture captures what the code prints. Add capsys as a parameter
# of the test, call the code, then read the output:
#
#     def test_output(capsys):
#         print_even_numbers([1, 2])
#         captured = capsys.readouterr()
#         assert captured.out == '2\n'        <- every print adds a newline
#
# The rules of print_even_numbers (the supplied code above): print each even
# number on its own line, in input order. Keep duplicates, 0, and negative
# numbers. Print nothing for [] or an all-odd list. Return None.
#
''' + _JUDGE + r'''#
# Faults to catch: print odd numbers, omit zero, omit negative numbers,
#                  omit newline, deduplicate output.
#
# There is one step: one parametrized test. Each row is a list and the exact
# text that it must print.


@pytest.mark.parametrize('numbers, expected', [
    ([1, 3], ''),
    # TODO: add rows for: 0 and other evens with odds between them
    #       ([0, 1, 2, 3, 4] -> '0\n2\n4\n'), negative numbers, duplicates ([2, 2]),
    #       and an empty list.
])
def test_output(numbers, expected, capsys):
    assert print_even_numbers(numbers) is None
    # TODO: captured = capsys.readouterr(), then assert captured.out == expected.
''',

    5: r'''import json
from ipaddress import IPv4Network

import pytest
from ips import IPRange, parse_ranges, get_ranges, filter_ranges

# What you practise
# -----------------
# 1. A fixture is setup code that a test asks for by name:
#
#        @pytest.fixture
#        def ranges(tmp_path):            <- tmp_path is pytest's temporary folder
#            path = tmp_path / 'ranges.json'
#            path.write_text(json.dumps(SAMPLE))
#            return get_ranges(path)
#
#        def test_parse(ranges):          <- pytest calls the fixture first
#            assert len(ranges) == 3
#
# 2. pytest.raises for each kind of bad input.
#
# The supplied code: parse_ranges(text) parses JSON into IPRange objects in
# input order; get_ranges(path) reads a file; filter_ranges(ranges,
# region=None, service=None) keeps ranges that match ALL given filters.
#
''' + _JUDGE + r'''#
# Faults to catch: swap region and service, skip the first range,
#                  invert region filter, invert service filter,
#                  combine filters with or.
#
# SUPPLIED: SAMPLE is ready-made test data in the AWS ip-ranges shape.
# Writing test data is not the skill of this exercise. Use it.
SAMPLE = {'prefixes': [
    {'ip_prefix': '10.0.0.0/24', 'region': 'west', 'service': 'EC2'},
    {'ip_prefix': '192.0.2.0/24', 'region': 'east', 'service': 'S3'},
    {'ip_prefix': '198.51.100.0/24', 'region': 'west', 'service': 'S3'},
]}

# Work in three steps.
#
#   Step 1 (fixture and parsing)  -> skip the first range, swap region and service
#   Step 2 (filters)              -> invert region filter, invert service filter,
#                                    combine filters with or
#   Step 3 (errors)               -> covers the error paths


# Step 1: write SAMPLE to a file in tmp_path and return get_ranges(path).
@pytest.fixture
def ranges(tmp_path):
    # TODO: path = tmp_path / 'ranges.json'; path.write_text(json.dumps(SAMPLE))
    # TODO: return get_ranges(path)
    ...


def test_parse(ranges):
    # TODO: assert len(ranges) == 3
    # TODO: assert ranges[0] == IPRange(IPv4Network('10.0.0.0/24'), 'west', 'EC2')
    ...


# Step 2: one assert per filter case. Expected results with SAMPLE:
#     filter_ranges(ranges)                           -> all 3
#     filter_ranges(ranges, region='west')            -> [ranges[0], ranges[2]]
#     filter_ranges(ranges, service='S3')             -> [ranges[1], ranges[2]]
#     filter_ranges(ranges, region='west', service='S3') -> [ranges[2]]
def test_filters(ranges):
    # TODO: assert each case above.
    ...


# Step 3: bad input raises. Use pytest.raises for each:
#     parse_ranges('broken')        -> ValueError (bad JSON)
#     parse_ranges('{}')            -> KeyError   (no 'prefixes')
#     an ip_prefix such as 'invalid' -> ValueError
def test_errors():
    # TODO: three with pytest.raises(...) blocks.
    ...
''',

    6: r'''from unittest.mock import patch

import pytest
from colors import gen_hex_color, HEX

# What you practise
# -----------------
# Mocking: replace a function with a fake while a test runs, so the result is
# predictable. gen_hex_color uses random.sample, imported into the colors
# module, so patch the name where the code looks it up: 'colors.sample'.
#
#     with patch('colors.sample', side_effect=[list('A1B2C3'), list('FEDCBA')]) as sample:
#         next(gen)  -> '#A1B2C3'     (1st call of sample returns list('A1B2C3'))
#         next(gen)  -> '#FEDCBA'     (2nd call returns list('FEDCBA'))
#
# side_effect=[...] gives one return value per call. The mock also records
# the calls:
#     sample.call_count                          -> 2
#     sample.assert_called_with('0123456789ABCDEF', 6)  -> fails if the last call differs
#
# The supplied code: gen_hex_color() is a generator that never stops. Each
# next() calls sample('0123456789ABCDEF', 6), joins the 6 characters
# unchanged, and puts '#' in front.
#
''' + _JUDGE + r'''#
# Faults to catch: missing hash prefix, wrong sample size, lowercase output,
#                  generator stops early, wrong character alphabet.
#
# There is one step.


@pytest.fixture
def gen():
    return gen_hex_color()


def test_colors(gen):
    with patch('colors.sample', side_effect=[list('A1B2C3'), list('FEDCBA')]) as sample:
        # TODO: assert next(gen) == '#A1B2C3'   (catches missing hash, lowercase output)
        # TODO: assert next(gen) == '#FEDCBA'   (catches generator stops early)
        # TODO: assert sample.call_count == 2
        # TODO: sample.assert_called_with('0123456789ABCDEF', 6)
        #       (catches wrong sample size and wrong character alphabet)
        ...
''',

    7: r'''import pytest
from account import Account

# What you practise
# -----------------
# Testing a class: create objects, call methods, and check the state. Write
# one small test per behaviour, so a failing test names the broken rule.
#
# The supplied Account class:
#     Account('Bob', 10)        owner 'Bob', starting amount 10 (default 0)
#     account.add_transaction(5)        a positive, negative or zero int
#     account.balance           starting amount + all transactions
#     len(account)              the number of transactions (not the amount)
#     account[0], account[:2], list(account)   the transactions
#     str(account)   -> 'Account of Bob with starting amount: 10'
#     repr(account)  -> "Account('Bob', 10)"
#     ==, <          compare the CURRENT balance
#     a non-int amount (also True) -> TypeError with 'integer' in the message
#
''' + _JUDGE + r'''#
# Faults to catch: ignore starting amount, subtract transactions,
#     reject zero transactions, accept booleans as amounts,
#     count starting amount as a transaction, compare initial amounts,
#     less than includes equality.
#
# Work in four steps.
#
#   Step 1 (test_initial_and_representation)
#   Step 2 (test_transactions)       -> ignore starting amount, subtract transactions,
#                                       reject zero transactions,
#                                       count starting amount as a transaction
#   Step 3 (test_invalid_amounts)    -> accept booleans as amounts
#   Step 4 (test_comparisons)        -> compare initial amounts,
#                                       less than includes equality


# Step 1: a new account.
def test_initial_and_representation():
    account = Account('Bob', 10)
    assert account.owner == 'Bob'
    # TODO: check amount, balance (10), len (0), str() and repr() exactly.
    # TODO: Account('Ada') has balance 0.


# Step 2: transactions. Use a starting amount that is not 0, and add
# 5, -3 and 0:
#     balance -> 12, len -> 3, list(account) -> [5, -3, 0], account[-1] -> 0
def test_transactions():
    account = Account('Ada', 10)
    # TODO: add the three transactions, then assert the values above.
    # TODO: account[3] raises IndexError (use pytest.raises).


# Step 3: bad amounts raise TypeError, in the constructor AND in
# add_transaction. Include True.
@pytest.mark.parametrize('value', [
    1.5,
    # TODO: add True, '2' and None.
])
def test_invalid_amounts(value):
    with pytest.raises(TypeError, match='integer'):
        Account('Ada', value)
    # TODO: the same check for Account('Ada').add_transaction(value).


# Step 4: comparisons use the CURRENT balance, not the starting amount.
#     first = Account('A', 3); first.add_transaction(5)   -> balance 8
#     second = Account('B', 8)                             -> balance 8
#     first == second -> True, and first < second -> False (equal is not less)
def test_comparisons():
    # TODO: build the two accounts above and assert == and not <.
    # TODO: add 1 to second, then assert first < second.
    ...
''',

    9: r'''from unittest.mock import patch

import pytest
from guessing import GuessingGame

# What you practise
# -----------------
# 1. Mocking input(): play() asks the user with input(). Patch it so the test
#    "types" the answers. side_effect gives one answer per call:
#
#        with patch('builtins.input', side_effect=['x', '9', '10']) as read:
#            result = game.play()
#        read.call_count  -> how many times play() asked
#
# 2. capsys reads what play() printed:
#        capsys.readouterr().out  -> 'Enter a number\nToo low\nYou win!\n'
#
# The supplied GuessingGame:
#     GuessingGame(secret, max_guesses=5): secret is an int from 1 to 20,
#         max_guesses a positive int (bool is rejected). Else ValueError with
#         'secret must be an integer from 1 to 20' or
#         'max_guesses must be a positive integer'.
#     play(): at most max_guesses answers. Not a number -> 'Enter a number'
#         (uses an attempt). Too small -> 'Too low'. Too big -> 'Too high'.
#         Right -> 'You win!' and return True at once. No attempts left ->
#         'You lose! The number was N' and return False.
#
''' + _JUDGE + r'''#
# Faults to catch: reject lower endpoint, reject upper endpoint,
#     accept boolean secret, omit last attempt, swap high and low,
#     wrong winning result, wrong losing result.
#
# Work in four steps.
#
#   Step 1 (validation)       -> accept boolean secret
#   Step 2 (test_endpoints)   -> reject lower endpoint, reject upper endpoint
#   Step 3 (win on last try)  -> omit last attempt, swap high and low, wrong winning result
#   Step 4 (test_loss)        -> wrong losing result


# Step 1: bad secrets raise ValueError. Include 0, 21 and True.
@pytest.mark.parametrize('secret', [
    0,
    # TODO: add 21, True and '2'.
])
def test_secret_validation(secret):
    with pytest.raises(ValueError, match='secret must be an integer from 1 to 20'):
        GuessingGame(secret)


# Step 2: 1 and 20 are valid secrets, and a right first guess wins.
@pytest.mark.parametrize('secret', [1, 20])
def test_endpoints(secret, capsys):
    game = GuessingGame(secret)
    with patch('builtins.input', return_value=str(secret)):
        # TODO: assert game.play() is True
        ...
    # TODO: assert capsys.readouterr().out == 'You win!\n'


# Step 3: secret 10, 4 attempts, answers 'x', '9', '11', '10'.
#     printed: 'Enter a number\nToo low\nToo high\nYou win!\n'
#     play() -> True, and input was called 4 times.
def test_win_on_last_guess(capsys):
    # TODO: patch builtins.input with side_effect=[...] as read, play, and assert.
    ...


# Step 4: secret 10, 2 attempts, answers '1', '20'.
#     printed: 'Too low\nToo high\nYou lose! The number was 10\n'
#     play() -> False
def test_loss(capsys):
    # TODO: patch input, play, and assert the result and the output.
    ...
''',

    10: r'''import sqlite3

import pytest
from movies import MovieDB

# What you practise
# -----------------
# A yield fixture has setup code before yield and teardown code after it.
# pytest runs the teardown after the test, even when the test fails:
#
#     @pytest.fixture
#     def db():
#         database = MovieDB()      <- setup
#         database.init()
#         yield database            <- the test runs here and gets database
#         database.drop_table()     <- teardown
#         database.close()
#
# tmp_path gives a temporary folder for a file database.
#
# The supplied MovieDB (SQLite). init() adds 3 movies:
#     ('Alien', 1979, 8.5), ('Arrival', 2016, 7.9), ('Moon', 2009, 7.8)
# query(title=None, min_score=0, year=None) -> list of (title, year, score),
#     sorted by title. title matches a part of the title, any case.
#     min_score is inclusive (score >= min_score). All filters combine.
# add(title, year, score) inserts and saves. A duplicate title raises
#     sqlite3.IntegrityError.
# delete(title) removes an exact title, saves, and returns 1 or 0.
#
''' + _JUDGE + r'''#
# Faults to catch: exclude exact score threshold, wrong year filter,
#     exact title instead of substring, reverse title ordering,
#     wrong deletion count, omit insert commit, omit delete commit.
#
# Work in four steps.
#
#   Step 1 (the db fixture)
#   Step 2 (test_query)                -> score threshold, year filter,
#                                         substring title, title ordering
#   Step 3 (test_add_and_delete)       -> wrong deletion count
#   Step 4 (test_persistence)          -> omit insert commit, omit delete commit
#                                         (only a NEW connection to the same
#                                          file shows a missing commit)


# Step 1: the yield fixture.
@pytest.fixture
def db():
    # TODO: database = MovieDB(); database.init(); yield database
    # TODO: after the yield: database.drop_table(); database.close()
    ...


# Step 2: query results. Expected with the 3 movies:
#     db.query()               -> all 3, sorted: Alien, Arrival, Moon
#     db.query(title='ali')    -> [('Alien', 1979, 8.5)]
#     db.query(min_score=7.9)  -> Alien and Arrival (7.9 is included)
#     db.query(year=2009)      -> [('Moon', 2009, 7.8)]
def test_query(db):
    # TODO: one assert per case above.
    ...


# Step 3: add a movie, a duplicate (IntegrityError), delete it (returns 1),
# and delete a missing title (returns 0).
def test_add_and_delete(db):
    # TODO
    ...


# Step 4: a file database. Write with one MovieDB, close it, and read with a
# NEW MovieDB on the same path:
#     path = tmp_path / 'movies.db'
#     first = MovieDB(path); first.init(); first.add('Up', 2009, 8.3); first.close()
#     second = MovieDB(path); second.query(title='Up') -> [('Up', 2009, 8.3)]
# Then delete 'Up' with second, close it, and check with a third MovieDB that
# 'Up' is gone.
def test_persistence(tmp_path):
    # TODO
    ...
''',
}

HINTS = {
    1: ['Concept: @pytest.mark.parametrize("n, expected", [...]) runs one test per row. Each fault changes one rule, so give a row for each rule: the two base cases and values that need the recurrence.',
        'fib(0) == 0 catches "reject zero". fib(1) == 1 and fib(2) == 1 catch "wrong base case". fib(10) == 55 catches the recurrence faults.',
        'For negative input: with pytest.raises(ValueError): fib(-1).'],
    2: ['Concept: one parametrized test per rule. Valid lists go in one test, wrong types in another, and out-of-range digits in a third.',
        '[1, 0, 2] -> 102 catches "reject zero digit" and "wrong place value". [] -> 0 catches "wrong empty result".',
        'True is an int subclass, so [1, True] must raise TypeError. [10] must raise ValueError (catches "accept ten").'],
    3: ['Concept: capsys captures printed text. Call the function, then compare capsys.readouterr().out with the exact text, newlines included.',
        'One list can catch several faults: [0, 1, 2, 3, 4] must print "0\\n2\\n4\\n". Add [-4, -3, -2] -> "-4\\n-2\\n" and [2, 2] -> "2\\n2\\n".',
        'Also assert that the function returns None, and test [] and [1, 3] (no output).'],
    5: ['Concept: a fixture prepares data for a test. Write SAMPLE to tmp_path / "ranges.json" with json.dumps, then return get_ranges(path).',
        'Assert ranges[0] == IPRange(IPv4Network("10.0.0.0/24"), "west", "EC2") and len(ranges) == 3. Then test each filter alone and both filters together.',
        'Error paths: parse_ranges("broken") raises ValueError, parse_ranges("{}") raises KeyError, and an invalid ip_prefix raises ValueError.'],
    6: ["Concept: patch('colors.sample', side_effect=[...]) replaces sample in the colors module during the with block. Each call returns the next item of side_effect.",
        "Call next(gen) twice and compare with '#A1B2C3' and '#FEDCBA'. Two values catch a generator that stops early.",
        "Check the arguments: sample.assert_called_with('0123456789ABCDEF', 6) catches a wrong alphabet and a wrong sample size."],
    7: ['Concept: test one behaviour per test. Use a starting amount that is not 0, so faults that ignore it change the balance.',
        'Add 5, -3 and 0 to an account that starts at 10: balance 12 and len 3. These values catch subtracting, ignoring the start, rejecting 0, and counting the start as a transaction.',
        'Comparisons use the current balance: Account("A", 3) plus 5 equals Account("B", 8), and is not less than it. True must raise TypeError in both places.'],
    9: ["Concept: patch('builtins.input', side_effect=[...]) answers each input() call in turn. capsys.readouterr().out returns everything that play() printed.",
        'Secrets 1 and 20 must be valid (they catch the endpoint faults). True must raise ValueError.',
        'Win on the LAST allowed attempt (catches "omit last attempt"), compare the exact printed lines (catches swapped hints), and assert the True and False results.'],
    10: ['Concept: a yield fixture: setup, then yield db, then teardown (drop_table and close). pytest runs the teardown after each test.',
         'Test each query filter at its edge: min_score=7.9 must include Arrival (7.9), title="ali" must find Alien (a part of the title, any case), and the order must be by title.',
         'A missing commit is only visible from a new connection. Use a file in tmp_path: add with one MovieDB, close it, then query with a new MovieDB on the same path. Do the same for delete.'],
}
