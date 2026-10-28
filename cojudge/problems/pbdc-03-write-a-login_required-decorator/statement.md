# 03. Write a login_required decorator

Implement `login_required(func)`.

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
