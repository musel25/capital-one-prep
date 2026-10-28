"""Keep the original testing tasks visible alongside their supplied targets."""

STARTS = {
    1: 'Our first Test Bite!',
    2: 'Our 4th test Bite.',
    3: 'In this Bite you test a function',
    4: 'In our second Test Bite',
    5: 'Another Test Bite,',
    6: 'In this Bite you will mock out',
    7: 'In our third Test Bite',
    8: 'In this Bite we will write tests',
    9: 'In this Bite you test a simple',
    10: 'Time for fixtures,',
}


def original_description(spec):
    text = spec['page']['description']
    text = STARTS[spec['number']] + text.split(STARTS[spec['number']], 1)[1]
    text = text.rsplit(' Topics ', 1)[0]
    # This word is the source page's code-tab label, outside its task paragraph.
    if spec['number'] == 1:
        text = text.removesuffix(' fibonacci')
    for transition in ('Why fixtures?', 'In this Bite ', 'At the end of the fixture',
                       'Apart from this setup', 'As with all our test Bites',
                       'Good luck', 'Have fun', 'Some examples:'):
        text = text.replace(' ' + transition, '\n\n' + transition)
    return text.strip()


EXAMPLES = {
    1: [('print(fib(0), fib(1), fib(10), fib(50))', '0 1 55 12586269025')],
    2: [('print(list_to_decimal([0, 4, 2, 8]))\nprint(list_to_decimal([]))', '428\n0')],
    3: [('result = print_even_numbers([0, 1, 2, -4, 2])\nprint("Return value:", result)', '0\n2\n-4\n2\nReturn value: None')],
    4: [('print([fizzbuzz(n) for n in [1, 3, 5, 15]])', "[1, 'Fizz', 'Buzz', 'FizzBuzz']")],
    5: [('text = \'{"prefixes": [{"ip_prefix": "10.0.0.0/24", "region": "west", "service": "EC2"}]}\'\nranges = parse_ranges(text)\nprint(ranges)\nprint(filter_ranges(ranges, region="east"))', "[IPRange(network=IPv4Network('10.0.0.0/24'), region='west', service='EC2')]\n[]")],
    6: [('from unittest.mock import patch\nwith patch("colors.sample", return_value=list("A1B2C3")):\n    print(next(gen_hex_color()))', '#A1B2C3')],
    7: [('account = Account("Ada", 10)\naccount.add_transaction(5)\naccount.add_transaction(-3)\nprint(account.balance, len(account), list(account))', '12 2 [5, -3]')],
    8: [('from datetime import date\nsigns = get_signs()\nprint(get_sign_with_most_famous_people(signs))\nprint(signs_are_mutually_compatible(signs, "Aries", "Leo"))\nprint(get_sign_by_date(signs, date(2024, 1, 1)))', 'Leo\nTrue\nCapricorn')],
    9: [('from unittest.mock import patch\nwith patch("builtins.input", side_effect=["9", "10"]):\n    result = GuessingGame(10, max_guesses=2).play()\nprint("Return value:", result)', 'Too low\nYou win!\nReturn value: True')],
    10: [('db = MovieDB()\ndb.init()\nprint(db.query(min_score=8))\nprint(db.delete("Moon"))\nprint(db.delete("Moon"))\ndb.close()', "[('Alien', 1979, 8.5)]\n1\n0")],
}

RUNNER_HELP = ('The offline runner supports `pytest.raises` with `match`, '
    '`pytest.mark.parametrize`, function and yield fixtures, numeric `pytest.approx`, '
    '`pytest.fail`, `capsys`, `capfd`, `monkeypatch`, and `tmp_path`. '
    '`unittest.mock.patch` also works. Use top-level test functions and function-scoped '
    'fixtures. Async tests, pytest classes with setup hooks, plugins, skip/xfail, and '
    'advanced fixture scopes are not supported.\n\n'
    'This course measures statement coverage with Python tracing and checks explicit '
    'faulty variants. It does not run pytest-cov or mutatest. '
    '`SURVIVED` names a fault that your tests did not detect.')
