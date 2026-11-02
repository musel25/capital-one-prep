## Reference solution

Paste this code above the supplied tests and runner.

```python
from collections import Counter

TEXT = "The wizard met the owl. The wizard waved."
STOPWORDS = {"the", "a", "and"}

# FOCUS: count the words by hand with collections.Counter.
# SUPPLIED: _clean removes punctuation from one token. It is not the skill of
#        this exercise. Use it. Do not edit it.


def _clean(token):
    """Keep only letters and digits: _clean("can't,") == 'cant'. Case is not changed."""
    return ''.join(char for char in token if char.isalnum())


def get_most_common_word(text=TEXT, stopwords=STOPWORDS):
    ignored = {word.lower() for word in stopwords}
    counts = Counter()
    for token in text.lower().split():
        word = _clean(token)
        if word and word not in ignored:
            counts[word] += 1
    return counts.most_common(1)[0] if counts else (None, 0)
```
