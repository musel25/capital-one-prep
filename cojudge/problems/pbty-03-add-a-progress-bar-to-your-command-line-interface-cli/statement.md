# 03. Add a progress bar to your command line interface (cli)

[Course list](/?course=pybites-typer) · [Original bite](https://pybitesplatform.com/bites/add-a-progress-bar-to-your-command-line-interface-cli/)

Create a single-command Typer `app`. Its `main` command takes a required
integer `count` from 0 through 100, and an optional `--label` (default `Processing`).
Use `with typer.progressbar(range(count), label=label) as items` and iterate over
`items` once. Do not sleep. After the bar closes, print `Processed N items`.
A non-terminal test can show only the label. The tests also check the iterable
passed to the real progress bar and the items consumed from it.

**Source:** The original template and tests are not visible in this account.
This template and these tests are recreations based on the public description.
The contract above defines behavior that the public description does not specify.

<details>
<summary>Original public description</summary>

In this Bite, you will create a simplistic CLI application with a simple progress bar.

Refer to the [progress bar documentation](https://typer.tiangolo.com/tutorial/progressbar/) for more information.

Enjoy!

</details>

Write your code at the top of the editor. The tests below it import your code as `cli`.
**Run** checks the first three tests. **Submit** checks all 8 tests.
A failure shows the test name, error, and test line.

- Python 3.11. The judge supplies real Typer 0.12.5, Click 8.1.7, and Rich 13.9.4.
- All libraries are bundled. No installation or network access is needed.
- Use the problem's Run and Submit actions. The playground and debugger do not load the library archive.
- Keep the supplied tests and runner. Guard any `typer.run(...)` or `app()` script entry point with `if __name__ == "__main__":`.
- The runner supports the pytest features used by these supplied tests. It is not a complete pytest installation.
