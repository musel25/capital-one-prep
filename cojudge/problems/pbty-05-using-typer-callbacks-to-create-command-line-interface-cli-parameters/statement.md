In the previous Bite you have created your first simple Typer application with several commands.

You might have asked yourself, "How do I create arguments or options that are initialized once and can be used by several commands?". Without a feature like that, one could potentially have lots of redundant code that initializes the same arguments and options for multiple commands.

Luckily, [Typer Callback](https://typer.tiangolo.com/tutorial/commands/callback/) serves exactly this purpose.

In this Bite, you will implement a simple Typer Callback, to get familiar with the concept.

Let's add a verbosity option such that the commands can return a less verbose output by default.

Check out the tests for more information about what output is expected.

Enjoy!

**Constraints:**

- Add root options `--verbose` and `-v`, default false. Share their value through `ctx.obj`. Commands are `sum a b` and `compare c d`, with required integers. Without verbosity, print the sum or comparison result (`-1`, `0`, or `1`). With verbosity, use the messages from exercise 2. Reset verbosity for each invocation.
