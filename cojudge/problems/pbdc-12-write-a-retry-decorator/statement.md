# 12. Write a retry decorator

Write `retry` in `retrying` to repeat a failed function call.

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
