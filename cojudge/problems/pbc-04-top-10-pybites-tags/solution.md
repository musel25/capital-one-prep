## Reference solution

Paste this code above the supplied tests and runner.

```python
from collections import Counter
import xml.etree.ElementTree as ET

XML = '<rss><channel><item><category>Python</category><category>learning</category></item><item><category>Python</category><category>Flask</category><category>learning</category><category>Python</category></item></channel></rss>'

def get_top_tags(xml=XML, n=10):
    counts = Counter()
    for node in ET.fromstring(xml).iter('category'):
        tag = (node.text or '').strip()
        if tag:
            counts[tag] += 1
    return counts.most_common(n)
```
