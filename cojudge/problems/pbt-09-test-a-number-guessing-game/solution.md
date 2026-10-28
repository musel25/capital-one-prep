## Reference tests

```python
from unittest.mock import patch
import pytest
from guessing import GuessingGame

@pytest.mark.parametrize('secret', [0, 21, True, '2', 1.5])
def test_secret_validation(secret):
    with pytest.raises(ValueError, match='secret must be an integer from 1 to 20'):
        GuessingGame(secret)

@pytest.mark.parametrize('limit', [0, -1, True, '2', 1.5])
def test_limit_validation(limit):
    with pytest.raises(ValueError, match='max_guesses must be a positive integer'):
        GuessingGame(10, limit)

@pytest.mark.parametrize('secret', [1, 20])
def test_endpoints(secret, capsys):
    game = GuessingGame(secret)
    assert game.max_guesses == 5
    with patch('builtins.input', return_value=str(secret)):
        assert game.play() is True
    assert capsys.readouterr().out == 'You win!\n'

def test_win_on_last_guess(capsys):
    with patch('builtins.input', side_effect=['x', '9', '11', '10']) as read:
        assert GuessingGame(10, 4).play() is True
        assert read.call_count == 4
    assert capsys.readouterr().out == 'Enter a number\nToo low\nToo high\nYou win!\n'

def test_loss(capsys):
    with patch('builtins.input', side_effect=['1', '20']) as read:
        assert GuessingGame(10, 2).play() is False
        assert read.call_count == 2
    assert capsys.readouterr().out == 'Too low\nToo high\nYou lose! The number was 10\n'
```
