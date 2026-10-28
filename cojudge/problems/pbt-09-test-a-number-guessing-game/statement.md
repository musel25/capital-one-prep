In this Bite you test a simple number guessing game (class). Ready to write some pytest code? Read on ... You again will need to mock out a standard library function, input this time. We tried to use random.randint to get the secret number, but mutation testing became a bit too strict on us, so for now we just pass the secret number into the constructor. That said, there is some validation going on that you will need to test. Check for boundaries and to check exception strings, pytest's raises has a nice match kwarg. The constructor also takes an optional max_guesses arg to make the game easier or harder. You will need to the use capfd/capsys fixture again to test the standard output of the game (100% test coverage remember).

Good luck and keep calm and code in Python / pytest.

For this version, write tests for the supplied code. Your tests must pass against the correct code, cover at least 90% of its executable statements, and detect every supplied faulty version. A fault is detected when at least one test fails. An empty test suite does not pass.

Import the target as `guessing`. The judge supplies it automatically.

```python
class GuessingGame:
    def __init__(self, secret, max_guesses=5):
        if type(secret) is not int or not 1 <= secret <= 20:
            raise ValueError('secret must be an integer from 1 to 20')
        if type(max_guesses) is not int or max_guesses < 1:
            raise ValueError('max_guesses must be a positive integer')
        self.secret, self.max_guesses = secret, max_guesses

    def play(self):
        for _ in range(self.max_guesses):
            text = input('Guess a number: ')
            try:
                guess = int(text)
            except ValueError:
                print('Enter a number')
                continue
            if guess == self.secret:
                print('You win!')
                return True
            if guess < self.secret:
                print('Too low')
            else:
                print('Too high')
        print(f'You lose! The number was {self.secret}')
        return False
```
