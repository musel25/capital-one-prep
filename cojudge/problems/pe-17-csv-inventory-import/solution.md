## Reference solution

```python
import csv
import io


def parse_inventory(csv_text):
    rows = csv.reader(io.StringIO(csv_text, newline=""))
    next(rows, None)
    return [{"sku": row[0], "quantity": int(row[1])} for row in rows if row]
```
