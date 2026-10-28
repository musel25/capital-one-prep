## Reference solution

Paste this code above the supplied tests and runner.

```python
import re
from collections import defaultdict

def make_character_index(text, characters):
    index = defaultdict(list)
    for character in characters:
        aliases = (character,) if isinstance(character, str) else character
        pattern = re.compile(r'\b(?:' + '|'.join(re.escape(alias) for alias in aliases) + r')\b', re.I)
        for number, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                index[aliases[0]].append(number)
    return dict(index)
```
