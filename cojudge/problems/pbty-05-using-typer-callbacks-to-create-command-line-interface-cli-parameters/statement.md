# 05. Using typer callbacks to create command line interface (cli) parameters

[Course list](/?course=pybites-typer) · [Original bite](https://pybitesplatform.com/bites/using-typer-callbacks-to-create-command-line-interface-cli-parameters/)

Export a multi-command Typer `app`. A root callback defines `--verbose` and `-v`,
both false by default. The option appears before the command. Share its value through
`ctx.obj`. Implement `sum a b` and `compare c d` with required integer arguments.
By default, print only the sum or the comparison result (`-1` if c < d, `0` if
c == d, `1` if c > d). With verbosity enabled, use the messages from exercise 2.
Each invocation must start with its own verbosity value.

**Source:** The original template and tests are not visible in this account.
This template and these tests are recreations based on the public description.
The contract above defines behavior that the public description does not specify.

<details>
<summary>Original public description</summary>

In the previous Bite you have created your first simple Typer application with several commands.

You might have asked yourself, "How do I create arguments or options that are initialized once and can be used by several commands?". Without a feature like that, one could potentially have lots of redundant code that initializes the same arguments and options for multiple commands.

Luckily, [Typer Callback](https://typer.tiangolo.com/tutorial/commands/callback/) serves exactly this purpose.

In this Bite, you will implement a simple Typer Callback, to get familiar with the concept.

Let's add a verbosity option such that the commands can return a less verbose output by default.

Check out the tests for more information about what output is expected.

Enjoy!

</details>

Write your code at the top of the editor. The tests below it import your code as `cli`.
**Run** checks the first three tests. **Submit** checks all 11 tests.
A failure shows the test name, error, and test line.

- Python 3.11. The judge supplies real Typer 0.12.5, Click 8.1.7, and Rich 13.9.4.
- All libraries are bundled. No installation or network access is needed.
- Use the problem's Run and Submit actions. The playground and debugger do not load the library archive.
- Keep the supplied tests and runner. Guard any `typer.run(...)` or `app()` script entry point with `if __name__ == "__main__":`.
- The runner supports the pytest features used by these supplied tests. It is not a complete pytest installation.
