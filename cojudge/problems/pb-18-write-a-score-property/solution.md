## Reference solution

```python
BELTS = {10: 'white', 50: 'yellow', 100: 'orange', 175: 'green',
         250: 'blue', 400: 'brown', 600: 'black', 800: 'paneled',
         1000: 'red'}


class NinjaBelt:

    def __init__(self, score=0):
        self._score = score
        self._last_earned_belt = None

    def _get_belt(self, new_score):
        """Might be a useful helper"""
        earned = [belt for points, belt in sorted(BELTS.items()) if new_score >= points]
        return earned[-1] if earned else None

    def _get_score(self):
        return self._score

    def _set_score(self, new_score):
        if type(new_score) is not int:
            raise ValueError("Score takes an int")
        if new_score < self._score:
            raise ValueError("Cannot lower score")
        self._score = new_score
        belt = self._get_belt(new_score)
        if belt is not None and belt != self._last_earned_belt:
            self._last_earned_belt = belt
            print(f"Congrats, you earned {new_score} points obtaining the PyBites Ninja {belt.title()} Belt")
        else:
            print(f"Set new score to {new_score}")

    score = property(_get_score, _set_score)
```
