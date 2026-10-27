## Reference solution

```python
from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import List, NamedTuple, Optional, Union

TMP = Path(os.getenv("TMP", "/tmp"))

import html as _html
import re as _re


class Soup:
    """Stand-in for BeautifulSoup (the judge has no third-party packages).

    Soup(html).find_all("table") returns the tables as Table objects.
    str(table) is the table's HTML. table.rows() returns the text of each
    cell (th or td), row by row.
    """

    def __init__(self, markup: str):
        self.markup = markup

    def find_all(self, name: str) -> list:
        if name != "table":
            raise NotImplementedError("this Soup only finds tables")
        return [Table(m.group(0)) for m in _re.finditer(r"<table\b.*?</table>", self.markup, _re.S | _re.I)]


class Table(str):
    def rows(self) -> list:
        rows = []
        for row in _re.findall(r"<tr\b.*?</tr>", self, _re.S | _re.I):
            cells = _re.findall(r"<t[hd]\b[^>]*>(.*?)</t[hd]>", row, _re.S | _re.I)
            rows.append([" ".join(_html.unescape(_re.sub(r"<[^>]+>", "", c)).split()) for c in cells])
        return rows


class Candidate(NamedTuple):
    name: str
    votes: str


class LeaderBoard(NamedTuple):
    Candidate: str
    Average: str
    Delegates: int
    Contributions: str
    Coverage: int


class Poll(NamedTuple):
    Poll: str
    Date: str
    Sample: int
    Sanders: float
    Biden: float
    Gabbard: float
    Spread: str


@dataclass
class File:
    name: str
    path: Path = field(init=False)

    def __post_init__(self):
        self.path = TMP / self.name

    @property
    def data(self) -> Optional[str]:
        return self.path.read_text() if self.path.exists() else None


@dataclass
class Web:
    url: str
    file: File

    @property
    def data(self) -> Optional[str]:
        return self.file.data

    @property
    def soup(self) -> Soup:
        return Soup(self.data or "")


@dataclass
class Site(ABC):
    web: Web

    def find_table(self, loc: int = 0) -> str:
        return str(self.web.soup.find_all("table")[loc])

    @abstractmethod
    def parse_rows(self, table: str) -> Union[List[LeaderBoard], List[Poll]]:
        pass

    @abstractmethod
    def polls(self, table: int = 0) -> Union[List[LeaderBoard], List[Poll]]:
        pass

    @abstractmethod
    def stats(self, loc: int = 0):
        pass


@dataclass
class RealClearPolitics(Site):

    def parse_rows(self, table: str) -> List[Poll]:
        rows = Soup(table).find_all("table")[0].rows()[1:]
        return [Poll(p, d, int(s), float(sa), float(b), float(g), sp) for p, d, s, sa, b, g, sp in rows]

    def polls(self, table: int = 2) -> List[Poll]:
        return self.parse_rows(self.find_table(table))

    def stats(self, loc: int = 2):
        polls = self.polls(loc)
        totals = {name: sum(getattr(p, name) for p in polls) for name in ("Biden", "Sanders", "Gabbard")}
        title = self.__class__.__name__
        print(f"\n{title}\n{'=' * len(title)}")
        for name, total in sorted(totals.items(), key=lambda item: -item[1]):
            print(f"{name:>9}: {total}")
        print()


@dataclass
class NYTimes(Site):
    LABELS = ("National Polling Average", "Pledged Delegates", "Individual Contributions",
              "Weekly News Coverage")

    def parse_rows(self, table: str) -> List[LeaderBoard]:
        rows = Soup(table).find_all("table")[0].rows()[1:]
        return [LeaderBoard(c, a, int(d), co, int(cv)) for c, a, d, co, cv in rows]

    def polls(self, table: int = 0) -> List[LeaderBoard]:
        return self.parse_rows(self.find_table(table))

    def stats(self, loc: int = 0):
        print(f"\n{self.__class__.__name__}\n{'=' * 33}")
        for board in self.polls(loc):
            print(f"\n{board.Candidate:>33}\n{'-' * 33}")
            for label, value in zip(self.LABELS, board[1:]):
                print(f"{label:>24}: {value}")
        print()
```
