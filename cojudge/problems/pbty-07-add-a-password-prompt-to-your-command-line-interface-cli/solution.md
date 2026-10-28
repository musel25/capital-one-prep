## Reference solution

Paste above the supplied tests and runner.

```python
import typer

app = typer.Typer()


@app.command()
def main(username: str = typer.Option(..., prompt="Username"),
         password: str = typer.Option(..., prompt="Password", hide_input=True, confirmation_prompt=True)):
    typer.echo(f"Authenticated as {username}")
```
