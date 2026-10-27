## Approach

The constructor walks the lines once with two pieces of state: the current
section and the last key. The fixed order of the checks resolves overlaps: comments first, then
indentation, then headers, then `=`. Any unclassified line raises, so a broken file never creates
an object. The query methods read the nested dictionaries; `get_list` splits on both separators
with one regular expression. Parsing is O(total text length).

## Reference classes

```python
import re


class IniConfig:
    def __init__(self, text: str):
        self._data: dict[str, dict[str, str]] = {}
        section = key = None
        for number, line in enumerate(text.split("\n"), start=1):
            stripped = line.strip(" \t")
            if not stripped or stripped[0] in "#;":
                continue
            if line[0] in " \t":
                if key is None:
                    raise ValueError(f"line {number}: continuation without a key")
                current = self._data[section][key]
                self._data[section][key] = f"{current}\n{stripped}" if current else stripped
            elif stripped.startswith("[") and stripped.endswith("]"):
                name = stripped[1:-1].strip(" \t")
                if not name or name in self._data:
                    raise ValueError(f"line {number}: empty or repeated section {name!r}")
                self._data[name] = {}
                section, key = name, None
            elif "=" in line:
                name, _, value = line.partition("=")
                name = name.strip(" \t")
                if section is None or not name or name in self._data[section]:
                    raise ValueError(f"line {number}: invalid key {name!r}")
                self._data[section][name] = value.strip(" \t")
                key = name
            else:
                raise ValueError(f"line {number}: cannot parse {line!r}")

    @property
    def sections(self) -> list[str]:
        return list(self._data)

    def keys(self, section: str) -> list[str]:
        return list(self._data[section])

    def get(self, section: str, key: str, default=None):
        return self._data.get(section, {}).get(key, default)

    def get_list(self, section: str, key: str) -> list[str]:
        items = re.split(r"[\n,]", self._data[section][key])
        return [item.strip(" \t") for item in items if item.strip(" \t")]

    def __contains__(self, section: object) -> bool:
        return section in self._data
```
