"""Recreated Typer exercises. Contracts resolve details absent from public pages."""
COMMON = '''import typer
from typer.testing import CliRunner
import cli

runner = CliRunner()

def invoke(args, input=None):
    return runner.invoke(cli.app, args, input=input, color=False)
'''

SPECS = []


def add(contract, template, reference, tests, mutations):
    SPECS.append(dict(module='cli', contract=contract, template=template, reference=reference,
                      tests=COMMON + tests, mutations=mutations))


add(
'''Implement `main(a, b)` with two required integer CLI arguments. Add help text
`The value of the first summand` and `The value of the second summand`.
Print `The sum is N`. Export `app`, a Typer application with `main` registered as
its single command. You can also call `typer.run(main)` from a guarded script entry point.
Accept negative integers. Reject missing or non-integer values.''',
'''import typer


def main(a: int = typer.Argument(..., help="The value of the first summand"),
         b: int = typer.Argument(..., help="The value of the second summand")):
    """CLI that allows you to add two numbers."""
    # Print the sum.
    pass


app = typer.Typer()
app.command()(main)
''',
'''import typer


def main(a: int = typer.Argument(..., help="The value of the first summand"),
         b: int = typer.Argument(..., help="The value of the second summand")):
    """CLI that allows you to add two numbers."""
    typer.echo(f"The sum is {a + b}")


app = typer.Typer()
app.command()(main)
''',
'''
import pytest

@pytest.mark.parametrize("args, expected", [(["3", "5"], "The sum is 8"),
    (["0", "0"], "The sum is 0"), (["--", "-4", "7"], "The sum is 3"),
    (["--", "-4", "-7"], "The sum is -11")])
def test_sum(args, expected):
    result = invoke(args)
    assert result.exit_code == 0, result.output
    assert result.output.strip() == expected

@pytest.mark.parametrize("args", [[], ["2"], ["two", "3"], ["1.5", "2"]])
def test_invalid_arguments(args):
    assert invoke(args).exit_code != 0

def test_help():
    result = invoke(["--help"])
    assert result.exit_code == 0
    assert "first summand" in result.output and "second summand" in result.output
''',
[dict(name='subtract instead of add', old='a + b', new='a - b')])

TWO = '''import typer

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
'''
add(
'''Export a Typer `app` with `sum a b` and `compare c d`. All four arguments are
required integers. `sum` prints `The sum is N`. `compare` prints
`c=C is greater than d=D`, `d=D is greater than c=C`, or `c=C is equal to d=D`.
Use the actual integer values in these messages. Reject unknown commands and invalid inputs.''',
'''import typer

app = typer.Typer()


@app.command(name="sum")
def sum_numbers(a: int, b: int):
    pass


@app.command()
def compare(c: int, d: int):
    pass
''', TWO,
'''
import pytest

@pytest.mark.parametrize("args, expected", [(["sum", "3", "5"], "The sum is 8"),
    (["sum", "--", "-2", "2"], "The sum is 0"),
    (["compare", "3", "5"], "d=5 is greater than c=3"),
    (["compare", "8", "2"], "c=8 is greater than d=2"),
    (["compare", "4", "4"], "c=4 is equal to d=4"),
    (["compare", "--", "-3", "-1"], "d=-1 is greater than c=-3")])
def test_commands(args, expected):
    result = invoke(args)
    assert result.exit_code == 0, result.output
    assert result.output.strip() == expected

@pytest.mark.parametrize("args", [["sum", "1"], ["compare", "x", "2"], ["unknown"]])
def test_reject_bad_command(args):
    assert invoke(args).exit_code != 0

def test_help_lists_both_commands():
    result = invoke(["--help"])
    assert result.exit_code == 0
    assert "sum" in result.output and "compare" in result.output
''',
[dict(name='equality handled as greater', old='elif d > c:', new='elif d >= c:')])

PROGRESS = '''import typer

app = typer.Typer()


@app.command()
def main(count: int = typer.Argument(..., min=0, max=100),
         label: str = typer.Option("Processing")):
    with typer.progressbar(range(count), label=label) as items:
        for item in items:
            pass
    typer.echo(f"Processed {count} items")
'''
add(
'''Create a single-command Typer `app`. Its `main` command takes a required
integer `count` from 0 through 100, and an optional `--label` (default `Processing`).
Use `with typer.progressbar(range(count), label=label) as items` and iterate over
`items` once. Do not sleep. After the bar closes, print `Processed N items`.
A non-terminal test can show only the label. The tests also check the iterable
passed to the real progress bar and the items consumed from it.''',
'''import typer

app = typer.Typer()


@app.command()
def main(count: int = typer.Argument(..., min=0, max=100),
         label: str = typer.Option("Processing")):
    # Iterate through a Typer progress bar, then print the item count.
    pass
''', PROGRESS,
'''
import pytest

@pytest.mark.parametrize("count", [0, 1, 5, 100])
def test_count(count):
    result = invoke([str(count)])
    assert result.exit_code == 0, result.output
    assert f"Processed {count} items" in result.output

@pytest.mark.parametrize("args", [["--", "-1"], ["101"], ["abc"]])
def test_invalid_count(args):
    assert invoke(args).exit_code != 0

def test_progress_iterates_all_items_with_custom_label(monkeypatch):
    original = typer.progressbar
    seen, labels = [], []
    def observe(iterable, **kwargs):
        labels.append(kwargs.get("label"))
        def values():
            for value in iterable:
                seen.append(value)
                yield value
        return original(values(), length=4, **kwargs)
    monkeypatch.setattr(typer, "progressbar", observe)
    result = invoke(["4", "--label", "Importing"])
    assert result.exit_code == 0, result.output
    assert seen == [0, 1, 2, 3] and labels == ["Importing"]
    assert "Importing" in result.output
''',
[dict(name='skip progress iteration', old='for item in items:', new='for item in []:')])

OPTIONS = '''from typing import Optional
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
'''
add(
'''Export a single-command Typer `app` with required integer arguments `a` and `b`.
Add optional integer option `--c` with no value by default. Without `--c`, print
`The sum is N`. With `--c`, print `The sum is N and c is smaller`, `greater`, or
`equal`, according to `c` relative to the sum. Zero is a supplied value.
Invalid or missing required values must produce a nonzero exit code.''',
'''from typing import Optional
import typer

app = typer.Typer()


@app.command()
def main(a: int, b: int, c: Optional[int] = typer.Option(None)):
    pass
''', OPTIONS,
'''
import pytest

@pytest.mark.parametrize("args, expected", [(["2", "3"], "The sum is 5"),
    (["2", "3", "--c", "1"], "The sum is 5 and c is smaller"),
    (["2", "3", "--c", "8"], "The sum is 5 and c is greater"),
    (["2", "3", "--c", "5"], "The sum is 5 and c is equal"),
    (["2", "3", "--c", "0"], "The sum is 5 and c is smaller"),
    (["0", "0", "--c", "0"], "The sum is 0 and c is equal"),
    (["--c", "-2", "--", "-3", "1"], "The sum is -2 and c is equal")])
def test_option_comparison(args, expected):
    result = invoke(args)
    assert result.exit_code == 0, result.output
    assert result.output.strip() == expected

@pytest.mark.parametrize("args", [["1"], ["1", "2", "--c", "x"], ["1", "2", "3"]])
def test_reject_invalid_values(args):
    assert invoke(args).exit_code != 0
''',
[dict(name='treat zero option as absent', old='if c is not None:', new='if c:')])

CALLBACK = '''import typer

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
'''
add(
'''Export a multi-command Typer `app`. A root callback defines `--verbose` and `-v`,
both false by default. The option appears before the command. Share its value through
`ctx.obj`. Implement `sum a b` and `compare c d` with required integer arguments.
By default, print only the sum or the comparison result (`-1` if c < d, `0` if
c == d, `1` if c > d). With verbosity enabled, use the messages from exercise 2.
Each invocation must start with its own verbosity value.''',
'''import typer

app = typer.Typer()


@app.callback()
def configure(ctx: typer.Context, verbose: bool = typer.Option(False, "--verbose", "-v")):
    ctx.obj = {"verbose": verbose}


@app.command(name="sum")
def sum_numbers(ctx: typer.Context, a: int, b: int):
    pass


@app.command()
def compare(ctx: typer.Context, c: int, d: int):
    pass
''', CALLBACK,
'''
import pytest

@pytest.mark.parametrize("args, expected", [(["sum", "3", "5"], "8"),
    (["--verbose", "sum", "3", "5"], "The sum is 8"),
    (["-v", "sum", "0", "0"], "The sum is 0"),
    (["compare", "3", "5"], "-1"), (["compare", "5", "3"], "1"),
    (["compare", "3", "3"], "0"),
    (["--verbose", "compare", "3", "5"], "d=5 is greater than c=3"),
    (["-v", "compare", "5", "3"], "c=5 is greater than d=3"),
    (["-v", "compare", "3", "3"], "c=3 is equal to d=3")])
def test_callback_output(args, expected):
    result = invoke(args)
    assert result.exit_code == 0, result.output
    assert result.output.strip() == expected

def test_verbose_does_not_leak_between_invocations():
    assert invoke(["--verbose", "sum", "1", "2"]).output.strip() == "The sum is 3"
    assert invoke(["sum", "1", "2"]).output.strip() == "3"

def test_unknown_root_option():
    assert invoke(["--unknown", "sum", "1", "2"]).exit_code != 0
''',
[dict(name='always verbose', old='ctx.obj = {"verbose": verbose}', new='ctx.obj = {"verbose": True}')])

TABLE = '''import typer
from rich.table import Table
from rich.console import Console

app = typer.Typer()
PEOPLE = [("Alice", 30, "London"), ("Bob", 25, "Paris")]


def create_table(rows):
    table = Table(title="People")
    for header in ("Name", "Age", "City"):
        table.add_column(header)
    for name, age, city in rows:
        table.add_row(str(name), str(age), str(city))
    return table


def show_table(rows):
    Console(width=80, color_system=None).print(create_table(rows))


@app.command()
def main():
    show_table(PEOPLE)
'''
# A valid Table starter lets collection succeed but contains no requested columns/rows.
add(
'''Implement `create_table(rows)` and `show_table(rows)`. Each input row contains
`(name, age, city)`, with printable names and cities from 1 through 20 characters and
integer ages from 0 through 120. Return a real `rich.table.Table` titled `People`
with columns `Name`, `Age`, `City`, in this order. Convert cell values to strings.
Keep input order. Empty input still produces the column headers. `show_table` prints
the table with `Console(width=80, color_system=None)`. The single-command `app` prints
`PEOPLE`, supplied in the template. Tests check table data and visible content, not
one exact border drawing.''',
'''import typer
from rich.table import Table
from rich.console import Console

app = typer.Typer()
PEOPLE = [("Alice", 30, "London"), ("Bob", 25, "Paris")]


def create_table(rows):
    return Table()


def show_table(rows):
    pass


@app.command()
def main():
    show_table(PEOPLE)
''', TABLE,
'''
import io
from rich.table import Table
from rich.console import Console


def test_real_table_and_headers():
    table = cli.create_table([])
    assert isinstance(table, Table)
    assert table.title == "People"
    assert [c.header for c in table.columns] == ["Name", "Age", "City"]


def test_row_values_and_order():
    table = cli.create_table([("Zoe", 0, "Lima"), ("Ari", 120, "Rome")])
    assert table.row_count == 2
    assert [list(c.cells) for c in table.columns] == [["Zoe", "Ari"], ["0", "120"], ["Lima", "Rome"]]


def test_duplicate_rows_are_kept():
    table = cli.create_table([("Ana", 9, "Oslo"), ("Ana", 9, "Oslo")])
    assert table.row_count == 2


def test_show_table(capsys):
    cli.show_table([("Rene", 44, "Tokyo")])
    text = capsys.readouterr().out
    assert all(word in text for word in ["People", "Name", "Age", "City", "Rene", "44", "Tokyo"])


def test_cli_table():
    result = invoke([])
    assert result.exit_code == 0, result.output
    assert all(word in result.output for word in ["People", "Alice", "30", "London", "Bob", "25", "Paris"])


def test_unicode_cells():
    table = cli.create_table([("Müsel", 25, "México")])
    buffer = io.StringIO()
    Console(file=buffer, width=80, color_system=None).print(table)
    assert "Müsel" in buffer.getvalue() and "México" in buffer.getvalue()
''',
[dict(name='omit final row', old='for name, age, city in rows:', new='for name, age, city in list(rows)[:-1]:')])

PASSWORD = '''import typer

app = typer.Typer()


@app.command()
def main(username: str = typer.Option(..., prompt="Username"),
         password: str = typer.Option(..., prompt="Password", hide_input=True, confirmation_prompt=True)):
    typer.echo(f"Authenticated as {username}")
'''
add(
'''Export a single-command Typer `app`. Prompt for a required `--username` using
`Username`. Prompt for a required `--password` using `Password`. Hide password input
and require confirmation. On a mismatch, let Typer request the password again.
Accept explicit options without a prompt. On success, print `Authenticated as USERNAME`.
Never print the password. This exercise demonstrates prompt handling. It does not
connect to an authentication service. Ctrl-C or end-of-input must abort with a
nonzero exit code. Use only test credentials.''',
'''import typer

app = typer.Typer()


@app.command()
def main(username: str = typer.Option(..., prompt="Username"),
         password: str = typer.Option(..., prompt="Password", hide_input=True, confirmation_prompt=True)):
    # Print the success message. Never print the password.
    pass
''', PASSWORD,
'''
import pytest

@pytest.mark.parametrize("username", ["alice", "musel25", "user-name"])
def test_explicit_options(username):
    result = invoke(["--username", username, "--password", "test-secret-42"])
    assert result.exit_code == 0, result.output
    assert result.output.strip() == f"Authenticated as {username}"
    assert "test-secret-42" not in result.output


def test_hidden_password_and_confirmation():
    result = invoke([], input="alice\\nprivate-value\\nprivate-value\\n")
    assert result.exit_code == 0, result.output
    assert "Username" in result.output and "Password" in result.output
    assert "Repeat for confirmation" in result.output
    assert "Authenticated as alice" in result.output
    assert "private-value" not in result.output


def test_mismatch_retries_without_echoing_secrets():
    result = invoke(["--username", "bob"], input="wrong-value\\nother-value\\ncorrect-value\\ncorrect-value\\n")
    assert result.exit_code == 0, result.output
    assert "do not match" in result.output
    assert "Authenticated as bob" in result.output
    assert all(secret not in result.output for secret in ["wrong-value", "other-value", "correct-value"])


def test_end_of_input_aborts():
    # Click 8.1's test stream returns an empty string forever at EOF.
    # Supply a stream that raises EOFError, as the real terminal input does.
    import io
    class EndOfInput(io.BytesIO):
        def read1(self, *args):
            raise EOFError
    result = invoke([], input=EndOfInput())
    assert result.exit_code != 0
    assert "Authenticated as" not in result.output


def test_password_option_is_hidden_in_help():
    result = invoke(["--help"])
    assert result.exit_code == 0
    assert "--username" in result.output and "--password" in result.output
''',
[dict(name='leak password', old='typer.echo(f"Authenticated as {username}")',
      new='typer.echo(f"Authenticated as {username}: {password}")')])
