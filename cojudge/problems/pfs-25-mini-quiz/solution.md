## One correct answer

Try the exercise first. There are many correct answers.

```python
a1 = input("What is 2 + 2? ")
a2 = input("What color is the sky on a sunny day? ")
a3 = input("How many legs does a spider have? ")
score = 0
if a1 == "4":
    score = score + 1
if a2 == "blue":
    score = score + 1
if a3 == "8":
    score = score + 1
print("You got", score, "out of 3")
if score == 3:
    print("Perfect!")
elif score == 2:
    print("Good job!")
else:
    print("Keep practicing!")
```
