"""Guided starters (the Pybites OOP bite 15 pattern) for the selected exercises.

Each entry replaces the whole starter with the same public names, a short
concept explanation, steps mapped to the tests, and TODO comments with exact
input and output examples. Tests and references do not change.
"""

_DECORATOR_BASICS = r'''# What you practise
# -----------------
# A decorator is a function that takes a function and returns a new function
# (the wrapper). The @ line is short for a reassignment:
#
#     @sandwich                      def filling(): ...
#     def filling(): ...      ==     filling = sandwich(filling)
#
# The usual shape:
#
#     def decorator(func):
#         @wraps(func)                    <- copies __name__, __doc__, annotations
#         def wrapper(*args, **kwargs):   <- accepts any arguments
#             ...                         <- code BEFORE the call
#             result = func(*args, **kwargs)
#             ...                         <- code AFTER the call
#             return result
#         return wrapper                  <- return it, do not call it
#
# Decorating must not call func. Only a call of the wrapper calls func.
'''

GUIDED = {
    1: r'''from functools import wraps

UPPER_SLICE = "=== Upper bread slice ==="
LOWER_SLICE = "=== Lower bread slice ==="

''' + _DECORATOR_BASICS + r'''#
# There is one step. Every test decorates a function with sandwich.


# Print the upper slice, call func, print the lower slice, return func's result.
#
#     @sandwich
#     def filling():
#         print('cheese')
#
#     filling()      prints:
#     === Upper bread slice ===
#     cheese
#     === Lower bread slice ===
#
# If func raises, let the exception go to the caller (no try/except needed).
def sandwich(func):
    """Add bread output around a function call."""
    # TODO: define wrapper(*args, **kwargs) with @wraps(func) above it.
    # TODO: in wrapper: print(UPPER_SLICE), result = func(*args, **kwargs),
    #       print(LOWER_SLICE), return result.
    # TODO: return wrapper.
    ...
''',

    2: r'''from functools import wraps

''' + _DECORATOR_BASICS + r'''#
# A decorator WITH an argument needs one more level. make_html('p') is not
# the decorator: it RETURNS the decorator.
#
#     @make_html('p')          ==     text = make_html('p')(text)
#     def text(): ...
#
#     make_html(tag)  -> returns decorate
#     decorate(func)  -> returns wrapper
#     wrapper(...)    -> calls func and returns the tagged text
#
# The inner functions can read tag, because they are defined inside
# make_html (a closure).
#
# There is one step. Every test uses make_html.


# Put the text that func returns between <tag> and </tag>.
#
#     @make_html('span')
#     def text():
#         return 'Hello'
#     text()  -> '<span>Hello</span>'
#
#     @make_html('p')
#     @make_html('strong')       <- the lower decorator wraps first
#     def text(): return 'Hello'
#     text()  -> '<p><strong>Hello</strong></p>'
#
# Do not escape the text: '<b>A & B</b>' stays as it is.
def make_html(tag):
    """Create a decorator that encloses returned text in an HTML tag."""
    # TODO: def decorate(func):
    #           @wraps(func)
    #           def wrapper(*args, **kwargs):
    #               text = func(*args, **kwargs)
    #               return f'<{tag}>{text}</{tag}>'
    #           return wrapper
    # TODO: return decorate.
    ...
''',

    3: r'''from functools import wraps

known_users = ['bob', 'julian', 'mike', 'carmen', 'sue']
loggedin_users = ['mike', 'sue']

''' + _DECORATOR_BASICS + r'''#
# A wrapper can also decide NOT to call func, and return something else.
#
# There is one step. Every test uses login_required.


# Check the user before the call. The user is the first positional argument
# or the keyword argument user:
#     user = args[0] if args else kwargs['user']
#
#     welcome('ada')    -> 'please create an account'   (not in known_users)
#     welcome('bob')    -> 'please login'               (known, not logged in)
#     welcome('mike')   -> 'welcome back mike'          (calls welcome)
#
# Check known_users FIRST. Read both lists on every call (the tests change
# them). If a check fails, return the message and do not call func.
def login_required(func):
    """Allow calls from known users who are logged in."""
    # TODO: define wrapper(*args, **kwargs) with @wraps(func) above it.
    # TODO: in wrapper: get the user (see above).
    #       if user not in known_users: return 'please create an account'
    #       if user not in loggedin_users: return 'please login'
    #       return func(*args, **kwargs)
    # TODO: return wrapper.
    ...


@login_required
def welcome(user):
    return f'welcome back {user}'
''',

    4: r'''from functools import wraps

''' + _DECORATOR_BASICS + r'''#
# A wrapper can check the arguments BEFORE the call, and raise an error so
# that func never runs.
#
# SUPPLIED: _check_arg does the type and range check. It is not the skill of
# this exercise. Use it. Do not edit it.
#
# There is one step. Every test uses validate_int_args.


def _check_arg(value):
    """Raise TypeError for a non-int (bool too). Raise ValueError for a negative int."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError('positional arguments must be integers')
    if value < 0:
        raise ValueError('positional arguments must be nonnegative')


# Check each POSITIONAL argument from left to right, then call func.
#
#     @validate_int_args
#     def total(*values, label='sum'):
#         return label, sum(values)
#
#     total(0, 2, 3, label='count')  -> ('count', 5)
#     total(1, -1)                   -> raises ValueError (func is not called)
#     total(True)                    -> raises TypeError
#     total(-1, 'bad')               -> raises ValueError (the first bad one wins)
#
# Do not check keyword arguments. Pass them on unchanged.
def validate_int_args(func):
    """Allow only nonnegative integers in positional arguments."""
    # TODO: define wrapper(*args, **kwargs) with @wraps(func) above it.
    # TODO: in wrapper: for value in args: _check_arg(value)
    #       then return func(*args, **kwargs).
    # TODO: return wrapper.
    ...
''',

    7: r'''# What you practise
# -----------------
# A context manager is an object that you use in a with statement. Python
# calls two special methods for you:
#
#     with account as acc:      1. calls account.__enter__(); its return value is acc
#         acc - 5               2. runs the block
#                               3. calls account.__exit__(exc_type, exc_value, traceback)
#
# __exit__ runs even when the block raises. Then the three arguments describe
# the exception; otherwise they are all None. If __exit__ returns a true
# value, Python hides the exception. Return None or False to let it through.
#
# Here the context manager gives a rollback: after the block, if the balance
# is below 0, undo every transaction that the block made.
#
# The first tests do not use the with statement. Then:
#
#   Step 1 (__enter__)  -> test_with_contextman_performs_rollback needs both steps
#   Step 2 (__exit__)   -> then the tests after it


class Account:

    def __init__(self):
        self._transactions = []

    @property
    def balance(self):
        return sum(self._transactions)

    def __add__(self, amount):
        self._transactions.append(amount)

    def __sub__(self, amount):
        self._transactions.append(-amount)

    # Step 1: remember where the block starts, and give the account to the block.
    #
    #     with account as acc:
    #         acc is account   -> True
    def __enter__(self):
        # TODO: store len(self._transactions) on self (for example self._start).
        # TODO: return self.
        ...

    # Step 2: after the block, roll back if the FINAL balance is below 0.
    #
    #     account + 3
    #     with account as acc:
    #         acc - 5                    balance -2 at the end -> roll back
    #     account.balance  -> 3
    #
    #     with account as acc:
    #         acc - 10
    #         acc + 6                    balance -1 at the end -> roll back
    #     with account as acc:
    #         acc - 3                    balance 0 at the end  -> keep it
    #
    # Undo only this block: delete the transactions from the stored start
    # position to the end. Then return False, so an exception in the block
    # still reaches the caller.
    def __exit__(self, exc_type, exc_value, traceback):
        # TODO: if self.balance < 0: del self._transactions[self._start:]
        # TODO: return False.
        ...
''',

    9: r'''import contextlib
import time
from collections import Counter
from datetime import date

OPERATION_THRESHOLD_IN_SECONDS = 2.2
ALERT_THRESHOLD = 3
ALERT_MSG = 'ALERT: suffering performance hit today'

violations = Counter()

# What you practise
# -----------------
# @contextlib.contextmanager turns a generator function into a context
# manager. The code BEFORE yield runs when the with block starts. The code
# AFTER yield runs when the block ends:
#
#     @contextlib.contextmanager
#     def timeit():
#         start = ...           <- runs at "with timeit():"
#         yield                 <- the with block runs here
#         ...                   <- runs after the block
#
# If the block raises, the exception comes out at the yield. To run your
# end code in every case, put the yield in try and the end code in finally.
# Do not catch the exception: it must still reach the caller.
#
# SUPPLIED: _record does the threshold, the daily count and the alert. It is
# not the skill of this exercise. Use it. Do not edit it.
#
# There is one step. Every test uses timeit.


def _record(duration):
    """Count a violation for today if duration >= the threshold; print ALERT_MSG from the 3rd one on."""
    if duration >= OPERATION_THRESHOLD_IN_SECONDS:
        today = date.today()
        violations[today] += 1
        if violations[today] >= ALERT_THRESHOLD:
            print(ALERT_MSG)


# Measure how long the with block takes, then pass the seconds to _record.
#
#     with timeit():
#         slow_operation()       # takes 3 seconds
#     -> _record(3.0) counts one violation for today
#
#     with timeit():
#         raise ValueError()     # after 3 seconds
#     -> _record(3.0) still runs, then the ValueError reaches the caller
#
# Use time.perf_counter() for both readings (the tests replace it with a
# fake clock). The with block gets None (a bare yield).
@contextlib.contextmanager
def timeit():
    # TODO: start = time.perf_counter()
    # TODO: try:
    #           yield
    #       finally:
    #           _record(time.perf_counter() - start)
    yield
''',

    12: r'''from functools import wraps

MAX_RETRIES = 3


class MaxRetriesException(Exception):
    """All allowed attempts failed."""


''' + _DECORATOR_BASICS + r'''#
# A wrapper can also call func more than once. Put the call in a loop, and
# use try/except to catch a failed attempt and try again.
#
# There is one step. Every test uses retry.


# Call func up to MAX_RETRIES (3) times in total.
#
#     - It returns a value  -> return that value at once (even None, 0 or '').
#     - It raises Exception -> try again.
#     - The 3rd attempt raises Exception too:
#           raise MaxRetriesException(...) from <the last error>
#       ("from" stores the last error as __cause__; a test checks it.)
#
# Catch only Exception. KeyboardInterrupt and SystemExit are not Exception
# subclasses, so they stop the loop at once. Each call of the wrapper starts
# again from attempt 1.
def retry(func):
    """Try the function up to MAX_RETRIES total times."""
    # TODO: define wrapper(*args, **kwargs) with @wraps(func) above it.
    # TODO: in wrapper:
    #           for attempt in range(MAX_RETRIES):
    #               try:
    #                   return func(*args, **kwargs)
    #               except Exception as error:
    #                   last_error = error
    #           raise MaxRetriesException('all attempts failed') from last_error
    # TODO: return wrapper.
    return func
''',
}

HINTS = {
    1: ['Concept: a decorator takes func and returns a wrapper function. @sandwich above def filling is the same as filling = sandwich(filling).',
        'The wrapper is def wrapper(*args, **kwargs). It prints UPPER_SLICE, calls result = func(*args, **kwargs), prints LOWER_SLICE, and returns result.',
        'Put @wraps(func) above def wrapper, so the wrapper keeps the name, docstring and annotations of func. sandwich returns wrapper without calling it.'],
    2: ['Concept: a decorator with an argument is a function that returns a decorator. make_html(tag) returns decorate, and decorate(func) returns wrapper.',
        "The wrapper calls text = func(*args, **kwargs) and returns f'<{tag}>{text}</{tag}>'. tag comes from the outer function (a closure).",
        'Put @wraps(func) above def wrapper. With two decorators, the one nearest to def wraps first, so @make_html("p") over @make_html("strong") gives <p><strong>...</strong></p>.'],
    3: ['Concept: a wrapper decides whether to call func. Return the message instead of calling func when a check fails.',
        "Get the user with user = args[0] if args else kwargs['user']. Check known_users first, then loggedin_users, inside the wrapper so each call reads the current lists.",
        'Return func(*args, **kwargs) only when both checks pass, and forward all arguments unchanged. Use @wraps(func).'],
    4: ['Concept: a wrapper can validate the arguments before the call. If a check raises, func never runs.',
        'Loop over args (the positional arguments) from left to right and call _check_arg(value) for each one. Do not check kwargs.',
        'After the loop, return func(*args, **kwargs). Use @wraps(func) above def wrapper.'],
    7: ['Concept: the with statement calls __enter__ at the start and __exit__ at the end, also when the block raises. The value that __enter__ returns is the name after "as".',
        'In __enter__, store the current number of transactions, for example self._start = len(self._transactions), and return self.',
        'In __exit__, if self.balance < 0, delete self._transactions[self._start:]. Return False, so an exception in the block is not hidden.'],
    9: ['Concept: in a @contextlib.contextmanager function, the code before yield runs at the start of the with block and the code after yield runs at the end.',
        'Read the clock with time.perf_counter() before the yield and again after it. The difference is the duration in seconds. Pass it to _record(duration).',
        'Use try: yield / finally: _record(...). finally runs also when the block raises, and the exception still reaches the caller.'],
    12: ['Concept: a retry decorator puts the call in a loop: for attempt in range(MAX_RETRIES), try to return func(*args, **kwargs).',
         'Catch only Exception and keep it: except Exception as error: last_error = error. KeyboardInterrupt and SystemExit are BaseException, so they pass through.',
         'After the loop, raise MaxRetriesException(...) from last_error. Use @wraps(func) on the wrapper; a test checks __wrapped__.'],
}


def apply(spec):
    """Replace the starter and hints of a selected exercise."""
    number = spec['number']
    if number in GUIDED:
        spec['template'] = GUIDED[number]
        spec['hints'] = HINTS[number]
        spec['guided'] = True
    return spec
