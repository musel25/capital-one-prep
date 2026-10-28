"""Bite: Composition, inheritance, abstract base class, what? (offline recreation)."""

_SOUP = '''import html as _html
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
        return [Table(m.group(0)) for m in _re.finditer(r"<table\\b.*?</table>", self.markup, _re.S | _re.I)]


class Table(str):
    def rows(self) -> list:
        rows = []
        for row in _re.findall(r"<tr\\b.*?</tr>", self, _re.S | _re.I):
            cells = _re.findall(r"<t[hd]\\b[^>]*>(.*?)</t[hd]>", row, _re.S | _re.I)
            rows.append([" ".join(_html.unescape(_re.sub(r"<[^>]+>", "", c)).split()) for c in cells])
        return rows
'''

_HEADER = '''from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import List, NamedTuple, Optional, Union

TMP = Path(os.getenv("TMP", "/tmp"))

''' + _SOUP

SPEC = {
    "title": "Composition, inheritance, abstract base class, what?",
    "module": "scraper",
    "contract": "This version reads cached files only. File names are relative names under the "
                "existing TMP directory. Missing files return None; empty files return an empty "
                "string. Web.soup returns a Soup even when data is missing. Tables have one header "
                "row, followed by zero or more rows with exactly the documented fields. Numeric "
                "cells use plain int or float text. parse_rows skips the header and preserves row "
                "order. NYTimes returns LeaderBoard records; RealClearPolitics returns Poll records. "
                "Default table indices are 0 and 2 respectively. Explicit indices must be valid and "
                "nonnegative. Statistics use nonempty tables and the exact documented format; RCP "
                "orders candidate totals from highest to lowest, with tied order unspecified. "
                "Nested tables, malformed HTML or rows, file access errors, and network downloads "
                "are outside this exercise.",
    "mutations": [
        {"name": "missing_file_is_empty_string", "old": "return self.path.read_text() if self.path.exists() else None", "new": "return self.path.read_text() if self.path.exists() else ''"},
        {"name": "rcp_uses_wrong_default_table", "old": "def polls(self, table: int = 2)", "new": "def polls(self, table: int = 0)"},
        {"name": "rcp_totals_only_first_poll", "old": "sum(getattr(p, name) for p in polls)", "new": "getattr(polls[0], name)"},
    ],
    "notes": "This is an offline version. The judge has no network and no BeautifulSoup, so the "
             "template supplies a small `Soup` class with `find_all(\"table\")`, and `Web.data` reads "
             "the cached HTML file (the tests create it). The sample pages in the tests are fictional "
             "and contain only the tables that are used. Everything else follows the description: the "
             "typed namedtuples, `File`, `Web`, the `Site` abstract base class, the two parsers, and "
             "the exact output formats.",
    "template": _HEADER + '''

# Add type hints: turn these into typing.NamedTuple classes.
#   Candidate: name (str), votes (str)
#   LeaderBoard: Candidate (str), Average (str), Delegates (int),
#                Contributions (str), Coverage (int)
#   Poll: Poll (str), Date (str), Sample (int), Sanders (float),
#         Biden (float), Gabbard (float), Spread (str)
Candidate = namedtuple("Candidate", "name votes")
LeaderBoard = namedtuple("LeaderBoard", "Candidate Average Delegates Contributions Coverage")
Poll = namedtuple("Poll", "Poll Date Sample Sanders Biden Gabbard Spread")


@dataclass
class File:
    """File represents a filesystem path.

    Variables:
        name: str -- The filename that will be created on the filesystem.
        path: Path -- Path object created from TMP and the name passed in.

    Methods:
        [property]
        data: -> Optional[str] -- If the file exists, it returns its contents.
            If it does not exist, it returns None.
    """
    name: str


@dataclass
class Web:
    """Web object.

    Variables:
        url: str -- The URL of the site.
        file: File -- File object where the HTML of the site is cached.

    Methods:
        [property]
        data: -> Optional[str] -- The contents of the cached file, or None.
            (The original downloads the page when the file is missing;
             the judge is offline, so return the file data.)
        [property]
        soup: -> Soup -- A Soup object of the HTML data.
    """
    url: str
    file: File


class Site(ABC):
    """Site abstract base class. Its constructor receives web: Web.

    Methods:
        find_table(loc: int = 0) -> str -- The HTML of the table at index loc
            in the page (str() of the Soup table). Not abstract.
        [abstract] parse_rows(table: str) -> Union[List[LeaderBoard], List[Poll]]
            -- Turn the data rows (skip the header row) into namedtuples.
        [abstract] polls(table: int = 0) -> Union[List[LeaderBoard], List[Poll]]
            -- parse_rows of find_table(table).
        [abstract] stats(loc: int = 0) -- Print the statistics.
    """


class RealClearPolitics(Site):
    """RealClearPolitics: Poll rows from the page's third table (loc=2).

    stats(loc=2) prints, for example:

    (blank line)
    RealClearPolitics
    =================
        Biden: 214.0
      Sanders: 142.0
      Gabbard: 6.0
    (blank line)

    One line per candidate (Biden, Sanders, Gabbard) with the sum of their
    numbers over all polls, highest sum first. The title is underlined with
    as many = signs as it has characters. Last names are right aligned to a
    width of 9: f"{name:>9}: {total}".
    """


class NYTimes(Site):
    """NYTimes: LeaderBoard rows from the "Current State of the Race" table (loc=0).

    stats(loc=0) prints, for example:

    (blank line)
    NYTimes
    =================================
    (blank line)
                       Pete Buttigieg
    ---------------------------------
    National Polling Average: 10%
           Pledged Delegates: 25
    Individual Contributions: $76.2m
        Weekly News Coverage: 3
    (blank line)
                       Bernie Sanders
    ---------------------------------
    ... and so on for every candidate in table order, then a final blank line.

    The dividers have 33 characters. The candidate name is right aligned to
    33 characters. The labels are right aligned to 24 characters, followed
    by ": " and the value.
    """
''',
    "tests": '''import inspect

import pytest

import scraper
from scraper import (Candidate, File, LeaderBoard, NYTimes, Poll, RealClearPolitics,
                     Site, Soup, Web)

NYT_HTML = """<html><body><h1>Democratic Presidential Candidates</h1>
<p>Current State of the Race</p>
<table class="leaderboard">
<tr><th>Candidate</th><th>National Polling Average</th><th>Pledged Delegates</th>
<th>Individual Contributions</th><th>Weekly News Coverage</th></tr>
<tr><td>Pete Buttigieg</td><td>10%</td><td>25</td><td>$76.2m</td><td>3</td></tr>
<tr><td>Bernie Sanders</td><td>23%</td><td>21</td><td>$134.4m</td><td>3</td></tr>
<tr><td>Joseph R. Biden Jr.</td><td>26%</td><td>15</td><td>$60.6m</td><td>1</td></tr>
<tr><td>Tulsi Gabbard</td><td>2%</td><td>0</td><td>$11.9m</td><td>8</td></tr>
</table></body></html>"""

RCP_HTML = """<html><body>
<table id="t1"><tr><th>Poll</th><th>Spread</th></tr><tr><td>RCP Average</td><td>Biden +5</td></tr></table>
<table id="t2"><tr><th>Poll</th><th>Spread</th></tr><tr><td>Monmouth</td><td>Tie</td></tr></table>
<table id="t3">
<tr><th>Poll</th><th>Date</th><th>Sample</th><th>Sanders</th><th>Biden</th><th>Gabbard</th><th>Spread</th></tr>
<tr><td>Emerson</td><td>2/16 - 2/18</td><td>1250</td><td>30.0</td><td>40.0</td><td>2.0</td><td>Biden +10</td></tr>
<tr><td>Monmouth</td><td>2/16 - 2/19</td><td>1500</td><td>26.0</td><td>48.0</td><td>1.0</td><td>Biden +22</td></tr>
<tr><td>CNN</td><td>2/17 - 2/20</td><td>900</td><td>35.0</td><td>63.0</td><td>2.0</td><td>Biden +28</td></tr>
<tr><td>Fox News</td><td>2/18 - 2/21</td><td>1000</td><td>51.0</td><td>63.0</td><td>1.0</td><td>Biden +12</td></tr>
</table></body></html>"""

NYT_STATS = """
NYTimes
=================================

                   Pete Buttigieg
---------------------------------
National Polling Average: 10%
       Pledged Delegates: 25
Individual Contributions: $76.2m
    Weekly News Coverage: 3

                   Bernie Sanders
---------------------------------
National Polling Average: 23%
       Pledged Delegates: 21
Individual Contributions: $134.4m
    Weekly News Coverage: 3

              Joseph R. Biden Jr.
---------------------------------
National Polling Average: 26%
       Pledged Delegates: 15
Individual Contributions: $60.6m
    Weekly News Coverage: 1

                    Tulsi Gabbard
---------------------------------
National Polling Average: 2%
       Pledged Delegates: 0
Individual Contributions: $11.9m
    Weekly News Coverage: 8

"""

RCP_STATS = """
RealClearPolitics
=================
    Biden: 214.0
  Sanders: 142.0
  Gabbard: 6.0

"""


@pytest.fixture
def tmp(tmp_path, monkeypatch):
    monkeypatch.setattr(scraper, "TMP", tmp_path)
    return tmp_path


@pytest.fixture
def nyt(tmp):
    (tmp / "nyt.html").write_text(NYT_HTML)
    return NYTimes(Web("https://www.nytimes.com/interactive/2020/us/elections/democratic-polls.html",
                       File("nyt.html")))


@pytest.fixture
def rcp(tmp):
    (tmp / "rcp.html").write_text(RCP_HTML)
    return RealClearPolitics(Web("https://www.realclearpolitics.com/epolls/2020/president/us/"
                                 "2020_democratic_presidential_nomination-6730.html", File("rcp.html")))


def test_namedtuples_have_type_hints():
    assert Candidate.__annotations__ == {"name": str, "votes": str}
    assert LeaderBoard.__annotations__ == {"Candidate": str, "Average": str, "Delegates": int,
                                           "Contributions": str, "Coverage": int}
    assert Poll.__annotations__ == {"Poll": str, "Date": str, "Sample": int, "Sanders": float,
                                    "Biden": float, "Gabbard": float, "Spread": str}
    assert Candidate("Bernie", "10")._fields == ("name", "votes")


def test_file(tmp):
    file = File("missing.html")
    assert file.path == tmp / "missing.html"
    assert file.data is None
    (tmp / "missing.html").write_text("<p>now it exists</p>")
    assert file.data == "<p>now it exists</p>"


def test_web(nyt, tmp):
    web = nyt.web
    assert isinstance(web.file, File)
    assert web.data == NYT_HTML
    assert isinstance(web.soup, Soup)
    assert len(web.soup.find_all("table")) == 1


def test_site_is_an_abstract_base_class(nyt):
    assert issubclass(Site, scraper.ABC)
    assert set(Site.__abstractmethods__) == {"parse_rows", "polls", "stats"}
    with pytest.raises(TypeError):
        Site(nyt.web)

    class Incomplete(Site):
        def polls(self, table=0):
            return []
    with pytest.raises(TypeError):
        Incomplete(nyt.web)


def test_composition(nyt, rcp):
    for site in (nyt, rcp):
        assert isinstance(site, Site)
        assert isinstance(site.web, Web)
        assert not isinstance(site, Web)


def test_find_table(rcp):
    first, third = rcp.find_table(0), rcp.find_table(2)
    assert isinstance(third, str)
    assert first.startswith("<table") and 'id="t1"' in first
    assert 'id="t3"' in third and "Emerson" in third
    assert "Emerson" not in first


def test_nyt_polls(nyt):
    polls = nyt.polls()
    assert len(polls) == 4
    assert polls[0] == LeaderBoard("Pete Buttigieg", "10%", 25, "$76.2m", 3)
    assert polls[2] == LeaderBoard("Joseph R. Biden Jr.", "26%", 15, "$60.6m", 1)
    assert all(isinstance(p, LeaderBoard) for p in polls)
    assert nyt.parse_rows(nyt.find_table(0)) == polls


def test_rcp_polls(rcp):
    polls = rcp.polls(2)
    assert len(polls) == 4
    assert polls[0] == Poll("Emerson", "2/16 - 2/18", 1250, 30.0, 40.0, 2.0, "Biden +10")
    assert all(isinstance(p.Sample, int) and isinstance(p.Biden, float) for p in polls)


def test_nyt_stats(nyt, capsys):
    nyt.stats()
    assert capsys.readouterr().out == NYT_STATS


def test_rcp_stats(rcp, capsys):
    rcp.stats(2)
    assert capsys.readouterr().out == RCP_STATS


def test_parsers_derive_from_site():
    assert issubclass(NYTimes, Site)
    assert issubclass(RealClearPolitics, Site)
    assert "find_table" not in NYTimes.__dict__ and "find_table" not in RealClearPolitics.__dict__


def test_missing_and_empty_web_cache(tmp):
    file = File('empty.html')
    web = Web('https://example.invalid/offline', file)
    assert web.data is None
    assert isinstance(web.soup, Soup)
    assert web.soup.find_all('table') == []
    file.path.write_text('')
    assert file.data == ''
    assert web.data == ''
    assert web.soup.find_all('table') == []
    file.path.write_text('<table><tr><th>header</th></tr></table>')
    assert len(web.soup.find_all('table')) == 1


def test_header_only_tables(nyt, rcp):
    table = '<table><tr><th>header</th></tr></table>'
    assert nyt.parse_rows(table) == []
    assert rcp.parse_rows(table) == []


def test_rcp_default_table_and_changed_poll_data(rcp, capsys):
    assert rcp.polls() == rcp.polls(2)
    table = ('<table><tr><th>Poll</th><th>Date</th><th>Sample</th><th>Sanders</th>'
             '<th>Biden</th><th>Gabbard</th><th>Spread</th></tr>'
             '<tr><td> New &amp; Co </td><td>today</td><td>1</td><td>2.5</td>'
             '<td>0</td><td>1</td><td>Sanders +2.5</td></tr>'
             '<tr><td>Other</td><td>yesterday</td><td>0</td><td>3.0</td>'
             '<td>0</td><td>0</td><td>Sanders +3</td></tr></table>')
    rcp.web.file.path.write_text(table)
    assert rcp.polls(0) == [Poll('New & Co', 'today', 1, 2.5, 0.0, 1.0, 'Sanders +2.5'),
                            Poll('Other', 'yesterday', 0, 3.0, 0.0, 0.0, 'Sanders +3')]
    rcp.stats(0)
    assert capsys.readouterr().out == ('\\nRealClearPolitics\\n=================\\n'
                                     '  Sanders: 5.5\\n  Gabbard: 1.0\\n    Biden: 0.0\\n\\n')


def test_nyt_parses_other_table_and_current_file_data(nyt, capsys):
    table = ('<table><tr><th>Candidate</th><th>Average</th><th>Delegates</th>'
             '<th>Contributions</th><th>Coverage</th></tr>'
             '<tr><td><b>A &amp; B</b></td><td>0%</td><td>0</td>'
             '<td>$0</td><td>0</td></tr></table>')
    nyt.web.file.path.write_text('<table><tr><th>unused</th></tr></table>' + table)
    assert nyt.polls(1) == [LeaderBoard('A & B', '0%', 0, '$0', 0)]
    nyt.stats(1)
    assert capsys.readouterr().out == ('\\nNYTimes\\n=================================\\n\\n'
        '                            A & B\\n---------------------------------\\n'
        'National Polling Average: 0%\\n       Pledged Delegates: 0\\n'
        'Individual Contributions: $0\\n    Weekly News Coverage: 0\\n\\n')
''',
    "reference": _HEADER + '''

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
        print(f"\\n{title}\\n{'=' * len(title)}")
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
        print(f"\\n{self.__class__.__name__}\\n{'=' * 33}")
        for board in self.polls(loc):
            print(f"\\n{board.Candidate:>33}\\n{'-' * 33}")
            for label, value in zip(self.LABELS, board[1:]):
                print(f"{label:>24}: {value}")
        print()
''',
}
