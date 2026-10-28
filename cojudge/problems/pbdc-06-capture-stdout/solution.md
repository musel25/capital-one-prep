## Reference solution

Use this implementation above the supplied tests and runner.

```python
from contextlib import redirect_stdout
from io import StringIO
import sys
from types import BuiltinFunctionType


def get_len_help_text(builtin):
    if not isinstance(builtin, BuiltinFunctionType):
        raise ValueError("expected a built-in function")
    output = StringIO()
    with redirect_stdout(output):
        help(builtin)
    return len(output.getvalue())
```
