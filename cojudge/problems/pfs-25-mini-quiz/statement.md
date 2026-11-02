## Learn

A variable can count. Start at 0 and add 1 for every correct answer:

```python
points = 0
if answer == "yes":
    points = points + 1
```

This is the last exercise. You can use everything you learned!

## Your task

Read three answers, one on each line. The questions and correct answers:

| Question | Correct answer |
| --- | --- |
| What is 2 + 2? | `4` |
| What color is the sky on a sunny day? | `blue` |
| How many legs does a spider have? | `8` |

Count the correct answers. Show the score, then a message:

| Score | Message |
| --- | --- |
| 3 | `Perfect!` |
| 2 | `Good job!` |
| 0 or 1 | `Keep practicing!` |

Example: the answers `4`, `blue`, `6` show

```text
You got 2 out of 3
Good job!
```

You can write `input("What is 2 + 2? ")`. The check does not count the question text.
