# 06. Convert dict to namedtuple/json

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/convert-dict-to-namedtuplejson/)

Implement `dict2nt(dict_)` and `nt2json(nt)`. Convert a dictionary to a namedtuple with matching field names, field order, and values. Keys are valid unique namedtuple field names: Python identifiers that do not start with an underscore and are not keywords. An empty dictionary is valid. Return JSON text for the namedtuple fields. Convert values that JSON cannot encode directly, such as datetime, with `str`. Do not change the input.

**Source and offline changes:** This version keeps the original free template and tests, with added boundary tests.

<details>
<summary>Original public description</summary>

Write a function to convert the given blog `dict` to a `namedtuple`

Write a second function to convert the resulting `namedtuple` to `json`.

Here you probably need to use two of the `_` methods of `namedtuple`

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`dict_convert`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
