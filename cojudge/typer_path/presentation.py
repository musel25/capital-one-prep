"""Concrete CLI calls and the few details absent from the public tasks."""

CLARIFICATIONS = {
    1: ('Export a Typer `app` with `main` registered as its single command. Accept negative integers and reject missing or non-integer arguments.',),
    2: ('Use required integer arguments. For equal inputs, print `c=C is equal to d=D` with the actual values.',),
    3: ('Export a single-command `app`. Require integer `count` from 0 through 100. Add `--label`, default `Processing`. Iterate once over `typer.progressbar(range(count), label=label)`, without a delay. After the bar closes, print `Processed N items`.',),
    4: ('Export a single-command `app`. Use integer arguments and integer option `--c` with default `None`. Include `c is smaller`, `c is greater`, or `c is equal` when `--c` is supplied. Zero is a supplied value.',),
    5: ('Add root options `--verbose` and `-v`, default false. Share their value through `ctx.obj`. Commands are `sum a b` and `compare c d`, with required integers. Without verbosity, print the sum or comparison result (`-1`, `0`, or `1`). With verbosity, use the messages from exercise 2. Reset verbosity for each invocation.',),
    6: ('Implement `create_table(rows)` and `show_table(rows)` for `(name, age, city)` rows. Names and cities have 1–20 printable characters; ages are integers from 0 through 120. Return a Rich `Table` titled `People`, with `Name`, `Age`, `City` columns. Convert cells to strings and preserve order and duplicates. Empty input keeps the headers.',
        '`show_table` prints with `Console(width=80, color_system=None)`. The single-command `app` prints the supplied `PEOPLE` rows. Tests check data and visible content; the border drawing can vary.'),
    7: ('Export a single-command `app`. Required options `--username` and `--password` prompt with `Username` and `Password`. Hide and confirm the password. After a mismatch, prompt again. Explicit options need no prompt. Print `Authenticated as USERNAME` on success. Never print the password. End-of-input or Ctrl-C must abort with a nonzero exit code.',),
}

CLI = 'from typer.testing import CliRunner\nrunner = CliRunner()\n'

EXAMPLES = {
    1: [(CLI + 'result = runner.invoke(app, ["3", "5"])\nprint(result.exit_code)\nprint(result.output, end="")', '0\nThe sum is 8')],
    2: [(CLI + 'result = runner.invoke(app, ["compare", "3", "5"])\nprint(result.exit_code)\nprint(result.output, end="")', '0\nd=5 is greater than c=3')],
    3: [(CLI + 'result = runner.invoke(app, ["3", "--label", "Importing"])\nprint(result.exit_code)\nprint(result.output, end="")', '0\nImporting\nProcessed 3 items')],
    4: [(CLI + 'result = runner.invoke(app, ["2", "3", "--c", "0"])\nprint(result.exit_code)\nprint(result.output, end="")', '0\nThe sum is 5 and c is smaller')],
    5: [(CLI + 'print(runner.invoke(app, ["sum", "3", "5"]).output, end="")\nprint(runner.invoke(app, ["--verbose", "sum", "3", "5"]).output, end="")', '8\nThe sum is 8')],
    6: [('table = create_table([("Zoe", 0, "Lima"), ("Ari", 120, "Rome")])\nprint(table.title)\nprint([column.header for column in table.columns])\nprint([[str(cell) for cell in column.cells] for column in table.columns])', "People\n['Name', 'Age', 'City']\n[['Zoe', 'Ari'], ['0', '120'], ['Lima', 'Rome']]")],
    7: [(CLI + 'result = runner.invoke(app, ["--username", "Ada", "--password", "test-password"])\nprint(result.exit_code)\nprint(result.output, end="")', '0\nAuthenticated as Ada')],
}
