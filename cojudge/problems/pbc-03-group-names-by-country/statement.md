# 03. Group names by country

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/group-names-by-country/)

Implement `group_names_by_country(data=data)`. The input is CSV text with headers `last_name,first_name,country_code`. Return a `defaultdict(list)` mapping each country to full names in `first_name last_name` form. Quoted fields are valid. Ignore blank lines. Keep duplicate people. Country and name order does not matter. Header-only input returns an empty defaultdict. All nonblank records have the three required fields.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite you are presented with a list of surnames, names, and countries. These 3 fields are in a multiline string, separated by a comma.

Code `group_names_by_country`, looping through the list, returning a `collections.defaultdict` where the keys are countries and the values are `list`s of concatenated names and surnames. The order of the keys (countries) and the value lists (names) does not matter.

Here is an example of a possible input to your function:

```python
data = """last_name,first_name,country_code
Watsham,Husain,ID
Harrold,Alphonso,BR
Apdell,Margo,CN
Tomblings,Deerdre,RU
Wasielewski,Sula,ID
Jeffry,Rudolph,TD
Brenston,Luke,SE
Parrett,Ines,CN
Braunle,Kermit,PL
Halbard,Davie,CN"""

```

... and the output your function should return:

```python
defaultdict(<class 'list'>,
            {'BR': ['Alphonso Harrold'],
             'CN': ['Margo Apdell', 'Ines Parrett', 'Davie Halbard'],
             'ID': ['Husain Watsham', 'Sula Wasielewski'],
             'PL': ['Kermit Braunle'],
             'RU': ['Deerdre Tomblings'],
             'SE': ['Luke Brenston'],
             'TD': ['Rudolph Jeffry']})

```

Good luck and keep calm and code in Python! Read up on [`collections`](https://docs.python.org/3.7/library/collections.html), one of our favorite standard library modules!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`countries`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
