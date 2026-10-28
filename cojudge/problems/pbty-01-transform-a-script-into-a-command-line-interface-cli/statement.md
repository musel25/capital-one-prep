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

**Constraints:**

- Export a Typer `app` with `main` registered as its single command. Accept negative integers and reject missing or non-integer arguments.
