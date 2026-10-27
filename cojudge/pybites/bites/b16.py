"""Bite: Matrix multiplication / @ operator (recreated tests and template)."""

SPEC = {
    "title": "Matrix multiplication / @ operator",
    "module": "matmul",
    "template": '''class Matrix(object):

    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return f'<Matrix values="{self.values}">'
''',
    "tests": '''import pytest

from matmul import Matrix

A = [[1, 2], [3, 4]]
B = [[11, 12], [13, 14]]
AB = [[37, 40], [85, 92]]


def test_matmul():
    result = Matrix(A) @ Matrix(B)
    assert isinstance(result, Matrix)
    assert result.values == AB


def test_matmul_does_not_change_operands():
    a, b = Matrix([row[:] for row in A]), Matrix([row[:] for row in B])
    a @ b
    assert a.values == A
    assert b.values == B


def test_not_commutative():
    assert (Matrix(B) @ Matrix(A)).values == [[47, 70], [55, 82]]


def test_rmatmul():
    """A plain list of lists on the left uses Matrix.__rmatmul__."""
    result = A @ Matrix(B)
    assert isinstance(result, Matrix)
    assert result.values == AB


def test_imatmul():
    a = Matrix([row[:] for row in A])
    original = a
    a @= Matrix(B)
    assert a is original
    assert a.values == AB


def test_non_square():
    left = Matrix([[1, 2, 3], [4, 5, 6]])
    right = Matrix([[7, 8], [9, 10], [11, 12]])
    assert (left @ right).values == [[58, 64], [139, 154]]
    assert (right @ left).values == [[39, 54, 69], [49, 68, 87], [59, 82, 105]]


def test_identity_and_vector():
    identity = Matrix([[1, 0], [0, 1]])
    assert (Matrix(A) @ identity).values == A
    assert (Matrix(A) @ Matrix([[1], [1]])).values == [[3], [7]]


def test_repr():
    assert repr(Matrix(A) @ Matrix(B)) == '<Matrix values="[[37, 40], [85, 92]]">'
''',
    "reference": '''class Matrix(object):

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
''',
}
