# 04. When to use command line option (cli) options and when cli arguments?

[Course list](/?course=pybites-typer) · [Original bite](https://pybitesplatform.com/bites/when-to-use-command-line-option-cli-options-and-when-cli-arguments/)

Export a single-command Typer `app` with required integer arguments `a` and `b`.
Add optional integer option `--c` with no value by default. Without `--c`, print
`The sum is N`. With `--c`, print `The sum is N and c is smaller`, `greater`, or
`equal`, according to `c` relative to the sum. Zero is a supplied value.
Invalid or missing required values must produce a nonzero exit code.

**Source:** The original template and tests are not visible in this account.
This template and these tests are recreations based on the public description.
The contract above defines behavior that the public description does not specify.

<details>
<summary>Original public description</summary>

In Typer, you can use either `typer.Option` or `typer.Argument`.

Well, you might have guessed it:

CLI options are similar to CLI arguments - but options are optional by default (while arguments are required by default).

Furthermore, CLI options have some additional functionality compared to arguments.

In this Bite, you will extend the previous CLI script and implement a simple CLI option.

For documentation, see the [CLI Options Intro](https://typer.tiangolo.com/tutorial/options/).

Extend the code such that it also receives an optional number `c` and then compare whether the sum of `a` and `b` is greater than `c`.

Hence, when one runs `python script.py 2 3 --c 1`, we expect the following response:

```python
The sum is 5 and c is smaller
```

</details>

Write your code at the top of the editor. The tests below it import your code as `cli`.
**Run** checks the first three tests. **Submit** checks all 10 tests.
A failure shows the test name, error, and test line.

- Python 3.11. The judge supplies real Typer 0.12.5, Click 8.1.7, and Rich 13.9.4.
- All libraries are bundled. No installation or network access is needed.
- Use the problem's Run and Submit actions. The playground and debugger do not load the library archive.
- Keep the supplied tests and runner. Guard any `typer.run(...)` or `app()` script entry point with `if __name__ == "__main__":`.
- The runner supports the pytest features used by these supplied tests. It is not a complete pytest installation.
