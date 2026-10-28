# 01. Transform a script into a command line interface (cli)

[Course list](/?course=pybites-typer) · [Original bite](https://pybitesplatform.com/bites/transform-a-script-into-a-command-line-interface-cli/)

Implement `main(a, b)` with two required integer CLI arguments. Add help text
`The value of the first summand` and `The value of the second summand`.
Print `The sum is N`. Export `app`, a Typer application with `main` registered as
its single command. You can also call `typer.run(main)` from a guarded script entry point.
Accept negative integers. Reject missing or non-integer values.

**Source:** The original template and tests are not visible in this account.
This template and these tests are recreations based on the public description.
The contract above defines behavior that the public description does not specify.

<details>
<summary>Original public description</summary>

There are several Python frameworks to create CLIs, check out this overview of CLI framework options.

In this Bite we will leverage Typer to create a CLI based on a simple Python script.

Therefore, a script with a simple function will be provided so that you will only need to extend the provided script with Typer annotations to allow it to be called with typer.run(main).

Typing python script.py --help should return the following:

```python
Usage: script.py [OPTIONS] a b  CLI that allows you to add two numbersArguments:  a  The value of the first summand  [required]  b  The value of the second summand  [required]Options:  --install-completion  Install completion for the current shell.  --show-completion     Show completion for the current shell, to copy it or                        customize the installation.  --help                Show this message and exit.
```

The Options are standard Typer switches which are available out-of-the-box, so you don't need to worry about them.

If this description is unclear, check out the tests to better understand what is required.

One last hint: Make sure to always use lowercase arguments, since there is a bug in click concerning mixed and upper case arguments.

Enjoy!

PS: Just use typer.Argument for now. If you stumble over typer.Option and wonder what the difference is, wait for the next Bite. :)

</details>

Write your code at the top of the editor. The tests below it import your code as `cli`.
**Run** checks the first three tests. **Submit** checks all 9 tests.
A failure shows the test name, error, and test line.

- Python 3.11. The judge supplies real Typer 0.12.5, Click 8.1.7, and Rich 13.9.4.
- All libraries are bundled. No installation or network access is needed.
- Use the problem's Run and Submit actions. The playground and debugger do not load the library archive.
- Keep the supplied tests and runner. Guard any `typer.run(...)` or `app()` script entry point with `if __name__ == "__main__":`.
- The runner supports the pytest features used by these supplied tests. It is not a complete pytest installation.
