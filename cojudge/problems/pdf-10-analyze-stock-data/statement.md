# 10. Analyze stock data

[Course list](/?course=pybites-data-formats) · [Original bite](https://pybitesplatform.com/bites/analyze-stock-data/)

Implement four functions. `get_stock_data(data=STOCK_DATA)` parses a JSON string and returns its list of stock dictionaries. `get_stocks_by_sector(stocks, sector)` returns matching dictionaries in input order; compare sector names exactly. `get_largest_stock(stocks)` returns the dictionary with the largest numeric market capitalization (`cap`). Caps have a leading `$`, a nonnegative decimal number, and an optional M, B, or T suffix (million, billion, trillion). A cap of `n/a` is unknown and is excluded. With a tie, return the first stock. If no stock has a known cap, return None. `get_market_distribution(stocks)` returns a Counter mapping each `market` to its number of records. Count duplicate records. All required fields are present. Do not modify the input. Empty input produces an empty list, None, or an empty Counter as appropriate. The supplied JSON is a small local sample with the fields shown in the public description. The public description does not give the four original function contracts; these four queries define this recreation.

**Source and offline changes:** The premium template and tests are not available in this account. This version uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

In this Bite we will answer some questions about stocks, using some JSON data obtained from the awesome [Mockeroo *fake data generator service*](https://www.mockaroo.com/).

Here is a snippet of the output you will parse (full output [here](https://bites-data.s3.us-east-2.amazonaws.com/stocks.json)):

```python
  [{"id":1,"name":"Anworth Mortgage Asset  Corporation",
    "symbol":"ANH","industry":"Real Estate Investment Trusts",
    "sector":"Consumer Services","market":"NYSE","cap":"$600.57M"},
   {"id":2,"name":"DarioHealth Corp.",
   "symbol":"DRIO","industry":"Medical/Dental Instruments",
   "sector":"Health Care","market":"NASDAQ","cap":"$21.78M"},
   ... 998 more stocks ...
  ]

```

Complete the 4 functions below following the instructions in the *docstrings*. Good luck and keep calm and parse your Data in Python.

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`stock_data`. **Run** checks the first three tests. **Submit** checks all 8 tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
