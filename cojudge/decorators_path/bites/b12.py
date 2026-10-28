"""Recreated retry exercise; no premium source code used."""

SPEC = {
    "title": "Write a retry decorator",
    "module": "retrying",
    "contract": "Expose MAX_RETRIES=3 and class MaxRetriesException(Exception). retry(func) makes at most "
                "three TOTAL attempts per invocation, not three retries after the first call. Catch Exception "
                "subclasses and return the first successful result, including falsy results. If every attempt "
                "fails, raise MaxRetriesException chained from the final exception. Do not catch BaseException "
                "subclasses such as KeyboardInterrupt and SystemExit. Reset the attempt count on each invocation. "
                "Forward all positional and keyword arguments. Preserve the original function's metadata. Do not sleep.",
    "statement": """Write `retry` in `retrying` to repeat a failed function call.

The local constant `MAX_RETRIES = 3` means **three total attempts** per call.
Retry exceptions derived from `Exception`. Return immediately after a successful
call, including when its result is false or empty. Do not retry `KeyboardInterrupt`
or other exceptions outside `Exception`.

After three failures, raise `MaxRetriesException` with the final failure as its
explicit cause (`__cause__`). Define `MaxRetriesException` as an `Exception`
subclass. Each new call starts with three attempts, even after a previous call
succeeded or exhausted its attempts. Forward all positional and keyword
arguments on every attempt. Preserve the function's name, docstring, module,
annotations, and `__wrapped__` link. Use no waiting.

For example, a decorated function that fails twice and then returns `0` is
called three times and returns `0`.
""",
    "template": '''from functools import wraps

MAX_RETRIES = 3


class MaxRetriesException(Exception):
    """All allowed attempts failed."""


def retry(func):
    """Try the function up to MAX_RETRIES total times."""
    return func
''',
    "tests": '''import pytest

from retrying import MAX_RETRIES, MaxRetriesException, retry


def test_public_retry_configuration():
    assert MAX_RETRIES == 3
    assert issubclass(MaxRetriesException, Exception)


@pytest.mark.parametrize('value', [None, False, 0, '', [], {}, 'ready'])
def test_successful_results_stop_immediately(value):
    calls = []
    @retry
    def operation():
        calls.append(1)
        return value
    assert operation() is value
    assert calls == [1]


@pytest.mark.parametrize('failures', [1, 2])
def test_recovers_after_exception(failures):
    calls = []
    @retry
    def operation():
        calls.append(1)
        if len(calls) <= failures:
            raise ValueError('temporary failure')
        return 0
    assert operation() == 0
    assert len(calls) == failures + 1


def test_three_total_attempts_and_final_exception_cause():
    errors = [ValueError('first'), LookupError('second'), RuntimeError('third')]
    calls = []
    @retry
    def operation():
        calls.append(1)
        raise errors[min(len(calls) - 1, 2)]
    with pytest.raises(MaxRetriesException) as caught:
        operation()
    assert len(calls) == 3
    assert caught.value.__cause__ is errors[-1]


def test_exception_subclasses_are_retried():
    class TemporaryError(Exception):
        pass
    calls = []
    @retry
    def operation():
        calls.append(1)
        if len(calls) < 3:
            raise TemporaryError('try again')
        return 'done'
    assert operation() == 'done'
    assert len(calls) == 3


@pytest.mark.parametrize('error_type', [KeyboardInterrupt, SystemExit, BaseException])
def test_base_exceptions_are_not_retried(error_type):
    calls = []
    error = error_type('stop')
    @retry
    def operation():
        calls.append(1)
        raise error
    with pytest.raises(error_type) as caught:
        operation()
    assert caught.value is error
    assert calls == [1]


def test_attempts_reset_after_exhaustion_and_after_success():
    calls = []
    @retry
    def operation(mode):
        calls.append(mode)
        if mode == 'fail' or calls.count(mode) < 3:
            raise ValueError(mode)
        return mode
    with pytest.raises(MaxRetriesException):
        operation('fail')
    assert operation('first') == 'first'
    assert operation('second') == 'second'
    with pytest.raises(MaxRetriesException):
        operation('fail')
    assert calls.count('fail') == 6
    assert calls.count('first') == calls.count('second') == 3


def test_positional_and_keyword_arguments_are_forwarded_on_each_attempt():
    calls = []
    @retry
    def operation(left, right, *, suffix):
        calls.append((left, right, suffix))
        if len(calls) == 1:
            raise TypeError('temporary failure')
        return left + right + suffix
    assert operation('a', 'b', suffix='!') == 'ab!'
    assert calls == [('a', 'b', '!'), ('a', 'b', '!')]


def test_metadata_and_wrapped_function_are_preserved():
    def operation(value: int) -> int:
        """Return a documented result."""
        return value
    decorated = retry(operation)
    assert decorated.__name__ == operation.__name__
    assert decorated.__doc__ == operation.__doc__
    assert decorated.__module__ == operation.__module__
    assert decorated.__annotations__ == operation.__annotations__
    assert decorated.__wrapped__ is operation
''',
    "reference": '''from functools import wraps

MAX_RETRIES = 3


class MaxRetriesException(Exception):
    """All allowed attempts failed."""


def retry(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                if attempt == MAX_RETRIES - 1:
                    raise MaxRetriesException('all attempts failed') from error
    return wrapped
''',
    "mutations": [
        {"name": "four_total_attempts", "old": "MAX_RETRIES = 3", "new": "MAX_RETRIES = 4"},
        {"name": "base_exceptions_are_retried", "old": "except Exception as error:", "new": "except BaseException as error:"},
        {"name": "missing_final_cause", "old": "raise MaxRetriesException('all attempts failed') from error", "new": "raise MaxRetriesException('all attempts failed') from None"},
        {"name": "drop_keyword_arguments", "old": "return func(*args, **kwargs)", "new": "return func(*args)"},
        {"name": "lose_metadata", "old": "    @wraps(func)\n", "new": ""},
    ],
    "examples": [{"input": "A @retry function fails twice, then returns 0", "output": "0", "explanation": "The third call succeeds. A falsy result is still success."}],
    "notes": "Recreated local API. MAX_RETRIES counts total attempts. The final exception is the explicit cause of MaxRetriesException.",
    "original": False,
}
