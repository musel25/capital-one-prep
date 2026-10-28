"""Examples use the public functions, not the internal judge selector."""

ASSUMPTIONS = {
    1: ['Scores and owner counts are nonnegative integers.'],
    2: ['The maximum length is a nonnegative integer.'],
    3: ['Input has `last_name,first_name,country_code` headers and valid CSV records.'],
    4: ['XML is well formed and has no namespaces. Strip category text and ignore empty categories. Ties keep first appearance order.'],
    5: ['Paths use the form `NN/user`. Exclude `bbelderbos`, `juliansequeira`, and `pybites` from both counts. Ties keep first appearance order.'],
    6: ['Dictionary keys are valid namedtuple field names. Encode non-JSON values with `str`.'],
    7: ['Split on whitespace, then remove non-alphanumeric characters. Ties keep first appearance order.'],
    8: ['Present CSV numbers are valid. Calculate means from nonempty movie lists.'],
    9: ['CSV records contain all four fields and belong to one season. Episode keys stay strings.'],
    10: ['Use the supplied BeautifulSoup interface. HTML is well formed. Dates use `YYYY-MM-DD`; the fourth cell contains the holiday name.'],
    11: ['Aliases are nonempty and have word characters at both ends. Match whole words and count blank physical lines.'],
}

EXAMPLES = {
    1: [
        ('get_total_points({"yellow": BeltStats(50, 3), "orange": BeltStats(100, 2)})', '350', 'Three yellow belts and two orange belts earn 150 + 200 points.'),
        ('get_total_points({})', '0', 'An empty dictionary earns no points.'),
    ],
    2: [
        ('queue = my_queue(3)\nqueue.extend([1, 2, 3, 4, 5])\nlist(queue)', '[3, 4, 5]', 'Only the latest three items remain.'),
        ('queue = my_queue(0)\nqueue.append("item")\nlist(queue)', '[]', 'A maximum length of zero retains nothing.'),
    ],
    3: [
        ('data = "last_name,first_name,country_code\\nLovelace,Ada,GB\\nHopper,Grace,US\\nTuring,Alan,GB\\n"\ndict(group_names_by_country(data))', "{'GB': ['Ada Lovelace', 'Alan Turing'], 'US': ['Grace Hopper']}", 'Group full names under the country code.'),
    ],
    4: [
        ('xml = "<rss><category>Python</category><category>Flask</category><category>Python</category></rss>"\nget_top_tags(xml, n=2)', "[('Python', 2), ('Flask', 1)]", 'Rank category counts from highest to lowest.'),
    ],
    5: [
        ('diehard_pybites(["01/ada", "02/bob", "01/ada", "02/pybites"])', "Stats(user='ada', challenge=('01', 2))", 'Exclude Pybites accounts before counting users and challenges.'),
        ('diehard_pybites([])', 'Stats(user=None, challenge=(None, 0))', 'No eligible paths produce empty statistics.'),
    ],
    6: [
        ('record = dict2nt({"name": "Ada", "score": 7})\n(record.name, record.score, record._fields)', "('Ada', 7, ('name', 'score'))", 'Dictionary order becomes namedtuple field order.'),
        ('nt2json(dict2nt({"name": "Ada", "score": 7}))', '\'{"name": "Ada", "score": 7}\'', 'Namedtuple fields become JSON object keys.'),
    ],
    7: [
        ('get_most_common_word("The owl, the OWL and wizard.", {"the", "and"})', "('owl', 2)", 'Remove punctuation and stopwords before counting.'),
        ('get_most_common_word("the and", {"the", "and"})', '(None, 0)', 'Return an empty result if every word is excluded.'),
    ],
    8: [
        ('calc_mean_score([Movie("A", 2000, 8.0), Movie("B", 2001, 7.5)])', '7.8', 'Round the average to one decimal place.'),
        ('directors = {"Ada": [Movie("A", 2000, 8.0)] * 4, "Bob": [Movie("B", 2001, 9.0)] * 3}\nget_average_scores(directors)', "[('Ada', 8.0)]", 'A director needs at least four movies.'),
    ],
    9: [
        ('data = "Season,Episode,Character,Line\\n1,1,Cartman,Hello there\\n1,1,Cartman,Again\\n1,2,Stan,Hi\\n"\ndict(get_num_words_spoken_by_character_per_episode(data))', "{'Cartman': Counter({'1': 3}), 'Stan': Counter({'2': 1})}", 'Add dialogue word counts for each character and episode.'),
    ],
    10: [
        ('html = \'<table class="list-table"><tr><td><time datetime="2026-01-01"></time></td><td>Thursday</td><td>US</td><td> New Year </td></tr></table>\'\ndict(get_us_bank_holidays(html))', "{'01': ['New Year']}", 'Group the stripped holiday name under its two-digit month.'),
        ('dict(get_us_bank_holidays("<p>No table</p>"))', '{}', 'A missing holiday table produces an empty mapping.'),
    ],
    11: [
        ('make_character_index("Grandma met Red.\\n\\nGRANNY waved.\\nA redwood grew.", [("Grandmother", "Grandma", "Granny"), "Red"])', "{'Grandmother': [1, 3], 'Red': [1]}", 'Aliases share one key; blank lines count and redwood does not match Red.'),
    ],
}


def examples(number):
    return [dict(input=code, output=output, explanation=explanation)
            for code, output, explanation in EXAMPLES[number]]
