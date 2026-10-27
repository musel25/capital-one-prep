## Approach

Each mixin does one step and calls `super().format`, so the classes form one
chain in MRO order. For `Alert` the MRO is Alert, Shout, Tag, Trim, Formatter: `Shout` waits for
the rest of the chain and then uppercases everything, including the tag. `Trim` strips before it
passes the text on. `Tag` reads `self.tag`, which finds `Alert.tag` first. If one class returned
a value without `super()`, every class after it in the MRO would be skipped.

## Reference classes

```python
class Formatter:
    def format(self, text: str) -> str:
        return text


class Trim(Formatter):
    def format(self, text: str) -> str:
        return super().format(text.strip())


class Shout(Formatter):
    def format(self, text: str) -> str:
        return super().format(text).upper() + "!"


class Tag(Formatter):
    tag = "info"

    def format(self, text: str) -> str:
        return f"[{self.tag}] " + super().format(text)


class Alert(Shout, Tag, Trim):
    tag = "alert"


class Note(Tag, Trim):
    pass
```
