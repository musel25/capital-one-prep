# 09. What south park characters talk most?

[Course list](/?course=pybites-collections) · [Original bite](https://pybitesplatform.com/bites/what-south-park-characters-talk-most/)

Implement `get_num_words_spoken_by_character_per_episode(data=DATA)`. The input is CSV text with `Season,Episode,Character,Line` headers. Return a `defaultdict(Counter)` mapping each character to word counts per episode. Episode keys stay strings. Count words by splitting dialogue on whitespace. Add counts across rows. Quoted commas, quotes, and newlines are valid CSV. Include a zero count for an empty dialogue. Header-only input returns an empty defaultdict. All records belong to one season and contain the four fields.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Did we already tell you we love the `collections` module? In this Bite we combine its `defaultdict` and `Counter` data structures for powerful data querying.

We will use [this cool South Park data set](https://github.com/BobAdamsEE/SouthParkData) (thanks [Peter](https://twitter.com/thelynchpinau) for the idea and collaboration on this one!). See the template below: we already completed `get_season_csv_file` to load in the csv data for a given season.

You need to complete `get_num_words_spoken_by_character_per_episode` which receives the loaded csv data ([example](https://raw.githubusercontent.com/pybites/SouthParkData/master/by-season/Season-1.csv)) and parse it into a defaultdict of Counter objects (don't forget to split by newlines first). Here is a snippet what you should end up with:

```python
              {'Agent 1': Counter({'8': 48, '2': 1}),
...
# Counter k,v here = (episode, # number of words spoken)
...
               'Anthropologist': Counter({'12': 101}),
...
               'Cartman': Counter({'1': 735,
                                   '10': 669,
                                   '13': 621,
... etc ...

```

Why is this cool? This structure makes it easy to do lookups by character, for example: *Cartman* was most talkative in episode 1, *Agent 1* in episode 8, etc. See more checks under the TESTS tab. Ready to add `collections` to your toolkit? Have fun!

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`southpark`. **Run** checks the first three tests. **Submit** checks all 6 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
