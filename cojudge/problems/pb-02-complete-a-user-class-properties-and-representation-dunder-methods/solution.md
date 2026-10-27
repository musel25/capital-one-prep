## Reference solution

```python
class User:
    """A User class
       (Django's User model inspired us)
    """

    def __init__(self, first_name, last_name):
        """Constructor, base values"""
        self.first_name = first_name
        self.last_name = last_name

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def username(self):
        return (self.first_name[0] + self.last_name[:7]).lower()

    def __str__(self):
        return f"{self.get_full_name} ({self.username})"

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.first_name}", "{self.last_name}")'
```
