"""Original exercise: matrix multiplication with the @ operator."""
from cojudge.oop.steps import builtin, call, case, error, get, new, obj, op, ref

SPEC = {
    "number": 19, "slug": "matrix-matmul", "title": "Matrix multiplication with @",
    "difficulty": "Medium", "time": 35, "level": 4,
    "prerequisites": "Exercise 17. Operator dunder methods and `NotImplemented`.",
    "learn": """Python has an operator only for matrix multiplication: `a @ b` calls
`a.__matmul__(b)`. No built-in type uses it; libraries such as NumPy do. Your own class can too.

For an `m × n` matrix `A` and an `n × p` matrix `B`, the product `C = A @ B` is `m × p`. Each
entry is a row of `A` times a column of `B`:

```text
C[i][j] = A[i][0]*B[0][j] + A[i][1]*B[1][j] + ... + A[i][n-1]*B[n-1][j]
```

The inner sizes must match (`n`). `zip(*rows)` turns rows into columns, which makes the formula
short: `sum(a * b for a, b in zip(row, col))`.

A class that stores a list must protect it. Copy the rows when you receive them and when you
return them, so outside code cannot change the matrix.""",
    "scenario": """A small graphics engine transforms points with matrices: rotate, scale, and move.
Several transformations combine into one matrix by multiplication. The engine has no external
packages, so it needs its own `Matrix` type.""",
    "task": """Write the class `Matrix`. Entries are integers.

- `Matrix(rows)`: `rows` is a non-empty list of non-empty lists, all with the same length;
  otherwise raise `ValueError`. Keep your own copy.
- `shape`: read-only property. `(row_count, column_count)`.
- `rows`: read-only property. A new list of new lists. A change to the result must not change the
  matrix.
- `Matrix.identity(n)`: **class method**. The `n × n` identity matrix (1 on the diagonal, 0
  elsewhere). `n` below 1 raises `ValueError`.
- `transpose()`: a new matrix with rows and columns exchanged.
- `a @ b`: a new matrix, the product. If the column count of `a` is not the row count of `b`,
  raise `ValueError`. A non-`Matrix` operand gives `TypeError` (return `NotImplemented`).
- `a == b`: `True` when the entries are equal. For a non-`Matrix`, return `NotImplemented`.
- `repr`: `Matrix([[1, 2], [3, 4]])`.""",
    "constraints": ["At most 8 rows and 8 columns.", "Entries are from -1000 to 1000.", "At most 30 steps per test."],
    "hints": ["`[list(col) for col in zip(*rows)]` is the transpose.",
              "`f\"Matrix({self._rows!r})\"` gives the required repr for a list of lists of integers."],
    "starter": '''class Matrix:
    def __init__(self, rows: list[list[int]]):
        raise NotImplementedError

    @property
    def shape(self) -> tuple[int, int]:
        raise NotImplementedError

    @property
    def rows(self) -> list[list[int]]:
        raise NotImplementedError

    @classmethod
    def identity(cls, n: int) -> "Matrix":
        raise NotImplementedError

    def transpose(self) -> "Matrix":
        raise NotImplementedError

    def __matmul__(self, other: "Matrix") -> "Matrix":
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
''',
    "reference": '''class Matrix:
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
''',
    "facts": ["classmethod Matrix identity", "property Matrix shape", "property Matrix rows"],
    "java": '''static class Matrix implements Obj {
    long[][] a;
    public String type() { return "Matrix"; }
    Matrix(long[][] a) { this.a = a; }
    static Matrix of(Object raw) {
        List<Object> rows = arr(raw);
        if (rows.isEmpty() || arr(rows.get(0)).isEmpty()) throw err("ValueError");
        int c = arr(rows.get(0)).size();
        long[][] a = new long[rows.size()][c];
        for (int i = 0; i < rows.size(); i++) {
            List<Object> r = arr(rows.get(i));
            if (r.size() != c) throw err("ValueError");
            for (int j = 0; j < c; j++) a[i][j] = lng(r.get(j));
        }
        return new Matrix(a);
    }
    List<Object> rows() { List<Object> out = new ArrayList<>(); for (long[] r : a) { List<Object> row = new ArrayList<>(); for (long v : r) row.add(v); out.add(row); } return out; }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) return Matrix.of(arg(op, 0, "rows", MISSING));
    if (d.equals("call") && t instanceof String && s(op.get("method")).equals("identity")) {
        int n = (int) lng(args(op).get(0));
        if (n < 1) throw err("ValueError");
        long[][] a = new long[n][n]; for (int i = 0; i < n; i++) a[i][i] = 1; return new Matrix(a);
    }
    if (t instanceof List && d.equals("call") && s(op.get("method")).equals("append")) { arr(t).add(args(op).get(0)); return null; }
    if (d.equals("op")) {
        Object l = val(op.get("left")), r = val(op.get("right"));
        String sym = s(op.get("op"));
        if (sym.equals("==") || sym.equals("!=")) {
            boolean eq = l instanceof Matrix && r instanceof Matrix ? Arrays.deepEquals(((Matrix) l).a, ((Matrix) r).a) : l == r;
            return sym.equals("==") ? eq : !eq;
        }
        if (!(l instanceof Matrix && r instanceof Matrix)) throw err("TypeError");
        long[][] x = ((Matrix) l).a, y = ((Matrix) r).a;
        if (x[0].length != y.length) throw err("ValueError");
        long[][] out = new long[x.length][y[0].length];
        for (int i = 0; i < x.length; i++) for (int j = 0; j < y[0].length; j++) for (int k = 0; k < y.length; k++) out[i][j] += x[i][k] * y[k][j];
        return new Matrix(out);
    }
    Matrix m = (Matrix) t;
    if (d.equals("get")) {
        String a = s(op.get("attr"));
        if (a.equals("shape")) return list((long) m.a.length, (long) m.a[0].length);
        if (a.equals("rows")) return m.rows();
    }
    if (d.equals("call") && s(op.get("method")).equals("transpose")) {
        long[][] out = new long[m.a[0].length][m.a.length];
        for (int i = 0; i < m.a.length; i++) for (int j = 0; j < m.a[0].length; j++) out[j][i] = m.a[i][j];
        return new Matrix(out);
    }
    if (d.equals("repr")) {
        StringBuilder sb = new StringBuilder("Matrix([");
        for (int i = 0; i < m.a.length; i++) {
            sb.append(i > 0 ? ", [" : "[");
            for (int j = 0; j < m.a[i].length; j++) sb.append(j > 0 ? ", " : "").append(m.a[i][j]);
            sb.append("]");
        }
        return sb.append("])").toString();
    }
    throw err("AttributeError");
}
''',
    "approach": """The constructor validates the rectangle and copies every row; `rows` copies again
on the way out, so the matrix owns its data. `@` checks the operand type first (returning
`NotImplemented` for foreign types), then the inner dimension. The product uses the columns of
the right matrix from `zip(*rows)`. For m×n by n×p it costs O(m·n·p).""",
    "example_notes": [
        "A 2×3 matrix times a 3×2 matrix gives a 2×2 matrix. Entry [0][0] is 1·7 + 2·9 + 3·11 = 58.",
        "Multiplying by the identity matrix returns an equal matrix.",
        "A 2×3 matrix cannot multiply another 2×3 matrix: 3 columns, 2 rows. A plain list gives TypeError.",
    ],
    "cases": [
        case("2x3 times 3x2",
             (new("Matrix", [[1, 2, 3], [4, 5, 6]], save="a"), obj("Matrix")), (new("Matrix", [[7, 8], [9, 10], [11, 12]], save="b"), obj("Matrix")),
             (op(ref("a"), "@", ref("b"), save="c"), obj("Matrix")), (builtin("repr", "c"), "Matrix([[58, 64], [139, 154]])"),
             (get("c", "shape"), [2, 2])),
        case("identity",
             (new("Matrix", [[2, -1], [0, 3]], save="a"), obj("Matrix")), (call("Matrix", "identity", 2, save="i"), obj("Matrix")),
             (op(ref("a"), "@", ref("i"), save="b"), obj("Matrix")), (op(ref("a"), "==", ref("b")), True),
             (builtin("repr", "i"), "Matrix([[1, 0], [0, 1]])")),
        case("shape mismatch and wrong type",
             (new("Matrix", [[1, 2, 3], [4, 5, 6]], save="a"), obj("Matrix")), (op(ref("a"), "@", ref("a")), error("ValueError")),
             (op(ref("a"), "@", [[1], [2], [3]]), error("TypeError"))),
        case("invalid shapes",
             (new("Matrix", []), error("ValueError")), (new("Matrix", [[]]), error("ValueError")),
             (new("Matrix", [[1, 2], [3]]), error("ValueError")), (call("Matrix", "identity", 0), error("ValueError"))),
        case("rows is a copy",
             (new("Matrix", [[1, 2]], save="a"), obj("Matrix")), (get("a", "rows", save="r"), [[1, 2]]),
             (call("r", "append", [3, 4]), None), (get("a", "rows"), [[1, 2]]), (get("a", "shape"), [1, 2])),
        case("transpose",
             (new("Matrix", [[1, 2, 3], [4, 5, 6]], save="a"), obj("Matrix")), (call("a", "transpose", save="t"), obj("Matrix")),
             (get("t", "rows"), [[1, 4], [2, 5], [3, 6]]), (get("t", "shape"), [3, 2]), (get("a", "shape"), [2, 3])),
        case("row times column",
             (new("Matrix", [[1, 2, 3]], save="r"), obj("Matrix")), (new("Matrix", [[4], [5], [6]], save="c"), obj("Matrix")),
             (op(ref("r"), "@", ref("c"), save="dot"), obj("Matrix")), (get("dot", "rows"), [[32]]),
             (op(ref("c"), "@", ref("r"), save="outer"), obj("Matrix")), (get("outer", "rows"), [[4, 8, 12], [5, 10, 15], [6, 12, 18]])),
        case("multiplication is not commutative",
             (new("Matrix", [[0, 1], [0, 0]], save="a"), obj("Matrix")), (new("Matrix", [[0, 0], [1, 0]], save="b"), obj("Matrix")),
             (op(ref("a"), "@", ref("b"), save="ab"), obj("Matrix")), (op(ref("b"), "@", ref("a"), save="ba"), obj("Matrix")),
             (get("ab", "rows"), [[1, 0], [0, 0]]), (get("ba", "rows"), [[0, 0], [0, 1]]), (op(ref("ab"), "==", ref("ba")), False)),
        case("negative entries and 1x1",
             (new("Matrix", [[-3]], save="a"), obj("Matrix")), (new("Matrix", [[-1000]], save="b"), obj("Matrix")),
             (op(ref("a"), "@", ref("b"), save="c"), obj("Matrix")), (builtin("repr", "c"), "Matrix([[3000]])")),
        case("equality with other types",
             (new("Matrix", [[1]], save="a"), obj("Matrix")), (op(ref("a"), "==", [[1]]), False), (op(ref("a"), "!=", 1), True),
             (new("Matrix", [[1]], save="b"), obj("Matrix")), (op(ref("a"), "==", ref("b")), True)),
        case("chain of transformations",
             (new("Matrix", [[2, 0], [0, 2]], save="scale"), obj("Matrix")), (new("Matrix", [[0, -1], [1, 0]], save="rot"), obj("Matrix")),
             (op(ref("rot"), "@", ref("scale"), save="m"), obj("Matrix")), (new("Matrix", [[3], [1]], save="p"), obj("Matrix")),
             (op(ref("m"), "@", ref("p"), save="q"), obj("Matrix")), (get("q", "rows"), [[-2], [6]])),
        case("identity 3 and transpose twice",
             (call("Matrix", "identity", 3, save="i"), obj("Matrix")), (get("i", "rows"), [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
             (new("Matrix", [[1, 2], [3, 4], [5, 6]], save="a"), obj("Matrix")), (call("a", "transpose", save="t"), obj("Matrix")),
             (call("t", "transpose", save="tt"), obj("Matrix")), (op(ref("tt"), "==", ref("a")), True)),
    ],
    "generate": lambda rng: (lambda m, n, p: (
        [new("Matrix", [[rng.randint(-9, 9) for _ in range(n)] for _ in range(m)], save="a"),
         new("Matrix", [[rng.randint(-9, 9) for _ in range(p)] for _ in range(rng.choice([n, n, n, p]))], save="b")]
        + [rng.choice([op(ref("a"), "@", ref("b"), save="c"), builtin("repr", "c"), get("c", "rows"), call("a", "transpose", save="a"),
                       get("a", "shape"), op(ref("a"), "==", ref("b")), call("Matrix", "identity", rng.randint(1, 4), save="b")])
           for _ in range(rng.randint(3, 9))]))(rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 4)),
    "mutations": [
        {"name": "dimension check skipped", "old": "        if self.shape[1] != other.shape[0]:\n", "new": "        if False:\n"},
        {"name": "rows returned directly", "old": "        return [list(row) for row in self._rows]\n", "new": "        return self._rows\n"},
        {"name": "uses rows of the right matrix", "old": "columns = list(zip(*other._rows))", "new": "columns = other._rows"},
        {"name": "ragged rows accepted", "old": "any(len(row) != len(rows[0]) for row in rows)", "new": "False"},
    ],
    "sources": ["https://docs.python.org/3.11/reference/datamodel.html#object.__matmul__",
                "https://peps.python.org/pep-0465/"],
}
