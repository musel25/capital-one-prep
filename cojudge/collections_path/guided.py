"""Guided starters (the Pybites OOP bite 15 pattern) for the selected exercises.

Each entry keeps the original starter up to MARKER (imports, data and supplied
helpers) and replaces the rest with a short concept explanation, steps mapped
to the tests, and TODO comments with exact input and output examples. Tests
and references do not change.
"""

GUIDED = {
    1: ('def get_total_points', r'''# What you practise
# -----------------
# A namedtuple is a tuple whose items also have names. You read a field
# with a dot instead of an index:
#
#     belt = BeltStats(score=50, ninjas=11)
#     belt.score   -> 50        (same as belt[0])
#     belt.ninjas  -> 11        (same as belt[1])
#
# There is one step. Every test calls get_total_points.


# Points for one belt = belt.score * belt.ninjas. Add the points of all belts.
#
#     get_total_points()                              -> 2675
#         yellow 50*11 + orange 100*7 + green 175*1 + blue 250*5
#     get_total_points({'new': BeltStats(7, 9)})      -> 63
#     get_total_points({})                            -> 0
#
# Do not use the belt names: the tests add new belts such as 'brown'.
def get_total_points(belts=ninja_belts):
    """Return the sum of score * ninjas over all belts, as an int."""
    # TODO: loop over belts.values() (the BeltStats, not the names).
    # TODO: add up belt.score * belt.ninjas and return the total.
    ...
'''),

    2: ('def my_queue', r'''# What you practise
# -----------------
# collections.deque is a list-like queue that is fast at both ends. Give it
# maxlen and it never grows past that size: when it is full, append() drops
# the OLDEST item from the left.
#
#     q = deque(maxlen=2)
#     q.append(1); q.append(2); q.append(3)
#     list(q)  -> [2, 3]        (1 was dropped)
#
# There is one step. Every test calls my_queue.


# Return a NEW, empty deque that keeps at most n items.
#
#     q = my_queue()      -> deque([], maxlen=5)
#     q = my_queue(0)     -> deque([], maxlen=0)   (keeps nothing)
#
# Each call returns its own deque: two queues never share items.
def my_queue(n=5):
    """Return an empty collections.deque with maxlen n."""
    # TODO: return deque(maxlen=n).
    ...
'''),

    3: ('def group_names_by_country', r'''# What you practise
# -----------------
# defaultdict(list) is a dict that creates a missing value for you. Read or
# append to a new key, and it first stores an empty list there:
#
#     groups = defaultdict(list)
#     groups['ID'].append('Sula Wasielewski')   <- no KeyError for a new key
#     groups['ZZ']                              -> []
#
# There is one step. Every test calls group_names_by_country.


# Group full names ("first last") by country code.
#
#     _rows(data) gives one dict per person, for example:
#         {'last_name': 'Watsham', 'first_name': 'Husain', 'country_code': 'ID'}
#
#     groups = group_names_by_country()
#     groups['ID']  -> ['Husain Watsham', 'Sula Wasielewski']
#     groups['BR']  -> ['Alphonso Harrold']
#
# Keep duplicates: the same person twice gives the name twice.
def group_names_by_country(data=data):
    """Return a defaultdict(list): country code -> list of 'first last' names."""
    # TODO: groups = defaultdict(list)  (a new one on every call)
    # TODO: for row in _rows(data): append row['first_name'] + ' ' + row['last_name']
    #       to groups[row['country_code']].
    # TODO: return groups (the defaultdict itself, not dict(groups)).
    ...
'''),

    5: ('def gen_files', r'''# What you practise
# -----------------
# 1. A generator function uses yield instead of return. It hands out one
#    value at a time, and a for loop asks for the next one:
#
#        def count_up():
#            yield 1
#            yield 2
#        list(count_up())  -> [1, 2]
#
# 2. collections.Counter counts things. counter[key] += 1 works for a new
#    key, and most_common(1) gives the top pair: [(key, count)]. On a tie,
#    the key that was counted FIRST wins.
#
# Work in two steps. The tests run top to bottom. Submit also runs the
# edge-case tests.
#
#   Step 1 (gen_files)        -> test_generator_and_local_file
#   Step 2 (diehard_pybites)  -> test_public_example and the other tests


# Step 1: yield each nonblank line of a text file, without spaces or newline.
#
#     file content: ' 01/ana  \n\n02/bob\n'
#     list(gen_files(path))  -> ['01/ana', '02/bob']   (blank line skipped)
def gen_files(tempfile):
    """Yield the stripped, nonblank lines of the file at path tempfile."""
    # TODO: open the file (encoding='utf-8') in a with block.
    # TODO: for each line: if line.strip() is not empty, yield line.strip().
    ...


# Step 2: each path is '<challenge>/<user>', for example '25/clamytoe'.
# Skip users in EXCLUDED. Count the users and the challenges separately.
#
#     diehard_pybites()  -> Stats(user='santiagobenitez', challenge=('25', 2))
#         santiagobenitez has 3 paths (the most); challenge '25' appears 2
#         times without the excluded user bbelderbos.
#     diehard_pybites(['09/zoe', '01/ana'])  -> Stats('zoe', ('09', 1))   (tie: first seen)
#     diehard_pybites([])                    -> Stats(None, (None, 0))
#
# files can be a one-time iterator, so loop over it only once.
def diehard_pybites(files=FILES):
    """Return Stats(top user, (top challenge, its count))."""
    # TODO: users, challenges = Counter(), Counter()
    # TODO: for path in files: challenge, user = path.strip().split('/')
    #       skip the user if it is in EXCLUDED; else add 1 to both counters.
    # TODO: top user = users.most_common(1)[0][0]       (None if users is empty)
    #       top challenge = challenges.most_common(1)[0] (a (name, count) pair,
    #                                                    or (None, 0) if empty)
    # TODO: return Stats(top user, top challenge).
    ...
'''),

    7: ('def get_most_common_word', r'''# What you practise
# -----------------
# collections.Counter counts things. counter[word] += 1 works for a new
# word, and most_common(1) returns the top pair in a list:
#
#     counts = Counter(['owl', 'cat', 'owl'])
#     counts.most_common(1)  -> [('owl', 2)]
#
# On a tie, the word that was counted FIRST wins.
#
# There is one step. Every test calls get_most_common_word.


# Count the words of text, ignoring case, punctuation and stopwords.
#
#     get_most_common_word()                        -> ('wizard', 2)
#         'The wizard met the owl. The wizard waved.'  ('the' is a stopword)
#     get_most_common_word('Owl, OWL! owl?', [])    -> ('owl', 3)
#     get_most_common_word('THE 42 42', ['The'])    -> ('42', 2)
#     get_most_common_word('', [])                  -> (None, 0)
#
# Per token: lowercase it, then _clean it ('owl,' -> 'owl'). Skip a token
# that is empty after _clean, and skip stopwords (compare them in lowercase).
# Do not change the stopwords argument.
def get_most_common_word(text=TEXT, stopwords=STOPWORDS):
    """Return (word, count) for the most common word, or (None, 0)."""
    # TODO: ignored = the stopwords in lowercase (a new set).
    # TODO: counts = Counter(); for token in text.lower().split(): word = _clean(token)
    #       if word and word not in ignored: counts[word] += 1
    # TODO: return counts.most_common(1)[0], or (None, 0) if counts is empty.
    ...
'''),

    8: ('def get_movies_by_director', r'''# What you practise
# -----------------
# 1. defaultdict(list) groups items: directors[name].append(movie) works even
#    for a new name. Reading a missing name gives [] instead of KeyError.
# 2. A namedtuple holds one record with named fields:
#        movie = Movie(title='Up', year=2009, score=8.3)
#        movie.score  -> 8.3
# 3. sorted(..., key=..., reverse=True) ranks the results.
#
# Work in three steps. The tests run top to bottom. Submit also runs the
# edge-case tests.
#
#   Step 1 (get_movies_by_director)  -> test_get_movies_by_director,
#                                       test_director_movies_data_structure
#   Step 2 (calc_mean_score)         -> test_calc_mean_score
#   Step 3 (get_average_scores)      -> test_get_average_scores_top_directors and the rest


# Step 1: group the movies by director. Skip movies from before MIN_YEAR (1960).
#
#     _movie_rows() yields tuples such as
#         ('Sergio Leone', 'The Good, the Bad and the Ugly', 1966, 8.9)
#
#     movies = get_movies_by_director()
#     movies['Sergio Leone'][0]  -> Movie(title=..., year=1966, score=8.9)
#     len(movies['Sergio Leone'])  -> 4
#     movies['Lowell Sherman']   -> []     (only a 1933 movie; skipped)
def get_movies_by_director():
    """Return a defaultdict(list): director -> list of Movie(title, year, score)."""
    # TODO: directors = defaultdict(list)
    # TODO: for director, title, year, score in _movie_rows():
    #           if year >= MIN_YEAR: append Movie(title, year, score) to directors[director]
    # TODO: return directors (keep the defaultdict).
    ...


# Step 2: the mean score of a list of movies, rounded to 1 decimal.
#
#     calc_mean_score([Movie('a', 2000, 7.0), Movie('b', 2000, 7.3)])  -> 7.2
#     calc_mean_score(movies['Sergio Leone'])                           -> 8.5
def calc_mean_score(movies):
    """Return round(mean of movie.score, 1)."""
    ...


# Step 3: rank directors with at least MIN_MOVIES (4) movies by mean score,
# highest first.
#
#     get_average_scores(movies)[:2]  -> [('Sergio Leone', 8.5), ('Christopher Nolan', 8.4)]
#
# For equal scores, keep the order of the input (sorted() is stable).
def get_average_scores(directors):
    """Return a list of (director, mean score), highest mean first."""
    # TODO: build (name, calc_mean_score(movies)) for each director with
    #       len(movies) >= MIN_MOVIES.
    # TODO: return sorted(pairs, key=lambda pair: pair[1], reverse=True).
    ...
'''),

    9: ('def get_num_words_spoken_by_character_per_episode', r'''# What you practise
# -----------------
# A nested counter: defaultdict(Counter). The outer dict creates a new
# Counter for a new character, and the Counter starts every new episode at 0:
#
#     counts = defaultdict(Counter)
#     counts['Cartman']['1'] += 2      <- no KeyError at either level
#     counts['Cartman']['1'] += 1
#     counts['Cartman']  -> Counter({'1': 3})
#
# There is one step. Every test calls the function.


# Count the words that each character speaks in each episode.
#
#     _rows(data) gives one dict per spoken line, for example:
#         {'Season': '1', 'Episode': '1', 'Character': 'Cartman', 'Line': 'Hello there'}
#
#     result = get_num_words_spoken_by_character_per_episode()
#     result['Cartman']  -> Counter({'1': 3, '2': 3})
#     result['Stan']     -> Counter({'1': 1})
#
# Words = len(line.split()). split() with no argument splits on any spaces,
# tabs or newlines. Keep the episode as the text from the CSV ('03' stays '03').
def get_num_words_spoken_by_character_per_episode(data=DATA):
    """Return a defaultdict(Counter): character -> Counter(episode -> words)."""
    # TODO: counts = defaultdict(Counter)
    # TODO: for row in _rows(data):
    #           counts[row['Character']][row['Episode']] += len(row['Line'].split())
    # TODO: return counts (the defaultdict itself).
    ...
'''),

    11: ('def make_character_index', r'''# What you practise
# -----------------
# defaultdict(list) builds an index: index[name].append(line_number) works
# even for a new name. enumerate(lines, 1) numbers the lines from 1:
#
#     for number, line in enumerate(['a', 'b'], 1):  -> (1, 'a'), (2, 'b')
#
# There is one step. Every test calls make_character_index.


# Map each character to the line numbers (from 1) where it is mentioned.
#
# A character is a name ('wolf') or a tuple of aliases
# ('Grandmother', 'Grandma', 'Granny'). Use the FIRST alias as the key.
# _mentions(line, aliases) does the matching (whole words, any case).
#
#     text = 'Red met the wolf.\nThe WOLF spoke.\nRed ran home.'
#     make_character_index(text, ['Red', 'wolf'])
#         -> {'Red': [1, 3], 'wolf': [1, 2]}
#     make_character_index('Granny waved.', [('Grandmother', 'Granny')])
#         -> {'Grandmother': [1]}
#
# A line number is added once, even if the line names the character twice.
# Blank lines count as lines. Characters that are never mentioned are left out.
def make_character_index(text, characters):
    """Return a plain dict: character (first alias) -> list of line numbers."""
    # TODO: index = defaultdict(list)
    # TODO: for each character: aliases = (character,) if it is a str, else character.
    #       for number, line in enumerate(text.splitlines(), 1):
    #           if _mentions(line, aliases): index[aliases[0]].append(number)
    # TODO: return dict(index) (a plain dict, so missing names are not created).
    ...
'''),
}

HINTS = {
    1: ['Concept: a namedtuple field has a name, so belt.score is the same as belt[0]. Use the names: they make the formula readable.',
        'Loop over belts.values(), not belts: the keys are only the belt names. sum(belt.score * belt.ninjas for belt in belts.values()) is the whole answer.',
        'The sum of an empty sequence is 0, so get_total_points({}) needs no special case.'],
    2: ['Concept: deque(maxlen=n) is a bounded queue. When it is full, append() drops the oldest item from the left.',
        'The function is one line: return deque(maxlen=n). Create the deque inside the function, so every call returns a new queue.'],
    3: ['Concept: defaultdict(list) creates an empty list for a new key, so groups[key].append(name) works without an if.',
        "Each row from _rows(data) is a dict with 'last_name', 'first_name' and 'country_code'. The name format is first name, a space, last name.",
        'Create the defaultdict inside the function and return it as it is. A test checks that the result is a defaultdict with list as its default factory.'],
    5: ['Concept: a function that contains yield is a generator. It returns a generator object, and each yield hands out one value to the loop that reads it.',
        "Split each path once: challenge, user = path.strip().split('/'). Skip excluded users before you count anything, so they count in neither Counter.",
        'Counter.most_common(1) returns a list such as [("25", 2)]. Take [0] for the pair, and [0][0] for the user name. An empty Counter returns [], so handle that case first.'],
    7: ['Concept: Counter counts hashable items. counts[word] += 1 starts a new word at 0, and counts.most_common(1) returns [(word, count)].',
        'Order per token: lowercase, then _clean, then skip it if it is empty or a stopword. Lowercase the stopwords too: the tests pass "The" as a stopword.',
        'Return counts.most_common(1)[0] when counts has items, else (None, 0). Build a new set for the stopwords; do not change the argument.'],
    8: ['Concept: defaultdict(list) groups records by a key, and a namedtuple gives each record named fields such as movie.score.',
        'Skip movies with year < MIN_YEAR while you group. Return the defaultdict itself: a test reads a director with no movies and expects [].',
        'calc_mean_score: round(sum(m.score for m in movies) / len(movies), 1). get_average_scores keeps directors with len(movies) >= MIN_MOVIES and sorts by the mean, highest first.'],
    9: ['Concept: defaultdict(Counter) is a two-level counter. counts[character][episode] += n works even when both keys are new.',
        "Words in one line: len(row['Line'].split()). split() without arguments splits on spaces, tabs and newlines and ignores repeats.",
        'Use the episode text as it is in the CSV, for example "03". Return the defaultdict itself; a test checks its default factory.'],
    11: ['Concept: defaultdict(list) builds an index: index[key].append(number) works for a new key. enumerate(lines, 1) gives line numbers that start at 1.',
         'A character is a str or a tuple of aliases. Turn a str into a one-item tuple, and use aliases[0] as the key. The supplied _mentions(line, aliases) checks all aliases at once.',
         'Use text.splitlines() so blank lines keep their numbers. Return dict(index) at the end, so the result is a plain dict.'],
}


def apply(specs):
    """Replace the starter and hints of each selected exercise."""
    for spec in specs:
        number = spec['number']
        if number not in GUIDED:
            continue
        marker, tail = GUIDED[number]
        template = spec['template']
        assert template.count(marker) == 1, (number, marker)
        spec['template'] = template[:template.index(marker)] + tail
        spec['hints'] = HINTS[number]
        spec['guided'] = True
