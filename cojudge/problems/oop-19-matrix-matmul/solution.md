## Approach

The constructor validates the rectangle and copies every row; `rows` copies again
on the way out, so the matrix owns its data. `@` checks the operand type first (returning
`NotImplemented` for foreign types), then the inner dimension. The product uses the columns of
the right matrix from `zip(*rows)`. For m×n by n×p it costs O(m·n·p).

## Reference classes

```python
class Matrix:
    def __init__(self, rows: list[list[int]]):
        if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
            raise ValueError("rows must be a non-empty rectangle")
        self._rows = [list(row) for row in rows]

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._rows), len(self._rows[0])

    @property
    def rows(self) -> list[list[int]]:
        return [list(row) for row in self._rows]

    @classmethod
    def identity(cls, n: int) -> "Matrix":
        if n < 1:
            raise ValueError("size must be at least 1")
        return cls([[int(i == j) for j in range(n)] for i in range(n)])

    def transpose(self) -> "Matrix":
        return Matrix([list(col) for col in zip(*self._rows)])

    def __matmul__(self, other: "Matrix") -> "Matrix":
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape[1] != other.shape[0]:
            raise ValueError(f"cannot multiply {self.shape} by {other.shape}")
        columns = list(zip(*other._rows))
        return Matrix([[sum(a * b for a, b in zip(row, col)) for col in columns] for row in self._rows])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self._rows == other._rows

    def __repr__(self) -> str:
        return f"Matrix({self._rows!r})"
```
