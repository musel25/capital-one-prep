## Reference solution

Paste above the supplied tests and runner.

```python
import typer

app = typer.Typer()


@app.callback()
def configure(ctx: typer.Context, verbose: bool = typer.Option(False, "--verbose", "-v")):
    ctx.obj = {"verbose": verbose}


@app.command(name="sum")
def sum_numbers(ctx: typer.Context, a: int, b: int):
    total = a + b
    typer.echo(f"The sum is {total}" if ctx.obj["verbose"] else str(total))


@app.command()
def compare(ctx: typer.Context, c: int, d: int):
    if ctx.obj["verbose"]:
        if c > d:
            typer.echo(f"c={c} is greater than d={d}")
        elif d > c:
            typer.echo(f"d={d} is greater than c={c}")
        else:
            typer.echo(f"c={c} is equal to d={d}")
    else:
        typer.echo(str((c > d) - (c < d)))
```
