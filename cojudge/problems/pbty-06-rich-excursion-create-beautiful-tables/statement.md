# 06. Rich excursion - create beautiful tables

[Course list](/?course=pybites-typer) · [Original bite](https://pybitesplatform.com/bites/rich-excursion-create-beautiful-tables/)

Implement `create_table(rows)` and `show_table(rows)`. Each input row contains
`(name, age, city)`, with printable names and cities from 1 through 20 characters and
integer ages from 0 through 120. Return a real `rich.table.Table` titled `People`
with columns `Name`, `Age`, `City`, in this order. Convert cell values to strings.
Keep input order. Empty input still produces the column headers. `show_table` prints
the table with `Console(width=80, color_system=None)`. The single-command `app` prints
`PEOPLE`, supplied in the template. Tests check table data and visible content, not
one exact border drawing.

**Source:** The original template and tests are not visible in this account.
This template and these tests are recreations based on the public description.
The contract above defines behavior that the public description does not specify.

<details>
<summary>Original public description</summary>

This will be a quick Bite showing you how to create a beautiful table with [Rich](https://github.com/Textualize/rich).

You might be surprised how easy it is and it might come in handy when improving your CLI.

Refer to the [Rich table documentation](https://typer.tiangolo.com/tutorial/printing/#rich-tables) for more help.

Enjoy!

PS: You may need to adjust the width of the rows to pass the tests.

</details>

Write your code at the top of the editor. The tests below it import your code as `cli`.
**Run** checks the first three tests. **Submit** checks all 7 tests.
A failure shows the test name, error, and test line.

- Python 3.11. The judge supplies real Typer 0.12.5, Click 8.1.7, and Rich 13.9.4.
- All libraries are bundled. No installation or network access is needed.
- Use the problem's Run and Submit actions. The playground and debugger do not load the library archive.
- Keep the supplied tests and runner. Guard any `typer.run(...)` or `app()` script entry point with `if __name__ == "__main__":`.
- The runner supports the pytest features used by these supplied tests. It is not a complete pytest installation.
