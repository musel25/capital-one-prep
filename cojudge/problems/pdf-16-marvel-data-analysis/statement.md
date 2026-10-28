Dive into the Marvel Universe! Your goal is to analyze a dataset of Marvel characters, focusing on popularity, historical introductions, and gender representation.

You'll implement three functions:

-`most_popular_characters`

 - `max_and_min_years_new_characters`

 - `get_percentage_female_characters`

You'll find more specific instructions in their docstrings.

The dataset is pre-loaded in the template code as a `list` of `Character` (typed) namedtuples, for example:

`Character(pid='1678', name='Spider-Man', sid='Secret Identity', align='Good Characters', sex='Male Characters', appearances='4043', year='1962')`

Note that each character is identified by a unique `pid`. Note that characters with the same name but different `pid`s represent different characters (across universes or timelines). See Thor for example:

`(Pdb) pp [ch for ch in characters if ch.name == "Thor"]<br>[Character(pid='2460', name='Thor', sid='No Dual Identity', align='Good Characters', sex='Male Characters', appearances='2258', year='1950'),<br> Character(pid='755266', name='Thor', sid='Secret Identity', align='Bad Characters', sex='Male Characters', appearances='1', year='1998'),<br> Character(pid='20704', name='Thor', sid='', align='Bad Characters', sex='Male Characters', appearances='', year='1954')]`

These are distinct characters and should not be aggregated by name alone.

**Tasks:**

- **Popularity**: Find the most popular characters based on their total appearances.
- **Yearly Introductions**: Identify the years with the highest and lowest numbers of new character introductions.
- **Gender Representation**: Calculate the percentage of female characters, ignoring characters without a specified gender.

Enjoy the journey through Marvel data while honing your Python skills!

The supplied TSV is a small local sample.

**Constraints:**

- Rank appearances numerically, breaking ties by numeric pid; blank appearances count as zero.
- Return `((most_year, count), (least_year, count))`, choosing earliest years for ties and `(None, None)` if none exist.
- Round the female percentage to two decimals; exclude blank genders, and return `0.0` if none are specified.
