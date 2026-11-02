## Reference solution

```python
import configparser

# FOCUS: load the file with configparser and write the three read-only properties by hand.
# SUPPLIED: the two list helpers below do the splitting and the duplicate removal.
#        They are not the skill of this exercise. Use them. Do not edit them.


def _unique(values):
    """Drop None, empty strings and repeats. Keep first-seen order: ['a', None, 'a', 'b'] -> ['a', 'b']."""
    return [value for value in dict.fromkeys(values) if value]


def _split_list(text):
    """Split on commas and newlines, strip spaces, then _unique: 'a, b\n c,a' -> ['a', 'b', 'c']."""
    return _unique(item.strip() for item in text.replace("\n", ",").split(","))


class ToxIniParser:

    def __init__(self, ini_file):
        """Use configparser to load ini_file into self.config"""
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(ini_file)

    @property
    def number_of_sections(self):
        return len(self.config.sections())

    @property
    def environments(self):
        return _split_list(self.config["tox"].get("envlist", ""))

    @property
    def base_python_versions(self):
        return _unique(self.config[s].get("basepython") for s in self.config.sections())
```
