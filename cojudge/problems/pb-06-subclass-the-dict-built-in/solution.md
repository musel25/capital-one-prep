## Reference solution

```python
from collections import UserDict

MSG = 'Hey {}, there are more people with your birthday!'


class BirthdayDict(UserDict):
    """Override UserDict to print a message every time a new person is added
       that has the same birthday (day+month) as somebody already in the dict"""

    def __setitem__(self, name, birthday):
        if any((d.month, d.day) == (birthday.month, birthday.day) for d in self.data.values()):
            print(MSG.format(name))
        super().__setitem__(name, birthday)
```
