## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import date, datetime
def years_ago(date_string, reference=date(2018, 8, 1)):
    born = date.fromisoformat(date_string)
    if born > reference:
        raise ValueError('Future date')
    return reference.year - born.year - ((reference.month, reference.day) < (born.month, born.day))
def convert_eu_to_us_date(value):
    dt = datetime.strptime(value, '%d/%m/%Y')
    return f'{dt.month:02}/{dt.day:02}/{dt.year:04}'
```
