In this Bite, you will create a simplistic CLI application with a simple progress bar.

Refer to the [progress bar documentation](https://typer.tiangolo.com/tutorial/progressbar/) for more information.

Enjoy!

**Constraints:**

- Export a single-command `app`. Require integer `count` from 0 through 100. Add `--label`, default `Processing`. Iterate once over `typer.progressbar(range(count), label=label)`, without a delay. After the bar closes, print `Processed N items`.
