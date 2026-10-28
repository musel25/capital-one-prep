This will be a quick Bite showing you how to create a beautiful table with [Rich](https://github.com/Textualize/rich).

You might be surprised how easy it is and it might come in handy when improving your CLI.

Refer to the [Rich table documentation](https://typer.tiangolo.com/tutorial/printing/#rich-tables) for more help.

Enjoy!

PS: You may need to adjust the width of the rows to pass the tests.

**Constraints:**

- Implement `create_table(rows)` and `show_table(rows)` for `(name, age, city)` rows. Names and cities have 1–20 printable characters; ages are integers from 0 through 120. Return a Rich `Table` titled `People`, with `Name`, `Age`, `City` columns. Convert cells to strings and preserve order and duplicates. Empty input keeps the headers.
- `show_table` prints with `Console(width=80, color_system=None)`. The single-command `app` prints the supplied `PEOPLE` rows. Tests check data and visible content; the border drawing can vary.
