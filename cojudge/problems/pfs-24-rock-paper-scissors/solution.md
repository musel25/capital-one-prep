## One correct answer

Try the exercise first. There are many correct answers.

```python
p1 = input()
p2 = input()
if p1 == p2:
    print("Tie")
elif p1 == "rock" and p2 == "scissors":
    print("Player 1 wins")
elif p1 == "scissors" and p2 == "paper":
    print("Player 1 wins")
elif p1 == "paper" and p2 == "rock":
    print("Player 1 wins")
else:
    print("Player 2 wins")
```
