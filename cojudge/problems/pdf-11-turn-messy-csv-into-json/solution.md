## Reference solution

Paste this code above the supplied tests and runner.

```python
import json
import re

# FOCUS: build the list of dicts by hand and return json.dumps(...).
# SUPPLIED: _fields splits one row on the three delimiters. It is not the skill
#        of this exercise. Use it. Do not edit it.


def _fields(line):
    """'1,Junie|Kybert;j@x.mil' -> ['1', 'Junie', 'Kybert', 'j@x.mil']. Spaces are kept."""
    return re.split(r'[,|;]', line)

members = 'id,first_name,last_name,email\n1,Junie|Kybert;jkybert0@army.mil\n2|Sid;Churching,schurching1@tumblr.com\n3;Cherry,Dudbridge|cdudbridge2@nifty.com\n4,Ada|Stone;ada@example.test\n5|Lin;River,lin@example.test\n6;Sam,Oak|sam@example.test\n7,Noor|Vale;noor@example.test\n8|Eli;Moon,eli@example.test\n9;Luz,Sun|luz@example.test\n10,Bo|Lake;bo@example.test\n'


def convert_to_json(data=members):
    lines = [line for line in data.splitlines() if line.strip()]
    if not lines:
        return json.dumps([])
    header = lines[0].split(',')
    rows = []
    for line in lines[1:]:
        values = _fields(line)
        if len(values) != len(header):
            raise ValueError('Row has a different field count from the header')
        rows.append(dict(zip(header, values)))
    return json.dumps(rows)
```
