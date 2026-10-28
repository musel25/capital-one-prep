"""Login decorator: recreated from the public description."""

SPEC = {
    "title": "Write a login_required decorator",
    "module": "login",
    "original": False,
    "contract": (
        "known_users initially equals ['bob', 'julian', 'mike', 'carmen', 'sue']; "
        "loggedin_users initially equals ['mike', 'sue']. login_required(func) "
        "checks current lists on every call. The user is the first positional "
        "argument or the user keyword. Unknown users return 'please create an "
        "account', even if present in loggedin_users. Known logged-out users "
        "return 'please login'. For logged-in known users, call func once with "
        "all supplied arguments and return the same result. Preserve function "
        "name, docstring and annotations. Propagate wrapped exceptions. welcome(user) "
        "is decorated and returns f'welcome back {user}' for authorized users. "
        "User names are strings. Missing or duplicate user arguments are outside the contract."
    ),
    "statement": '''Implement `login_required(func)`.

Use the current module lists on each call. Apply these rules in order:

1. An unknown user gets `'please create an account'`.
2. A known user who is not logged in gets `'please login'`.
3. A known user who is logged in can call the wrapped function.

The user is the first positional argument or the `user` keyword argument.
Forward all arguments to authorized calls. Return the wrapped result.
Do not call the function for rejected users. Preserve the function name,
docstring and annotations. Propagate exceptions from authorized calls.
Keep the supplied decorated `welcome(user)` example.

```python
welcome('bob')   # 'please login'
welcome('mike')  # 'welcome back mike'
welcome('ada')   # 'please create an account'
```
''',
    "template": '''known_users = ['bob', 'julian', 'mike', 'carmen', 'sue']
loggedin_users = ['mike', 'sue']


def login_required(func):
    """Allow calls from known users who are logged in."""
    # TODO: return the decorated function.
    pass


@login_required
def welcome(user):
    return f'welcome back {user}'
''',
    "tests": '''import pytest

import login
from login import login_required, welcome


def test_initial_user_lists():
    assert login.known_users == ["bob", "julian", "mike", "carmen", "sue"]
    assert login.loggedin_users == ["mike", "sue"]


@pytest.mark.parametrize("user, expected", [
    ("bob", "please login"),
    ("julian", "please login"),
    ("carmen", "please login"),
    ("mike", "welcome back mike"),
    ("sue", "welcome back sue"),
    ("ada", "please create an account"),
    ("", "please create an account"),
    ("Mike", "please create an account"),
])
def test_welcome_outcomes(user, expected):
    assert welcome(user) == expected


def test_keyword_user_and_extra_arguments_reach_the_function_once():
    calls = []
    answer = {"status": "ready"}
    @login_required
    def access(user, *items, action="read"):
        calls.append((user, items, action))
        return answer
    assert access("mike", "a", "b", action="write") is answer
    assert access(user="sue", action="read") is answer
    assert calls == [("mike", ("a", "b"), "write"), ("sue", (), "read")]


def test_rejected_users_do_not_run_the_wrapped_function():
    calls = []
    @login_required
    def access(user, payload):
        calls.append((user, payload))
        return "secret"
    assert access("bob", "first") == "please login"
    assert access(user="outsider", payload="second") == "please create an account"
    assert calls == []


def test_unknown_user_takes_precedence_over_logged_in_list(monkeypatch):
    monkeypatch.setattr(login, "loggedin_users", ["outsider", "mike"])
    assert welcome("outsider") == "please create an account"
    assert welcome("mike") == "welcome back mike"


def test_current_lists_are_checked_on_each_call(monkeypatch):
    known = ["new"]
    active = []
    monkeypatch.setattr(login, "known_users", known)
    monkeypatch.setattr(login, "loggedin_users", active)
    assert welcome("new") == "please login"
    active.append("new")
    assert welcome("new") == "welcome back new"
    active.remove("new")
    assert welcome("new") == "please login"
    active.append("new")
    known.remove("new")
    assert welcome("new") == "please create an account"


def test_preserves_function_metadata():
    def access(user: str) -> str:
        """Read a private item."""
        return user
    wrapped = login_required(access)
    assert wrapped.__name__ == "access"
    assert wrapped.__doc__ == "Read a private item."
    assert wrapped.__annotations__ == {"user": str, "return": str}


def test_authorization_and_result_do_not_leak_between_calls():
    @login_required
    def first(user):
        return "first:" + user
    @login_required
    def second(user):
        return "second:" + user
    assert first("mike") == "first:mike"
    assert first("bob") == "please login"
    assert second("sue") == "second:sue"
    assert first("sue") == "first:sue"
    assert login.known_users == ["bob", "julian", "mike", "carmen", "sue"]
    assert login.loggedin_users == ["mike", "sue"]


def test_authorized_call_propagates_the_original_exception():
    error = RuntimeError("private operation failed")
    @login_required
    def access(user):
        raise error
    with pytest.raises(RuntimeError) as caught:
        access("mike")
    assert caught.value is error
''',
    "examples": [
        {"input": "welcome('bob')", "output": "please login"},
        {"input": "welcome('mike')", "output": "welcome back mike"},
        {"input": "welcome('ada')", "output": "please create an account"},
    ],
    "notes": "The template and tests are recreated from the public description. Current-list checks, keyword user calls, argument forwarding, metadata preservation and unknown-user precedence are explicit course guarantees.",
}

SPEC["reference"] = '''from functools import wraps

known_users = ['bob', 'julian', 'mike', 'carmen', 'sue']
loggedin_users = ['mike', 'sue']


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = args[0] if args else kwargs['user']
        if user not in known_users:
            return 'please create an account'
        if user not in loggedin_users:
            return 'please login'
        return func(*args, **kwargs)
    return wrapper


@login_required
def welcome(user):
    return f'welcome back {user}'
'''
SPEC["mutations"] = [
    {"name": "omit known-user check", "old": "        if user not in known_users:\n            return 'please create an account'\n", "new": ""},
    {"name": "omit logged-in check", "old": "        if user not in loggedin_users:\n            return 'please login'\n", "new": ""},
    {"name": "ignore keyword user", "old": "args[0] if args else kwargs['user']", "new": "args[0]"},
    {"name": "cache the lists at decoration time", "old": "def login_required(func):\n", "new": "def login_required(func):\n    known_users = list(globals()['known_users'])\n    loggedin_users = list(globals()['loggedin_users'])\n"},
    {"name": "drop keyword arguments", "old": "func(*args, **kwargs)", "new": "func(*args)"},
    {"name": "lose function metadata", "old": "    @wraps(func)\n", "new": ""},
]
