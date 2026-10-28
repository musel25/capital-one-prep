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

The supplied composers and operas are small constructed fixtures.

**Constraints:**

- Birth and death dates are inclusive; preserve opera order.
