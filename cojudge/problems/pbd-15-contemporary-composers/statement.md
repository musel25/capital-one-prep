# 15. Contemporary composers

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/contemporary-composers/)

operas_both_at_premiere(guest, composer) returns a list of the given author's opera titles where both people were alive at the premiere, in fixture order. Birth and death dates are inclusive. Use the module composers dictionary and operas list. Unknown names raise ValueError. Equal guest and composer names are allowed. Dates use YYYY-MM-DD. The supplied namedtuple fixtures are constructed examples.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

You are given a list of `operas` and a list of `composers`. For two given composers find operas (where one of the composers is the author) at which premiere both could have been together (i.e. they both had to be alive). Consider just a theoretical possibility of presence, so omit health condition, traveling problems, resources, and any other problems (excluding death) which could restrict their presence.

The list of `operas` consists of `namedtuple('Opera', 'author play date')` objects. The list of `composers` contains dictionaries with keys => composer names and values => `namedtuple('Composer', 'name born died')` objects.

Complete the `operas_both_at_premiere(guest, composers)` function. Parameters:

```python
  guest - one of the composers but not the author of an opera
  composer - the author of an opera

```

If the required composer or guest is not in the list of composers, raise a `ValueError` exception. You can use the `_get_date` helper to convert date strings into `datetime` objects.

Return a `list` (or generator) of titles of operas. See the tests for more information.

---

Note that the list of operas in the Bite is shortened.
Sources:
[https://en.wikipedia.org/wiki/List_of_operas_by_Wolfgang_Amadeus_Mozart](https://en.wikipedia.org/wiki/List_of_operas_by_Wolfgang_Amadeus_Mozart) [https://en.wikipedia.org/wiki/List_of_compositions_by_Ludwig_van_Beethoven](https://en.wikipedia.org/wiki/List_of_compositions_by_Ludwig_van_Beethoven) [https://en.wikipedia.org/wiki/List_of_works_for_the_stage_by_Richard_Wagner](https://en.wikipedia.org/wiki/List_of_works_for_the_stage_by_Richard_Wagner) [https://en.wikipedia.org/wiki/List_of_compositions_by_Giuseppe_Verdi](https://en.wikipedia.org/wiki/List_of_compositions_by_Giuseppe_Verdi)

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`composers_dates`. **Run** checks the first three tests. **Submit** checks all 7 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
