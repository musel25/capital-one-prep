## Reference solution

Paste above the supplied tests and runner.

```python
from typing import Optional
import typer

app = typer.Typer()


@app.command()
def main(a: int, b: int, c: Optional[int] = typer.Option(None)):
    total = a + b
    message = f"The sum is {total}"
    if c is not None:
        relation = "smaller" if c < total else "greater" if c > total else "equal"
        message += f" and c is {relation}"
    typer.echo(message)
```
