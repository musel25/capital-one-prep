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

**Constraints:**

- Use required integer arguments. For equal inputs, print `c=C is equal to d=D` with the actual values.
