## Reference solution

Use this implementation above the supplied tests and runner.

```python
from functools import wraps

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
```
