# 02. Create your first typer command line interface (cli) application

[Course list](/?course=pybites-typer) · [Original bite](https://pybitesplatform.com/bites/create-your-first-typer-command-line-interface-cli-application/)

Export a Typer `app` with `sum a b` and `compare c d`. All four arguments are
required integers. `sum` prints `The sum is N`. `compare` prints
`c=C is greater than d=D`, `d=D is greater than c=C`, or `c=C is equal to d=D`.
Use the actual integer values in these messages. Reject unknown commands and invalid inputs.

**Source:** The original template and tests are not visible in this account.
This template and these tests are recreations based on the public description.
The contract above defines behavior that the public description does not specify.

<details>
<summary>Original public description</summary>

In the previous Bites, you have successfully transformed an existing script into a CLI using `typer.run()`.

In this Bite, you will create a CLI application including more than one command to run, leveraging `app = typer.Typer()`. See the [Commands documentation](https://typer.tiangolo.com/tutorial/commands/) for reference.

So, create a command `sum` that sums two numbers and a command `compare` that compares two numbers:

```python
$ python script.py sum 3 5
The sum is 8

$ python script.py compare 3 5
d=5 is greater than c=3
```

Check out the tests for more information on how to format the output.

</details>

Write your code at the top of the editor. The tests below it import your code as `cli`.
**Run** checks the first three tests. **Submit** checks all 10 tests.
A failure shows the test name, error, and test line.

- Python 3.11. The judge supplies real Typer 0.12.5, Click 8.1.7, and Rich 13.9.4.
- All libraries are bundled. No installation or network access is needed.
- Use the problem's Run and Submit actions. The playground and debugger do not load the library archive.
- Keep the supplied tests and runner. Guard any `typer.run(...)` or `app()` script entry point with `if __name__ == "__main__":`.
- The runner supports the pytest features used by these supplied tests. It is not a complete pytest installation.
