## Reference solution

Paste above the supplied tests and runner.

```python
import typer
from rich.table import Table
from rich.console import Console
from rich.text import Text

app = typer.Typer()
PEOPLE = [("Alice", 30, "London"), ("Bob", 25, "Paris")]


def create_table(rows):
    table = Table(title="People")
    for header in ("Name", "Age", "City"):
        table.add_column(header)
    for name, age, city in rows:
        table.add_row(Text(str(name)), Text(str(age)), Text(str(city)))
    return table


def show_table(rows):
    Console(width=80, color_system=None).print(create_table(rows))


@app.command()
def main():
    show_table(PEOPLE)
```
