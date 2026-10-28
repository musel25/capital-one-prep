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

**Constraints:**

- Export a single-command `app`. Use integer arguments and integer option `--c` with default `None`. Include `c is smaller`, `c is greater`, or `c is equal` when `--c` is supplied. Zero is a supplied value.
