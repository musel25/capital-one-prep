## Reference solution

```python
import configparser


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
        raw = self.config["tox"].get("envlist", "")
        items = [item.strip() for item in raw.replace("\n", ",").split(",")]
        return list(dict.fromkeys(item for item in items if item))

    @property
    def base_python_versions(self):
        values = (self.config[s].get("basepython") for s in self.config.sections())
        return list(dict.fromkeys(v.strip() for v in values if v))
```
