## Reference solution

Paste this code above the supplied tests and runner.

```python
import re
from collections import defaultdict

# FOCUS: build the index by hand with defaultdict.
# SUPPLIED: _mentions does the regex match. It is not the skill of this
#        exercise. Use it. Do not edit it.


def _mentions(line, aliases):
    """True if any alias is in line as a whole word, any case: _mentions('The WOLF!', ('wolf',)) -> True."""
    pattern = r'\b(?:' + '|'.join(re.escape(alias) for alias in aliases) + r')\b'
    return re.search(pattern, line, re.IGNORECASE) is not None


def make_character_index(text, characters):
    index = defaultdict(list)
    for character in characters:
        aliases = (character,) if isinstance(character, str) else character
        for number, line in enumerate(text.splitlines(), 1):
            if _mentions(line, aliases):
                index[aliases[0]].append(number)
    return dict(index)
```
