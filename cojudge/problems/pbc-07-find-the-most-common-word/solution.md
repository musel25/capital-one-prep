## Reference solution

Paste this code above the supplied tests and runner.

```python
from collections import Counter

TEXT = "The wizard met the owl. The wizard waved."
STOPWORDS = {"the", "a", "and"}

def get_most_common_word(text=TEXT, stopwords=STOPWORDS):
    ignored = {word.lower() for word in stopwords}
    counts = Counter()
    for token in text.lower().split():
        word = ''.join(char for char in token if char.isalnum())
        if word and word not in ignored:
            counts[word] += 1
    return counts.most_common(1)[0] if counts else (None, 0)
```
