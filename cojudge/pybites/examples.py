"""Concrete calls and the few input guarantees absent from the public tasks."""

ASSUMPTIONS = {
    1: ['Use naive datetimes. Compare expiry with the supplied `NOW`; equality is not expired.'],
    2: ['Names are nonempty strings of ASCII letters.'],
    3: ['Counts are nonnegative integers.'],
    4: ['Done IDs belong to the supplied catalog. Empty containers are valid inputs.'],
    5: ['Scores are finite integers or floats, including negative values.'],
    6: ['Each assigned name is new. Birthday values are `datetime.date` objects.'],
    8: ['Names have no newline characters.'],
    10: ['Files are valid INI files with a `[tox]` section. Interpreter values are single names; do not expand brace expressions.'],
    12: ['Use the supplied domain validation rule. URLs use HTTP or HTTPS; emails have one `@` and nonempty parts.'],
    13: ['Amounts are integers; reject `bool` values. Compare accounts by balance.'],
    14: ['Use integer amounts and non-nested context blocks. Check the final balance on every block exit; keep exceptions visible.'],
    16: ['Matrices are nonempty, rectangular, numeric lists with compatible dimensions.'],
    17: ['Transactions contain a User and integer points. Fans are distinct giver names.'],
    18: ['The initial score is a nonnegative integer. A `bool` is not a valid score.'],
    19: ['Numbers are finite integers or floats; `bool` values are invalid.'],
    20: ['Counts are nonnegative integers. Add each person once. Pair at most `min(count, len(rankings) // 2)` people pairs.'],
    21: ['Read cached HTML files through the supplied `Web` and `Soup` classes. Tables contain one header row and valid numeric cells.'],
    22: ['Valid hands contain 13 distinct cards. The second source example has 14 cards; use `S:9 H:KJT9 D:432 C:AJ742` for that example.'],
}

# Inputs are Python snippets. Outputs show printed text and/or the final expression.
EXAMPLES = {
    1: [
        ('from datetime import timedelta\nPromo("Autumn", NOW - timedelta(seconds=1)).expired', 'True', 'A time before NOW has expired.'),
        ('Promo("Autumn", NOW).expired', 'False', 'Expiry at NOW is still valid.'),
    ],
    2: [
        ('user = User("ada", "lovelace")\n(user.get_full_name, user.username, str(user))', "('Ada Lovelace', 'alovelac', 'Ada Lovelace (alovelac)')", 'The username uses at most seven surname letters.'),
        ('repr(User("ada", "lovelace"))', '\'User("ada", "lovelace")\'', 'The representation preserves the supplied case.'),
    ],
    3: [
        ('Car("Toyota", "Corolla", 4, 4).description()', "'Toyota Corolla with 4 wheels'", 'Car inherits the vehicle description.'),
        ('Motorbike("Yamaha", "R3", 2, 321).rev_engine()', "'Yamaha R3 with 2 wheels goes Vroom vroom!'", 'The engine message extends the parent description.'),
    ],
    4: [
        ('promo = Promo({1: "Properties", 2: "Classes"}, {1})\npromo.new_bite()', '2', 'Only bite 2 is available.'),
        ('promo = Promo({}, set())\ntry:\n    promo.new_bite()\nexcept NoBitesAvailable:\n    print("No bites available")', 'No bites available', 'An empty catalog raises the supplied exception.'),
    ],
    5: [
        ('record = RecordScore()\n[record(score) for score in [10, 8, 15, 15]]', '[10, 10, 15, 15]', 'Each call returns the highest score so far.'),
        ('record = RecordScore()\n[record(score) for score in [-8, -3, -10]]', '[-8, -3, -3]', 'The first score sets the record even when negative.'),
    ],
    6: [
        ('from datetime import date\nbirthdays = BirthdayDict()\nbirthdays["Ada"] = date(1815, 12, 10)\nbirthdays["Bob"] = date(1990, 12, 10)', 'Hey Bob, there are more people with your birthday!', 'Only month and day determine a shared birthday.'),
    ],
    7: [
        ('Color.hex2rgb("#ff8000")', '(255, 128, 0)', 'Convert each hexadecimal pair to one channel.'),
        ('Color.rgb2hex((0, 15, 255))', "'#000fff'", 'Each channel uses two lowercase hexadecimal digits.'),
        ('(str(Color("RED")), str(Color("unknown")))', "('(255, 0, 0)', 'Unknown')", 'Color names are case insensitive.'),
    ],
    8: [
        ('Animal("lion")\nAnimal("red panda")\nAnimal.zoo()', "'10001. Lion\\n10002. Red Panda'", 'A new zoo assigns consecutive IDs in creation order.'),
    ],
    9: [
        ('Bite(2, "fizz BUZZ")', "Bite(number=2, title='Fizz buzz', level='Beginner')", 'The title is capitalized and the level has a default.'),
        ('[bite.number for bite in sorted([Bite(3, "classes"), Bite(1, "properties")])]', '[1, 3]', 'The dataclass compares number first.'),
    ],
    10: [
        ('from pathlib import Path\nfrom tempfile import TemporaryDirectory\nwith TemporaryDirectory() as folder:\n    path = Path(folder) / "tox.ini"\n    path.write_text("[tox]\\nenvlist = py311, py312\\n[testenv]\\nbasepython = python3.11\\n")\n    parser = ToxIniParser(path)\n    result = (parser.number_of_sections, parser.environments, parser.base_python_versions)\nresult', "(2, ['py311', 'py312'], ['python3.11'])", 'Read the section count and interpreter lists from a local file.'),
    ],
    11: [
        ('[str(cls()) for cls in [Person, Father, Mother, Child]]', "['I am a person', 'I am a person and cool daddy', 'I am a person and awesome mom', 'I am the coolest kid']", 'Each class supplies its specified string.'),
        ('[cls.__name__ for cls in Child.__mro__]', "['Child', 'Father', 'Mother', 'Person', 'object']", 'Python searches the parents in this method resolution order.'),
    ],
    12: [
        ('str(Domain.parse_url("https://pybit.es/articles/"))', "'pybit.es'", 'The constructor extracts the network location.'),
        ('str(Domain.parse_email("ada@example.com"))', "'example.com'", 'The email constructor extracts the text after @.'),
    ],
    13: [
        ('account = Account("Ada", 100)\naccount + 25\naccount - 10\n(account.balance, len(account), list(account), str(account))', "(115, 2, [25, -10], 'Ada account - balance: 115')", 'Transactions affect the balance and remain available in order.'),
    ],
    14: [
        ('account = Account()\naccount + 10\nwith account:\n    account - 15\naccount.balance', '10', 'A negative final balance rolls back all transactions in the block.'),
        ('account = Account()\nwith account:\n    account - 5\n    account + 8\naccount.balance', '3', 'A temporary negative balance is allowed if the final balance is nonnegative.'),
    ],
    15: [
        ('challenge = BlogChallenge(7, "Classes", [12, 18])\n(challenge.pretty_title, challenge.verify(18), challenge.verify(20))', "('PCC7 - Classes', True, False)", 'A blog challenge checks merged pull request numbers.'),
        ('challenge = BiteChallenge(4, "Add", 7)\n(challenge.pretty_title, challenge.verify(7))', "('Bite 4. Add', True)", 'A bite checks equality with the expected result.'),
    ],
    16: [
        ('left = Matrix([[1, 2], [3, 4]])\nright = Matrix([[5], [6]])\n(left @ right).values', '[[17], [39]]', 'Multiply each left row by the right column.'),
        ('([[2, 3]] @ Matrix([[4], [5]])).values', '[[23]]', 'A plain list can be the left operand.'),
    ],
    17: [
        ('ada = User("Ada")\nbob = User("Bob")\nada + Transaction(bob, 5)\nada + Transaction(bob, -2)\n(ada.points, ada.karma, ada.fans, str(ada))', "([5, -2], 3, 1, 'Ada has a karma of 3 and 1 fan')", 'Two transactions from one giver still count as one fan.'),
    ],
    18: [
        ('ninja = NinjaBelt()\nninja.score = 10', 'Congrats, you earned 10 points obtaining the PyBites Ninja White Belt', 'Crossing a belt threshold prints the award.'),
        ('ninja = NinjaBelt(10)\ntry:\n    ninja.score = 5\nexcept ValueError as error:\n    print(f"ValueError: {error}")', 'ValueError: Cannot lower score', 'A lower score is rejected.'),
    ],
    19: [
        ('numbers = IntList([1, 3])\nnumbers.append([5, 7])\n(list(numbers), numbers.mean, numbers.median)', '([1, 3, 5, 7], 4, 4.0)', 'Appending a list adds its values to the numeric list.'),
        ('list(IntList([1.0]) + [2, 3])', '[1.0, 2, 3]', 'Addition accepts both integers and floats.'),
    ],
    20: [
        ('rankings = Rankings()\nfor name, bites in [("Ada", 20), ("Bob", 10), ("Cy", 30), ("Dee", 5)]:\n    rankings.add(Ninja(name, bites))\n[(str(high), str(low)) for high, low in rankings.pair_up()]', "[('[30] Cy', '[5] Dee'), ('[20] Ada', '[10] Bob')]", 'Pair the highest and lowest scores without reusing a person.'),
    ],
    21: [
        ('table = "<table><tr><th>Candidate</th><th>Average</th><th>Delegates</th><th>Contributions</th><th>Coverage</th></tr><tr><td>Ada</td><td>40%</td><td>12</td><td>$5</td><td>8</td></tr></table>"\nsite = NYTimes(Web("https://example.invalid", File("cached.html")))\nsite.parse_rows(table)', "[LeaderBoard(Candidate='Ada', Average='40%', Delegates=12, Contributions='$5', Coverage=8)]", 'Convert table cells into the supplied typed record.'),
    ],
    22: [
        ('text = "S:AK8 H:JT94 D:A2 C:KQ74"\ncards = [Card(Suit[part[0]], Rank[rank]) for part in text.split() for rank in part[2:]]\nhand = BridgeHand(cards)\n(str(hand), hand.hcp, hand.ssp, hand.total_points, hand.ltc)', "('S:AK8 H:JT94 D:A2 C:KQ74', 17, 1, 18, 6)", 'This hand has one doubleton and six losing tricks.'),
    ],
}


def examples(number):
    return [dict(input=code, output=output, explanation=explanation)
            for code, output, explanation in EXAMPLES[number]]
