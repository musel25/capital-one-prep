## Reference solution

```python
class Matrix(object):

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return f'<Matrix values="{self.values}">'

    @staticmethod
    def _multiply(left, right):
        columns = list(zip(*right))
        return [[sum(a * b for a, b in zip(row, col)) for col in columns] for row in left]

    def __matmul__(self, other):
        return Matrix(self._multiply(self.values, other.values))

    def __rmatmul__(self, other):
        return Matrix(self._multiply(other, self.values))

    def __imatmul__(self, other):
        self.values = self._multiply(self.values, other.values)
        return self
```
