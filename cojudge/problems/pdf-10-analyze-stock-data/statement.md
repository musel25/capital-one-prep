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

The supplied small JSON fixture replaces the external stock data.

**Constraints:**

- `get_stock_data` decodes JSON; sector filtering preserves input order; market distribution counts records.
- For the largest cap, compare M/B/T suffixes numerically, ignore `n/a`, keep the first tie, and return `None` if none are known.
