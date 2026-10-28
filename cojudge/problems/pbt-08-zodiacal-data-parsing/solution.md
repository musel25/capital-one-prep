## Reference tests

```python
from datetime import date
import pytest
from zodiac import get_signs, get_sign_with_most_famous_people, signs_are_mutually_compatible, get_sign_by_date

@pytest.fixture
def signs():
    return get_signs()

def test_most_and_independent_data(signs):
    assert get_sign_with_most_famous_people(signs) == 'Leo'
    signs[0]['famous_people'].append('Extra')
    assert len(get_signs()[0]['famous_people']) == 2
    assert get_sign_with_most_famous_people([signs[1], signs[2]]) == 'Taurus'
    with pytest.raises(ValueError):
        get_sign_with_most_famous_people([])

def test_compatibility(signs):
    assert signs_are_mutually_compatible(signs, 'Aries', 'Leo') is True
    assert signs_are_mutually_compatible(signs, 'Gemini', 'Libra') is False
    assert signs_are_mutually_compatible(signs, 'Aries', 'Taurus') is False
    with pytest.raises(KeyError):
        signs_are_mutually_compatible(signs, 'Unknown', 'Leo')

@pytest.mark.parametrize('month, day, expected', [(3, 21, 'Aries'), (4, 19, 'Aries'), (4, 20, 'Taurus'), (12, 22, 'Capricorn'), (12, 31, 'Capricorn'), (1, 1, 'Capricorn'), (1, 19, 'Capricorn'), (1, 20, 'Aquarius'), (2, 29, 'Pisces')])
def test_dates(signs, month, day, expected):
    assert get_sign_by_date(signs, date(2024, month, day)) == expected

def test_no_match():
    with pytest.raises(ValueError, match='no matching'):
        get_sign_by_date([], date(2024, 1, 1))
```
