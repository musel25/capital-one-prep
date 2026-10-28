## Reference solution

Paste this code above the supplied tests and runner.

```python
import json
from collections import Counter

CAR_JSON = '[{"id": 1, "automaker": "Dodge", "model": "Ram Van 1500", "year": 1999}, {"id": 2, "automaker": "Chrysler", "model": "Town & Country", "year": 2002}, {"id": 3, "automaker": "Porsche", "model": "Cayenne", "year": 2008}, {"id": 4, "automaker": "Dodge", "model": "Charger", "year": 2008}, {"id": 5, "automaker": "Dodge", "model": "Avenger", "year": 2008}]'
CARS = json.loads(CAR_JSON)

def most_prolific_automaker(year, cars=CARS):
    counts = Counter(car['automaker'] for car in cars if car['year'] == year)
    return counts.most_common(1)[0][0] if counts else None

def get_models(automaker, year, cars=CARS):
    return [car['model'] for car in cars
            if car['automaker'] == automaker and car['year'] == year]
```
