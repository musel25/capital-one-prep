## Reference solution

Paste this code above the supplied tests and runner.

```python
import json
from collections import Counter
from fractions import Fraction

STOCK_DATA = '[{"id": 1, "name": "Harbor Trust", "symbol": "HBR", "industry": "REIT", "sector": "Consumer Services", "market": "NYSE", "cap": "$600.57M"}, {"id": 2, "name": "Medical Tools", "symbol": "MED", "industry": "Instruments", "sector": "Health Care", "market": "NASDAQ", "cap": "$21.78M"}, {"id": 3, "name": "Cloud Works", "symbol": "CLD", "industry": "Software", "sector": "Technology", "market": "NASDAQ", "cap": "$2.1B"}, {"id": 4, "name": "Care Group", "symbol": "CARE", "industry": "Services", "sector": "Health Care", "market": "NYSE", "cap": "n/a"}, {"id": 5, "name": "Chip Works", "symbol": "CHP", "industry": "Semiconductors", "sector": "Technology", "market": "NASDAQ", "cap": "$950M"}]'


def get_stock_data(data=STOCK_DATA):
    return json.loads(data)


def get_stocks_by_sector(stocks, sector):
    return [stock for stock in stocks if stock['sector'] == sector]


def get_largest_stock(stocks):
    largest, highest = None, Fraction(-1)
    multipliers = {'M': 10**6, 'B': 10**9, 'T': 10**12}
    for stock in stocks:
        cap = stock['cap']
        if cap == 'n/a':
            continue
        suffix = cap[-1]
        value = Fraction(cap[1:-1]) * multipliers[suffix] if suffix in multipliers else Fraction(cap[1:])
        if value > highest:
            largest, highest = stock, value
    return largest


def get_market_distribution(stocks):
    return Counter(stock['market'] for stock in stocks)
```
