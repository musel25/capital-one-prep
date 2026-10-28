## Reference solution

Paste above the supplied tests and runner.

```python
import typer

app = typer.Typer()


@app.command()
def main(count: int = typer.Argument(..., min=0, max=100),
         label: str = typer.Option("Processing")):
    with typer.progressbar(range(count), label=label) as items:
        for item in items:
            pass
    typer.echo(f"Processed {count} items")
```
