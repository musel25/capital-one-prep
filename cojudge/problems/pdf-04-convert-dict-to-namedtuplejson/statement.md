Write a function to convert the given blog `dict` to a `namedtuple`

Write a second function to convert the resulting `namedtuple` to `json`.

Here you probably need to use two of the `_` methods of `namedtuple`

**Constraints:**

- Dictionary keys are valid namedtuple field names; preserve field order and stringify values JSON cannot encode.
- `dict2nt(d)` returns a namedtuple whose fields are the keys of `d`. `nt2json(nt)` returns `json.dumps(nt._asdict(), default=str)`.
