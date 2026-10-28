## Reference solution

Paste this code above the supplied tests and runner.

```python
import xml.etree.ElementTree as ET

XML = '<root response="True"><movie title="Memento" year="2000" runtime="113 min"/><movie title="The Dark Knight" year="2008" runtime="152 min"/><movie title="Interstellar" year="2014" runtime="169 min"/></root>'

def get_tree(xml=XML):
    return ET.fromstring(xml)

def get_movies(tree):
    return [dict(node.attrib) for node in tree.iter('movie')]

def get_movie_longest_runtime(movies):
    known = [movie for movie in movies if movie['runtime'] != 'N/A']
    return max(known, key=lambda movie: int(movie["runtime"].split()[0]), default=None)
```
