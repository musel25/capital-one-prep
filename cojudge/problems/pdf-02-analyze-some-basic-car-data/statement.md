# 02. Analyze some basic car data

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/analyze-some-basic-car-data/)

Implement `most_prolific_automaker(year, cars=CARS)` and `get_models(automaker, year, cars=CARS)`. `CARS` is decoded from the supplied JSON text. Each record has `id`, `automaker`, `model`, and integer `year`. Count matching records for the specified year. Return the automaker name with the largest count, or `None` if there are none. Ties keep first appearance order among matching records. Return matching model names in input order from `get_models`. Keep duplicate records. Match automaker names exactly. Return an empty list if no models match. Do not change the input.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

The premium template and tests are recreated. A small local JSON fixture replaces the unavailable 1,000-record download. Argument order, tie rules, and empty-input results are defined for this version.

<details>
<summary>Original public description</summary>

In this exercise you will analyze some basic car data. Here is the (fake) JSON data we created with [Mockeroo](https://www.mockaroo.com/) - see this example snippet:

```python
  [{"id":1,"automaker":"Dodge","model":"Ram Van 1500","year":1999},
   {"id":2,"automaker":"Chrysler","model":"Town & Country","year":2002},
   {"id":3,"automaker":"Porsche","model":"Cayenne","year":2008},
   ... 997 car entries more ...
  ]

```

First you will write `most_prolific_automaker` to find out which automaker produces the most new models for a particular year.

Secondly you will write `get_models` which filters the data set down to car models produced by a particular *automaker* and *year* (as passed into the function).

To keep it a Beginner Bite we'll pause here, but if you like this data set, let us know and we make a follow-up Bite, maybe we can add some financial data :)

Check out the *docstrings* and *pytests* and give it a shot. Good luck and keep calm keep and code in Python.

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`car_data`. **Run** checks the first three tests. **Submit** checks all 7 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
