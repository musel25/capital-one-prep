## Reference solution

Paste above the supplied tests and runner.

```python
import typer

app = typer.Typer()


@app.command(name="sum")
def sum_numbers(a: int, b: int):
    typer.echo(f"The sum is {a + b}")


@app.command()
def compare(c: int, d: int):
    if c > d:
        typer.echo(f"c={c} is greater than d={d}")
    elif d > c:
        typer.echo(f"d={d} is greater than c={c}")
    else:
        typer.echo(f"c={c} is equal to d={d}")
```
