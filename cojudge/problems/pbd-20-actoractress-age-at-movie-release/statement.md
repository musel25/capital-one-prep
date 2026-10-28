# 20. Actor/actress age at movie release

[Course list](/?course=pybites-datetimes-timezones) · [Original bite](https://pybitesplatform.com/bites/actoractress-age-at-movie-release/)

Actor(name, born) and Movie(title, release_date) are supplied dataclasses. Dates use full English month names: "July 31, 1962". get_age(actor, movie) returns "NAME was N years old when TITLE came out." Use completed birthdays. For a February 29 birth in a non-leap year, the birthday completes on March 1. Invalid dates or a release before birth raise ValueError.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Ever wondered how old an actor/actress was in a particular movie? In this Bite you will write some code to find the answer.

Here is how it should work (the `Actor` and `Movie` `dataclass`es are provided):

```python
  (Pdb) actor
  Actor(name='Wesley Snipes', born='July 31, 1962')
  (Pdb) movie
  Movie(title='New Jack City', release_date='January 17, 1991')
  (Pdb) get_age(actor, movie)
  'Wesley Snipes was 28 years old when New Jack City came out.'
  ...
  (Pdb) actor
  Actor(name='Jennifer Aniston', born='February 11, 1969')
  (Pdb) movie
  Movie(title='Horrible Bosses', release_date='September 16, 2011')
  (Pdb) get_age(actor, movie)
  'Jennifer Aniston was 42 years old when Horrible Bosses came out.'

```

You might want to look into using `dateutil` to make this a lot easier :)

Keep calm and code in Python!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`actor_age`. **Run** checks the first three tests. **Submit** checks all 7 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
