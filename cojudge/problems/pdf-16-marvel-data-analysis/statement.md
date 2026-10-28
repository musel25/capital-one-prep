# 16. Marvel data analysis

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/marvel-data-analysis/)

The supplied `Character` typed namedtuple has string fields `pid, name, sid, align, sex, appearances, year`. The supplied TSV loader creates the default `characters` list without network access. Each pid uniquely identifies a character; equal names with different pids are separate characters. Implement three functions. `most_popular_characters(data=characters, n=5)` returns up to n Character objects ordered by integer appearances descending, then numeric pid ascending. A blank appearance is zero. A negative n raises ValueError. `max_and_min_years_new_characters(data=characters)` counts characters introduced in each nonblank year. Return `((most_year, most_count), (least_year, least_count))` with integer years and counts. For ties, choose the earliest year in each result. If no character has a year, return `(None, None)`. `get_percentage_female_characters(data=characters)` returns the percentage whose sex is exactly `Female Characters`, rounded to two decimal places. Exclude blank sex values from the denominator; include every other specified gender. Return 0.0 if no genders are specified. All nonblank numeric fields contain nonnegative integer text. Do not change input lists or characters.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The premium docstrings and tests are unavailable. This version defines return shapes and tie rules explicitly. Its TSV is a small local practice sample. Characters with equal names remain separate, as required by the public description.

<details>
<summary>Original public description</summary>

Dive into the Marvel Universe! Your goal is to analyze a dataset of Marvel characters, focusing on popularity, historical introductions, and gender representation.

You'll implement three functions:

-`most_popular_characters`

 - `max_and_min_years_new_characters`

 - `get_percentage_female_characters`

You'll find more specific instructions in their docstrings.

The dataset is pre-loaded in the template code as a `list` of `Character` (typed) namedtuples, for example:

`Character(pid='1678', name='Spider-Man', sid='Secret Identity', align='Good Characters', sex='Male Characters', appearances='4043', year='1962')`

Note that each character is identified by a unique `pid`. Note that characters with the same name but different `pid`s represent different characters (across universes or timelines). See Thor for example:

`(Pdb) pp [ch for ch in characters if ch.name == "Thor"]
[Character(pid='2460', name='Thor', sid='No Dual Identity', align='Good Characters', sex='Male Characters', appearances='2258', year='1950'),
Character(pid='755266', name='Thor', sid='Secret Identity', align='Bad Characters', sex='Male Characters', appearances='1', year='1998'),
Character(pid='20704', name='Thor', sid='', align='Bad Characters', sex='Male Characters', appearances='', year='1954')]`

These are distinct characters and should not be aggregated by name alone.

**Tasks:**

- **Popularity**: Find the most popular characters based on their total appearances.
- **Yearly Introductions**: Identify the years with the highest and lowest numbers of new character introductions.
- **Gender Representation**: Calculate the percentage of female characters, ignoring characters without a specified gender.

Enjoy the journey through Marvel data while honing your Python skills!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`marvel_data`. **Run** checks the first three tests. **Submit** checks all 9 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
