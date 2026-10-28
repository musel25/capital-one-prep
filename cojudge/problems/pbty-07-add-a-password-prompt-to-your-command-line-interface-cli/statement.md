# 07. Add a password prompt to your command line interface (cli)

[Course list](/?course=pybites-typer) · [Original bite](https://pybitesplatform.com/bites/add-a-password-prompt-to-your-command-line-interface-cli/)

Export a single-command Typer `app`. Prompt for a required `--username` using
`Username`. Prompt for a required `--password` using `Password`. Hide password input
and require confirmation. On a mismatch, let Typer request the password again.
Accept explicit options without a prompt. On success, print `Authenticated as USERNAME`.
Never print the password. This exercise demonstrates prompt handling. It does not
connect to an authentication service. Ctrl-C or end-of-input must abort with a
nonzero exit code. Use only test credentials.

**Source:** The original template and tests are not visible in this account.
This template and these tests are recreations based on the public description.
The contract above defines behavior that the public description does not specify.

<details>
<summary>Original public description</summary>

Let's get serious. Your Command Line Interface (CLI) works and you want to authenticate who is using your application.

Here is a simple example of how to receive credentials via a password prompt.

Refer to [Typer password documentation](https://typer.tiangolo.com/tutorial/options/password/) for more help.

Enjoy!

</details>

Write your code at the top of the editor. The tests below it import your code as `cli`.
**Run** checks the first three tests. **Submit** checks all 7 tests.
A failure shows the test name, error, and test line.

- Python 3.11. The judge supplies real Typer 0.12.5, Click 8.1.7, and Rich 13.9.4.
- All libraries are bundled. No installation or network access is needed.
- Use the problem's Run and Submit actions. The playground and debugger do not load the library archive.
- Keep the supplied tests and runner. Guard any `typer.run(...)` or `app()` script entry point with `if __name__ == "__main__":`.
- The runner supports the pytest features used by these supplied tests. It is not a complete pytest installation.
