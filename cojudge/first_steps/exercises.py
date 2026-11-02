"""Python First Steps: 25 tiny exercises for a complete beginner.

Order: print, numbers, variables, input, if, if/else, elif, and/or, two small projects.
The order follows common beginner courses (Codecademy Learn Python, HackerRank
Python introduction, CodingBat Warmup). All exercise text and tests are original.

Each exercise has:
- ``reference``: a Python program (stdin -> printed text).
- ``java``: the body of an independent Java implementation used by Marker.java.
  It can use ``num(i)`` (line i as an int), ``line(i)`` (line i as text) and
  ``say(...)`` (prints values with one space between them, like Python print).
- ``tests``: stdin text for every official test. The first ``samples`` are shown.
- ``faults``: realistic mistakes that the tests must reject.
"""

NO_INPUT = ['']

EXERCISES = [
    # ------------------------------------------------------------------ print
    dict(
        slug='hello-world', title='Hello, World!', category='01-print',
        lesson='''`print()` shows text on the screen. Put the text inside quotes `" "`.

```python
print("I like pizza")
```

The screen shows:

```text
I like pizza
```''',
        task='''Show this text:

```text
Hello, World!
```

Big and small letters must match. The comma and the `!` must match too.''',
        starter='# Write your code below this line.\n# Example: print("I like pizza")\n',
        reference='print("Hello, World!")\n',
        java='say("Hello, World!");',
        tests=NO_INPUT,
        hints=['Write `print("Hello, World!")`.', 'Check the big H, the big W, the comma and the `!`.'],
        faults=[('small letters', 'Hello, World!', 'hello world')],
    ),
    dict(
        slug='a-short-poem', title='A Short Poem', category='01-print',
        lesson='''Each `print()` shows one line. Python runs your lines from top to bottom.

```python
print("one")
print("two")
```

```text
one
two
```''',
        task='''Show this poem. Use four `print()` lines.

```text
Roses are red
Violets are blue
I can write code
And so can you
```''',
        starter='# Write four print() lines below.\nprint("Roses are red")\n',
        reference='print("Roses are red")\nprint("Violets are blue")\nprint("I can write code")\nprint("And so can you")\n',
        java='say("Roses are red"); say("Violets are blue"); say("I can write code"); say("And so can you");',
        tests=NO_INPUT,
        hints=['Copy the first line. Change the text for each new line.'],
        faults=[('lines in the wrong order', 'print("Roses are red")\nprint("Violets are blue")',
                 'print("Violets are blue")\nprint("Roses are red")')],
    ),
    dict(
        slug='calculator', title='Python Is a Calculator', category='01-print',
        lesson='''Numbers do not need quotes. Python can do math:

| Sign | Meaning | Example | Result |
| --- | --- | --- | --- |
| `+` | plus | `print(2 + 3)` | `5` |
| `-` | minus | `print(9 - 4)` | `5` |
| `*` | times | `print(6 * 7)` | `42` |

Be careful: `print("2 + 3")` has quotes, so it shows the text `2 + 3`, not `5`.''',
        task='''Let Python calculate these. Show each result on its own line.

1. `12 + 30`
2. `9 * 8`
3. `100 - 1`

Do not calculate them in your head. Write the math inside `print()`.''',
        starter='# Write three print() lines. Use + * and -\n',
        reference='print(12 + 30)\nprint(9 * 8)\nprint(100 - 1)\n',
        java='say(12 + 30); say(9 * 8); say(100 - 1);',
        tests=NO_INPUT,
        hints=['The first line is `print(12 + 30)`.', 'No quotes around the math.'],
        faults=[('math inside quotes', 'print(12 + 30)', 'print("12 + 30")')],
    ),
    dict(
        slug='star-triangle', title='Draw a Triangle', category='01-print',
        lesson='''You can draw pictures with text. You can also multiply text:

```python
print("*" * 3)
```

```text
***
```''',
        task='''Draw this triangle. It has 5 rows.

```text
*
**
***
****
*****
```

You can type the stars, or use `"*" * 4` and similar.''',
        starter='print("*")\n# Add the other rows below.\n',
        reference='print("*")\nprint("*" * 2)\nprint("*" * 3)\nprint("*" * 4)\nprint("*" * 5)\n',
        java='for (int i = 1; i <= 5; i++) say("*".repeat(i));',
        tests=NO_INPUT,
        hints=['Row number 3 has 3 stars.', 'Five `print()` lines are enough.'],
        faults=[('only four rows', 'print("*" * 5)\n', '')],
    ),
    dict(
        slug='days-and-hours', title='Days and Hours', category='01-print',
        lesson='''Use commas in `print()` to show text and numbers together.
Python puts one space between the parts.

```python
print("I have", 2 + 1, "pets")
```

```text
I have 3 pets
```''',
        task='''A week has 7 days. A day has 24 hours. Show these two lines:

```text
A week has 7 days
A week has 168 hours
```

Let Python calculate `7 * 24` for the second line.''',
        starter='print("A week has", 7, "days")\n# Now show the hours. Use 7 * 24\n',
        reference='print("A week has", 7, "days")\nprint("A week has", 7 * 24, "hours")\n',
        java='say("A week has", 7, "days"); say("A week has", 7 * 24, "hours");',
        tests=NO_INPUT,
        hints=['The second line is like the first. Replace `7` with `7 * 24` and `"days"` with `"hours"`.'],
        faults=[('wrong hours', '7 * 24', '7 * 12')],
    ),
    # -------------------------------------------------------------- variables
    dict(
        slug='animal-sounds', title='Animal Sounds', category='02-variables',
        lesson='''A **variable** is a box with a name. You put a value in it with `=`.

```python
color = "green"
print("My bike is", color)
```

```text
My bike is green
```

Do not put quotes around the variable name. `print("color")` shows the word `color`.''',
        task='''The variables `animal` and `sound` are ready. Use them to show:

```text
The cat says meow
meow meow meow
```''',
        starter='animal = "cat"\nsound = "meow"\n\n# Write your code below. Use the variables.\n',
        reference='animal = "cat"\nsound = "meow"\nprint("The", animal, "says", sound)\nprint(sound, sound, sound)\n',
        java='String animal = "cat", sound = "meow"; say("The", animal, "says", sound); say(sound, sound, sound);',
        tests=NO_INPUT,
        hints=['First line: `print("The", animal, "says", sound)`.', 'Second line: use `sound` three times.'],
        faults=[('variable name in quotes', 'print("The", animal, "says", sound)', 'print("The", "animal", "says", sound)')],
    ),
    dict(
        slug='shopping', title='Going Shopping', category='02-variables',
        lesson='''Variables can hold numbers. You can do math with them.

```python
apples = 5
eaten = 2
print("Apples left:", apples - eaten)
```

```text
Apples left: 3
```''',
        task='''One notebook costs 3 dollars. You buy 4 notebooks. Show:

```text
Total: 12 dollars
```

Use the variables `price` and `count` to calculate the total.''',
        starter='price = 3\ncount = 4\n\n# Show the total below.\n',
        reference='price = 3\ncount = 4\nprint("Total:", price * count, "dollars")\n',
        java='int price = 3, count = 4; say("Total:", price * count, "dollars");',
        tests=NO_INPUT,
        hints=['Times is `*`.', '`print("Total:", price * count, "dollars")`'],
        faults=[('adds instead of multiplies', 'price * count', 'price + count')],
    ),
    # ------------------------------------------------------------------ input
    dict(
        slug='echo', title='Echo', category='03-input',
        lesson='''`input()` reads one line that someone types. Save it in a variable.

```python
food = input()
print(food)
```

If someone types `pizza`, the program shows `pizza`.

**How the check works:** each test types something for your program.
You see it as the test **input**. Your program must show the right text for every test.''',
        task='''Read one line with `input()`. Show the same line again.

| Input | Your program shows |
| --- | --- |
| `hello` | `hello` |
| `I like cake` | `I like cake` |''',
        starter='word = input()\n\n# Show the word below.\n',
        reference='word = input()\nprint(word)\n',
        java='say(line(0));',
        tests=['hello', 'I like cake', 'Python', '12345', 'Marie'],
        samples=2,
        hints=['`print(word)` with no quotes around `word`.'],
        faults=[('prints the variable name', 'print(word)', 'print("word")')],
    ),
    dict(
        slug='say-hello', title='Say Hello', category='03-input',
        lesson='''You can join text with `+`:

```python
name = "Sam"
print("Good morning, " + name + "!")
```

```text
Good morning, Sam!
```

`+` adds no space, so put the space inside the quotes: `"Good morning, "`.''',
        task='''Read a name. Say hello to it like this:

| Input | Your program shows |
| --- | --- |
| `Ana` | `Hello, Ana!` |
| `Leo` | `Hello, Leo!` |

There is no space before the `!`.''',
        starter='name = input()\n\n# Say hello below.\n',
        reference='name = input()\nprint("Hello, " + name + "!")\n',
        java='say("Hello, " + line(0) + "!");',
        tests=['Ana', 'Leo', 'Marie', 'Sam Smith', 'Python'],
        samples=2,
        hints=['`print("Hello, " + name + "!")`', 'Commas would add a space before `!`. Use `+` here.'],
        faults=[('space before !', 'print("Hello, " + name + "!")', 'print("Hello,", name, "!")')],
    ),
    dict(
        slug='double-it', title='Double It', category='03-input',
        lesson='''`input()` always gives you **text**. To do math, change it to a whole number with `int()`:

```python
n = int(input())
print(n + 1)
```

If the input is `4`, the program shows `5`.
Without `int()`, Python cannot add a number to the text.''',
        task='''Read a whole number. Show the number times 2.

| Input | Your program shows |
| --- | --- |
| `4` | `8` |
| `25` | `50` |''',
        starter='n = int(input())\n\n# Show n times 2 below.\n',
        reference='n = int(input())\nprint(n * 2)\n',
        java='say(num(0) * 2);',
        tests=['4', '25', '0', '-3', '1000'],
        samples=2,
        hints=['Times is `*`.'],
        faults=[('adds 2 instead', 'n * 2', 'n + 2')],
    ),
    dict(
        slug='next-birthday', title='Next Birthday', category='03-input',
        lesson='''You can read a number and use it in a sentence:

```python
pets = int(input())
print("Soon I will have", pets + 1, "pets")
```''',
        task='''Read an age. Show how old the person will be next year.

| Input | Your program shows |
| --- | --- |
| `14` | `Next year you will be 15` |
| `9` | `Next year you will be 10` |''',
        starter='age = int(input())\n\n# Write your code below.\n',
        reference='age = int(input())\nprint("Next year you will be", age + 1)\n',
        java='say("Next year you will be", num(0) + 1);',
        tests=['14', '9', '0', '99', '30'],
        samples=2,
        hints=['Use commas: `print("Next year you will be", age + 1)`.'],
        faults=[('forgets to add 1', 'age + 1', 'age')],
    ),
    dict(
        slug='add-two-numbers', title='Add Two Numbers', category='03-input',
        lesson='''Each `input()` reads the **next** line. Two `input()` calls read two lines.

```python
first = input()
second = input()
```

If the input is

```text
red
blue
```

then `first` is `"red"` and `second` is `"blue"`.''',
        task='''Read two whole numbers, one on each line. Show the sum like this:

| Input | Your program shows |
| --- | --- |
| `3` and `4` | `3 + 4 = 7` |
| `10` and `20` | `10 + 20 = 30` |

Tip: `print(a, "+", b, "=", a + b)` puts spaces between the parts.''',
        starter='a = int(input())\nb = int(input())\n\n# Show the sum below.\n',
        reference='a = int(input())\nb = int(input())\nprint(a, "+", b, "=", a + b)\n',
        java='int a = num(0), b = num(1); say(a, "+", b, "=", a + b);',
        tests=['3\n4', '10\n20', '0\n5', '-2\n2', '100\n250'],
        samples=2,
        hints=['The tip in the task is almost the full answer.'],
        faults=[('multiplies', '"=", a + b', '"=", a * b')],
    ),
    # ---------------------------------------------------------------- if/else
    dict(
        slug='big-number', title='Is It Big?', category='04-if-else',
        lesson='''`if` runs some lines **only when** something is true.

```python
temperature = int(input())
if temperature > 30:
    print("Drink water!")
print("Have a nice day")
```

- The line after `if` ends with `:`.
- The lines inside the `if` start with 4 spaces.
- `print("Have a nice day")` has no spaces, so it always runs.

Compare signs: `>` bigger, `<` smaller, `>=` bigger or equal, `<=` smaller or equal.''',
        task='''Read a number. If it is **bigger than 100**, show `Big number!`.
Then always show `Done`.

| Input | Your program shows |
| --- | --- |
| `150` | `Big number!` and then `Done` |
| `5` | `Done` |
| `100` | `Done` (100 is not bigger than 100) |''',
        starter='n = int(input())\n\n# Write your if below.\n\nprint("Done")\n',
        reference='n = int(input())\nif n > 100:\n    print("Big number!")\nprint("Done")\n',
        java='if (num(0) > 100) say("Big number!"); say("Done");',
        tests=['150', '5', '100', '101', '-50', '1000'],
        samples=3,
        hints=['`if n > 100:` and then a line with 4 spaces in front.', 'Keep `print("Done")` without spaces in front.'],
        faults=[('includes 100', 'n > 100', 'n >= 100'),
                ('Done inside the if', 'print("Done")', '    print("Done")')],
    ),
    dict(
        slug='even-or-odd', title='Even or Odd', category='04-if-else',
        lesson='''`else` runs when the `if` is **not** true. Exactly one of the two parts runs.

`%` gives the remainder after dividing. `7 % 2` is `1`. `8 % 2` is `0`.
Two equal signs `==` ask "is it equal?". One `=` puts a value in a variable.

```python
n = int(input())
if n % 3 == 0:
    print("fits in groups of 3")
else:
    print("does not fit")
```''',
        task='''Read a whole number. Show `even` or `odd` after it.

| Input | Your program shows |
| --- | --- |
| `4` | `4 is even` |
| `7` | `7 is odd` |
| `0` | `0 is even` |''',
        starter='n = int(input())\n\nif n % 2 == 0:\n    print(n, "is even")\n# Add an else below.\n',
        reference='n = int(input())\nif n % 2 == 0:\n    print(n, "is even")\nelse:\n    print(n, "is odd")\n',
        java='int n = num(0); if (n % 2 == 0) say(n, "is even"); else say(n, "is odd");',
        tests=['4', '7', '0', '13', '-2', '99'],
        samples=3,
        hints=['`else:` has no condition and ends with `:`.', 'The line under `else:` starts with 4 spaces.'],
        faults=[('checks remainder 1 as even', 'n % 2 == 0', 'n % 2 == 1')],
    ),
    dict(
        slug='secret-password', title='Secret Password', category='04-if-else',
        lesson='''You can compare text with `==`. The text must be **exactly** the same.
`"Cat" == "cat"` is false, because of the big C.

```python
answer = input()
if answer == "yes":
    print("Great!")
else:
    print("Oh no")
```''',
        task='''The secret password is `banana`. Read a word.
Show `Welcome!` if it is the password. Otherwise show `Wrong password`.

| Input | Your program shows |
| --- | --- |
| `banana` | `Welcome!` |
| `apple` | `Wrong password` |
| `Banana` | `Wrong password` |''',
        starter='word = input()\n\n# Check the password below.\n',
        reference='word = input()\nif word == "banana":\n    print("Welcome!")\nelse:\n    print("Wrong password")\n',
        java='if (line(0).equals("banana")) say("Welcome!"); else say("Wrong password");',
        tests=['banana', 'apple', 'Banana', 'bananas', 'BANANA', 'ban'],
        samples=3,
        hints=['`if word == "banana":`', 'Two `=` signs for comparing.'],
        faults=[('ignores big letters', 'word == "banana"', 'word.lower() == "banana"'),
                ('accepts longer words', 'word == "banana"', 'word.startswith("banana")')],
    ),
    dict(
        slug='pass-or-fail', title='Pass or Fail', category='04-if-else',
        lesson='''Think about the edge. Is 60 a pass when you need "60 or more"?
Use `>=` for "bigger or equal". `>` does not include the number itself.''',
        task='''Read a test score from 0 to 100. A score of **60 or more** passes.

| Input | Your program shows |
| --- | --- |
| `75` | `You passed!` |
| `59` | `Try again` |
| `60` | `You passed!` |''',
        starter='score = int(input())\n\n# Write your if and else below.\n',
        reference='score = int(input())\nif score >= 60:\n    print("You passed!")\nelse:\n    print("Try again")\n',
        java='if (num(0) >= 60) say("You passed!"); else say("Try again");',
        tests=['75', '59', '60', '100', '0', '61'],
        samples=3,
        hints=['`if score >= 60:`'],
        faults=[('60 does not pass', 'score >= 60', 'score > 60')],
    ),
    dict(
        slug='bigger-number', title='The Bigger Number', category='04-if-else',
        lesson='''You can compare two variables:

```python
if a < b:
    print("a is smaller")
```''',
        task='''Read two whole numbers, one on each line. Show the bigger one.
If they are the same, show `They are the same`.

| Input | Your program shows |
| --- | --- |
| `3` and `8` | `8` |
| `10` and `2` | `10` |
| `5` and `5` | `They are the same` |

Tip: use `if`, then `elif a > b:` (you learn `elif` soon), or check "same" first.''',
        starter='a = int(input())\nb = int(input())\n\nif a == b:\n    print("They are the same")\n# What if they are not the same?\n',
        reference='a = int(input())\nb = int(input())\nif a == b:\n    print("They are the same")\nelse:\n    if a > b:\n        print(a)\n    else:\n        print(b)\n',
        java='int a = num(0), b = num(1); if (a == b) say("They are the same"); else say(Math.max(a, b));',
        tests=['3\n8', '10\n2', '5\n5', '-1\n-4', '0\n7', '100\n99'],
        samples=3,
        hints=['You can put an `if` inside an `else`. Then use 8 spaces in front.',
               'Inside the `else`: `if a > b:` show `a`, otherwise show `b`.'],
        faults=[('shows the smaller one', 'if a > b:', 'if a < b:')],
    ),
    # ------------------------------------------------------------------- elif
    dict(
        slug='weather', title='What to Wear', category='05-elif',
        lesson='''`elif` means "else if". Python checks from top to bottom and runs only the **first** true part.

```python
speed = int(input())
if speed < 10:
    print("slow")
elif speed < 50:
    print("medium")
else:
    print("fast")
```

For `30`, the first check is false and the second is true, so it shows `medium`.''',
        task='''Read a temperature in °C. Show what to wear:

| Temperature | Your program shows |
| --- | --- |
| below 10 | `Cold. Wear a jacket.` |
| 10 to 24 | `Nice. Wear a sweater.` |
| 25 or more | `Hot. Wear a T-shirt.` |''',
        starter='temp = int(input())\n\nif temp < 10:\n    print("Cold. Wear a jacket.")\n# Add elif and else below.\n',
        reference='temp = int(input())\nif temp < 10:\n    print("Cold. Wear a jacket.")\nelif temp < 25:\n    print("Nice. Wear a sweater.")\nelse:\n    print("Hot. Wear a T-shirt.")\n',
        java='int t = num(0); if (t < 10) say("Cold. Wear a jacket."); else if (t < 25) say("Nice. Wear a sweater."); else say("Hot. Wear a T-shirt.");',
        tests=['5', '18', '30', '9', '10', '24', '25', '-5'],
        samples=3,
        hints=['`elif temp < 25:` works, because temperatures below 10 were already caught.'],
        faults=[('25 is still nice', 'temp < 25', 'temp <= 25'),
                ('10 is cold', 'temp < 10', 'temp <= 10')],
    ),
    dict(
        slug='grade-letter', title='Grade Letter', category='05-elif',
        lesson='''With `elif` you can have many steps. Put the biggest check first.''',
        task='''Read a score from 0 to 100. Show the grade letter:

| Score | Grade |
| --- | --- |
| 90 or more | `A` |
| 80 to 89 | `B` |
| 70 to 79 | `C` |
| 60 to 69 | `D` |
| below 60 | `F` |''',
        starter='score = int(input())\n\nif score >= 90:\n    print("A")\n# Add the other grades below.\n',
        reference='score = int(input())\nif score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\nelif score >= 70:\n    print("C")\nelif score >= 60:\n    print("D")\nelse:\n    print("F")\n',
        java='int s = num(0); say(s >= 90 ? "A" : s >= 80 ? "B" : s >= 70 ? "C" : s >= 60 ? "D" : "F");',
        tests=['95', '85', '72', '61', '30', '90', '89', '80', '79', '70', '60', '59', '100', '0'],
        samples=3,
        hints=['`elif score >= 80:` shows `B`. Scores of 90 or more never reach this line.'],
        faults=[('89 is an A', 'score >= 90', 'score >= 89'),
                ('no D grade', 'elif score >= 60:\n    print("D")\n', '')],
    ),
    dict(
        slug='positive-negative-zero', title='Positive, Negative, or Zero', category='05-elif',
        lesson='''Zero is not positive and not negative. It needs its own case.''',
        task='''Read a whole number. Show `positive`, `negative`, or `zero`.

| Input | Your program shows |
| --- | --- |
| `5` | `positive` |
| `-3` | `negative` |
| `0` | `zero` |''',
        starter='n = int(input())\n\n# Use if, elif and else.\n',
        reference='n = int(input())\nif n > 0:\n    print("positive")\nelif n < 0:\n    print("negative")\nelse:\n    print("zero")\n',
        java='int n = num(0); say(n > 0 ? "positive" : n < 0 ? "negative" : "zero");',
        tests=['5', '-3', '0', '1', '-1', '500'],
        samples=3,
        hints=['Check `n > 0` first, then `n < 0`. The `else` is for zero.'],
        faults=[('zero is positive', 'n > 0', 'n >= 0')],
    ),
    # ----------------------------------------------------------------- and/or
    dict(
        slug='teenager', title='Teenager?', category='06-and-or',
        lesson='''`and` is true when **both** sides are true.

```python
if hour >= 8 and hour < 15:
    print("School time")
```''',
        task='''A teenager is **13 to 19** years old (13 and 19 count). Read an age.

| Input | Your program shows |
| --- | --- |
| `14` | `Teenager` |
| `12` | `Not a teenager` |
| `19` | `Teenager` |
| `20` | `Not a teenager` |''',
        starter='age = int(input())\n\n# Use and in your if.\n',
        reference='age = int(input())\nif age >= 13 and age <= 19:\n    print("Teenager")\nelse:\n    print("Not a teenager")\n',
        java='int a = num(0); say(a >= 13 && a <= 19 ? "Teenager" : "Not a teenager");',
        tests=['14', '12', '19', '20', '13', '8', '30'],
        samples=4,
        hints=['`if age >= 13 and age <= 19:`'],
        faults=[('or instead of and', 'age >= 13 and age <= 19', 'age >= 13 or age <= 19'),
                ('19 is not a teen', 'age <= 19', 'age < 19')],
    ),
    dict(
        slug='weekend', title='Weekend!', category='06-and-or',
        lesson='''`or` is true when **at least one** side is true.

```python
if fruit == "apple" or fruit == "pear":
    print("It grows on a tree")
```

Write the full comparison on both sides of `or`.
`fruit == "apple" or "pear"` does not work as you expect.''',
        task='''Read a day of the week. It starts with a big letter, like `Monday`.

| Input | Your program shows |
| --- | --- |
| `Saturday` | `Weekend! Sleep in.` |
| `Sunday` | `Weekend! Sleep in.` |
| any other day | `School day. Wake up!` |''',
        starter='day = input()\n\n# Use or in your if.\n',
        reference='day = input()\nif day == "Saturday" or day == "Sunday":\n    print("Weekend! Sleep in.")\nelse:\n    print("School day. Wake up!")\n',
        java='String d = line(0); say(d.equals("Saturday") || d.equals("Sunday") ? "Weekend! Sleep in." : "School day. Wake up!");',
        tests=['Saturday', 'Monday', 'Sunday', 'Friday', 'Wednesday', 'Tuesday', 'Thursday'],
        samples=3,
        hints=['`if day == "Saturday" or day == "Sunday":`'],
        faults=[('the common or mistake', 'day == "Saturday" or day == "Sunday"', 'day == "Saturday" or "Sunday"'),
                ('forgets Sunday', 'day == "Saturday" or day == "Sunday"', 'day == "Saturday"')],
    ),
    dict(
        slug='movie-ticket', title='Movie Ticket', category='06-and-or',
        lesson='''You can save the result of an `if` in a variable, and show it later:

```python
if size == "big":
    price = 4
else:
    price = 2
print("You pay", price)
```''',
        task='''Read an age. Children **under 12** and seniors **65 or older** pay 5 dollars.
Everyone else pays 9 dollars.

| Input | Your program shows |
| --- | --- |
| `8` | `Your ticket costs 5 dollars` |
| `30` | `Your ticket costs 9 dollars` |
| `70` | `Your ticket costs 5 dollars` |''',
        starter='age = int(input())\n\n# Find the price, then show it.\n',
        reference='age = int(input())\nif age < 12 or age >= 65:\n    price = 5\nelse:\n    price = 9\nprint("Your ticket costs", price, "dollars")\n',
        java='int a = num(0); say("Your ticket costs", a < 12 || a >= 65 ? 5 : 9, "dollars");',
        tests=['8', '30', '70', '11', '12', '64', '65', '0'],
        samples=3,
        hints=['`if age < 12 or age >= 65:`'],
        faults=[('12 is a child', 'age < 12', 'age <= 12'),
                ('65 pays full price', 'age >= 65', 'age > 65')],
    ),
    # --------------------------------------------------------------- projects
    dict(
        slug='rock-paper-scissors', title='Rock, Paper, Scissors', category='07-projects',
        difficulty='Medium',
        lesson='''Time for a game! The rules:

- `rock` beats `scissors`
- `scissors` beats `paper`
- `paper` beats `rock`
- the same choice is a tie

Think first: when does player 1 win? Check the tie first, then the three ways player 1 wins.
In every other case player 2 wins.''',
        task='''Read two choices, one on each line: player 1, then player 2.
Each choice is `rock`, `paper`, or `scissors`. Show `Tie`, `Player 1 wins`, or `Player 2 wins`.

| Input | Your program shows |
| --- | --- |
| `rock` and `scissors` | `Player 1 wins` |
| `rock` and `paper` | `Player 2 wins` |
| `paper` and `paper` | `Tie` |''',
        starter='p1 = input()\np2 = input()\n\nif p1 == p2:\n    print("Tie")\n# Add the rest below.\n',
        reference='p1 = input()\np2 = input()\nif p1 == p2:\n    print("Tie")\nelif p1 == "rock" and p2 == "scissors":\n    print("Player 1 wins")\nelif p1 == "scissors" and p2 == "paper":\n    print("Player 1 wins")\nelif p1 == "paper" and p2 == "rock":\n    print("Player 1 wins")\nelse:\n    print("Player 2 wins")\n',
        java='''String a = line(0), b = line(1);
        if (a.equals(b)) { say("Tie"); return; }
        List<String> order = Arrays.asList("rock", "paper", "scissors");
        int i = order.indexOf(a), j = order.indexOf(b);
        say((i - j + 3) % 3 == 1 ? "Player 1 wins" : "Player 2 wins");''',
        tests=[f'{a}\n{b}' for a, b in [('rock', 'scissors'), ('rock', 'paper'), ('paper', 'paper'),
                                         ('rock', 'rock'), ('scissors', 'scissors'), ('paper', 'rock'),
                                         ('paper', 'scissors'), ('scissors', 'paper'), ('scissors', 'rock')]],
        samples=3,
        hints=['There are three ways for player 1 to win. Use `elif ... and ...` for each one.',
               '`elif p1 == "rock" and p2 == "scissors":`'],
        faults=[('paper loses to rock', 'p1 == "paper" and p2 == "rock"', 'p1 == "rock" and p2 == "paper"'),
                ('no tie check', 'if p1 == p2:\n    print("Tie")\nelif', 'if')],
    ),
    dict(
        slug='mini-quiz', title='Mini Quiz', category='07-projects',
        difficulty='Medium',
        lesson='''A variable can count. Start at 0 and add 1 for every correct answer:

```python
points = 0
if answer == "yes":
    points = points + 1
```

This is the last exercise. You can use everything you learned!''',
        task='''Read three answers, one on each line. The questions and correct answers:

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

You can write `input("What is 2 + 2? ")`. The check does not count the question text.''',
        starter='a1 = input("What is 2 + 2? ")\na2 = input("What color is the sky on a sunny day? ")\na3 = input("How many legs does a spider have? ")\n\nscore = 0\nif a1 == "4":\n    score = score + 1\n# Check the other answers, then show the score and the message.\n',
        reference='a1 = input("What is 2 + 2? ")\na2 = input("What color is the sky on a sunny day? ")\na3 = input("How many legs does a spider have? ")\nscore = 0\nif a1 == "4":\n    score = score + 1\nif a2 == "blue":\n    score = score + 1\nif a3 == "8":\n    score = score + 1\nprint("You got", score, "out of 3")\nif score == 3:\n    print("Perfect!")\nelif score == 2:\n    print("Good job!")\nelse:\n    print("Keep practicing!")\n',
        java='''int score = 0;
        if (line(0).equals("4")) score++;
        if (line(1).equals("blue")) score++;
        if (line(2).equals("8")) score++;
        say("You got", score, "out of 3");
        say(score == 3 ? "Perfect!" : score == 2 ? "Good job!" : "Keep practicing!");''',
        tests=['4\nblue\n6', '4\nblue\n8', '5\nred\n6', '4\ngreen\n6', '3\nblue\n8', '4\nblue\n4', '1\nblue\n2'],
        samples=2,
        hints=['Use three separate `if` lines, not `elif`. Every correct answer must count.',
               'Show the score with `print("You got", score, "out of 3")`.'],
        faults=[('elif stops counting', 'if a2 == "blue":', 'elif a2 == "blue":'),
                ('2 points is perfect', 'score == 3', 'score >= 2')],
    ),
]
