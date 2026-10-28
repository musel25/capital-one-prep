# 21. Composition, inheritance, abstract base class, what?

[Course list](/?course=pybites-oop) · Pybites Advanced · [Original bite](https://pybitesplatform.com/bites/composition-inheritance-abstract-base-class-what/)

**Inputs and required behavior for this version:**

This version reads cached files only. File names are relative names under the existing TMP directory. Missing files return None; empty files return an empty string. Web.soup returns a Soup even when data is missing. Tables have one header row, followed by zero or more rows with exactly the documented fields. Numeric cells use plain int or float text. parse_rows skips the header and preserves row order. NYTimes returns LeaderBoard records; RealClearPolitics returns Poll records. Default table indices are 0 and 2 respectively. Explicit indices must be valid and nonnegative. Statistics use nonempty tables and the exact documented format; RCP orders candidate totals from highest to lowest, with tied order unspecified. Nested tables, malformed HTML or rows, file access errors, and network downloads are outside this exercise.

<details>
<summary>Original bite description</summary>

It’s not as bad as that sounds, really. If you don’t know the difference between composition and inheritance, I would recommend reading up on it from [Real Python](https://realpython.com/inheritance-composition-python/). As most of their articles, the subject is covered pretty thoroughly!

### The scenario

So you’ve been tasked with scraping some presidential polling sites. The plan is to create a scraper that can be used on multiple sites.

I’ve already created the following *namedtuples*, but you will need to add type hints to them:

`Candidate`, `LeaderBoard`, and `Poll`

>  I’ve never tried to add type hinting to *namedtuples*, so it was a great learning experience for me and I hope to pass that experience along to you.

The plan is to create the following core classes:

- File:
  - Variables:
    - name: *str*
    - path: *Path*

  - Methods:
    - data -> *Optional[str]*

- Web:
  - Variables:
    - url: *str*
    - file: *File*

  - Methods:
    - data -> *Optional[str]*
    - soup -> *Soup*

- Site(*ABC*):
  - Variables:
    - web: *Web*

  - Methods:
    - find_table -> *str*
    - parse_rows -> *Union[List[LeaderBoard], List[Poll]]*
    - polls -> *Union[List[LeaderBoard], List[Poll]]*
    - stats

>  Site is an abstract base class which decorates some methods with abstractmethods!

If you are not familiar with Abstract Base Classes, read up on the documentation: [ABC](https://docs.python.org/3/library/abc.html)

### Adding new parsers

After creating the core of the application, you will have to create parsers for [The New York Times](https://www.nytimes.com/interactive/2020/us/elections/democratic-polls.html) and [RealClearPolitics](https://www.realclearpolitics.com/epolls/2020/president/us/2020_democratic_presidential_nomination-6730.html#polls). Don’t be scared by all the data, we’re only interested in the **Current State of the Race** table from *NYTimes* and the third table from *RCP*. Since the tables in RCP all pretty much have the same layout, your parser should work with any of them, but that won’t be checked.

The parsers should derive from the *Site* class. While coding this, I was able to get the `find_table` method to work for all sites, so that one is not decorated with `@abstractmethod`. The other methods however, need to be overwritten in order for them to be instantiated.

- RealClearPolitics(Site):
  - Variables:
    - web: Web

  - Methods:
    - find_table -> *str*
    - parse_rows -> *List[Poll]*
    - polls -> *List[Poll]*
    - stats

- NYTimes(Site):
  - Variables:
    - web: Web

  - Methods:
    - find_table -> *str*
    - parse_rows -> *List[Poll]*
    - polls -> *List[Poll]*
    - stats

### The output format

Each of the two different parsers will have different outputs. We’ll just keep it simple, but there are some rules to adhere to. First, this is what sample output from each should look like.

**NYTimes**

```python
NYTimes
=================================

                   Pete Buttigieg
---------------------------------
National Polling Average: 10%
       Pledged Delegates: 25
Individual Contributions: $76.2m
    Weekly News Coverage: 3

                   Bernie Sanders
---------------------------------
etc..
    Weekly News Coverage: 3

```

Things to note about this output:

- Starts and ends with blank lines
- There is a similar output for each of the remaining candidates:
  - Bernie Sanders
  - Joseph R. Biden Jr.
  - Tulsi Gabbard

- Not shown here, but there is a blank line between each candidate
- There are 33 equal (**=**) signs and hyphens (**-**) in the dividers
- The name of the candidate is right aligned
- The data lines are all right aligned
- The values from the data lines are all left aligned

>  *etc..* is just a place holder, indicating that not all data was shown

**RealClearPolitics**

```python
RealClearPolitics
=================
    Biden: 214.0
  Sanders: 142.0
  Gabbard: 6.0

```

Some things to note here.

- Starts and ends with blank line
- This is the whole output for this scraper
- There are as many equal (**=**) signs as the length of the title
- The candidate last names are right aligned

### Time to start coding

That’s it. I’ve scattered a generous amount of docstrings all over the code to try and make it as explicit as possible in order to help you out. When you complete this bite, you will have learned and or gained more experience with:

- Object Oriented Programming
- Dataclasses
- Inheritance
- Composition
- Abstract Base Classes
  - The *@abstractmethod* decorator

- Type hinting *namedtuples*
- String formatting
- Web scraping with BeautifulSoup

</details>

**Notes for this version:** This is an offline version. The judge has no network and no BeautifulSoup, so the template supplies a small `Soup` class with `find_all("table")`, and `Web.data` reads the cached HTML file (the tests create it). The sample pages in the tests are fictional and contain only the tables that are used. Everything else follows the description: the typed namedtuples, `File`, `Web`, the `Site` abstract base class, the two parsers, and the exact output formats.

**How to solve it here:** write your code at the top of the editor, like the Pybites Code tab.
The Pybites tests are in the editor below your code (the Tests tab). The tests import your code as
the module `scraper`. **Run** checks the first three tests. **Submit** runs all
15. A failing test shows its name, the error, and the failed test line. The original template and tests are in Pybites premium, so the template and tests here are a recreation that follows the description.

**Constraints:**

- Python 3.11, standard library only. No network access.
- Do not edit the tests or the supplied runner at the bottom of the editor.
- For an older saved solution, use **+** beside the editor tabs to open the current template in a new tab. Copy your implementation into that tab. This keeps the saved solution and gives you the current tests.
