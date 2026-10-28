## Reference solution

Paste above the supplied tests and runner.

```python
import typer


def main(a: int = typer.Argument(..., help="The value of the first summand"),
         b: int = typer.Argument(..., help="The value of the second summand")):
    """CLI that allows you to add two numbers."""
    typer.echo(f"The sum is {a + b}")


app = typer.Typer()
app.command()(main)
```
