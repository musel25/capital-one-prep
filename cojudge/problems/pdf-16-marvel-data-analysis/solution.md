## Reference solution

Paste this code above the supplied tests and runner.

```python
import csv
import io
from typing import NamedTuple


class Character(NamedTuple):
    pid: str
    name: str
    sid: str
    align: str
    sex: str
    appearances: str
    year: str


# Small constructed TSV with the fields shown in the public description.
MARVEL_TSV = 'pid\tname\tsid\talign\tsex\tappearances\tyear\n1678\tSpider-Man\tSecret Identity\tGood Characters\tMale Characters\t4043\t1962\n2460\tThor\tNo Dual Identity\tGood Characters\tMale Characters\t2258\t1950\n755266\tThor\tSecret Identity\tBad Characters\tMale Characters\t1\t1998\n20704\tThor\t\tBad Characters\tMale Characters\t\t1954\n100\tStorm\tPublic Identity\tGood Characters\tFemale Characters\t1000\t1975\n101\tJean Grey\tPublic Identity\tGood Characters\tFemale Characters\t1200\t1963\n102\tUnknown\t\t\t\t\t\n103\tPractice Hero\t\tGood Characters\tGenderfluid Characters\t2\t1963\n'


def load_characters(tsv=MARVEL_TSV):
    """Read the local TSV. Every stored field remains a string."""
    return [Character(**row) for row in csv.DictReader(io.StringIO(tsv), delimiter='\t')]


characters = load_characters()


def most_popular_characters(data=characters, n=5):
    if n < 0:
        raise ValueError('n must be nonnegative')
    return sorted(data, key=lambda ch: (-int(ch.appearances or '0'), int(ch.pid)))[:n]


def max_and_min_years_new_characters(data=characters):
    counts = {}
    for character in data:
        if character.year:
            year = int(character.year)
            counts[year] = counts.get(year, 0) + 1
    if not counts:
        return None, None
    most = min(counts, key=lambda year: (-counts[year], year))
    least = min(counts, key=lambda year: (counts[year], year))
    return (most, counts[most]), (least, counts[least])


def get_percentage_female_characters(data=characters):
    specified = [ch for ch in data if ch.sex]
    if not specified:
        return 0.0
    female = sum(ch.sex == 'Female Characters' for ch in specified)
    return round(100 * female / len(specified), 2)
```
