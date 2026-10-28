## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import date, datetime
import re
NOW = date(2019, 1, 1)
WEEKS_PER_YEAR = 52
def get_number_books_read(goal, at_date=NOW):
    if type(goal) is not int or goal <= 0:
        raise ValueError('Positive integer goal required')
    value = at_date
    if isinstance(value, str):
        cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', value)
        if ',' in cleaned:
            cleaned = cleaned.split(',', 1)[1].strip()
        for pattern in ('%Y-%m-%d', '%m-%d-%Y', '%B %d, %Y'):
            try:
                value = datetime.strptime(cleaned, pattern).date()
                break
            except ValueError:
                pass
    if type(value) is not date or value < NOW:
        raise ValueError('Valid current or future date required')
    return int(round(value.isocalendar().week / WEEKS_PER_YEAR * goal))
```
