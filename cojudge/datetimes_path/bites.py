"""Offline exercise contracts, independent tests, and reference implementations."""
import json
from pathlib import Path
from textwrap import dedent
from cojudge.pybites.bites.b01 import SPEC as PROPERTY

PAGES = json.loads((Path(__file__).parent / 'source-pages.json').read_text())
SPECS = []


def add(n, module, contract, template, reference, cases, mutations, extra=''):
    tests = f'from {module} import *\nimport {module} as subject\nfrom datetime import date, datetime, timedelta, timezone\nimport pytest\n\n'
    for i, (expression, expected) in enumerate(cases, 1):
        tests += f'def test_case_{i:02d}():\n    assert ({expression}) == {expected}\n\n'
    tests += dedent(extra)
    SPECS.append(dict(title=PAGES[n-1]['title'], module=module, contract=contract,
                      template=dedent(template).strip()+'\n', reference=dedent(reference).strip()+'\n',
                      tests=tests, mutations=[dict(name=name, old=old, new=new) for name,old,new in mutations]))


add(1, 'gendates',
    'Implement an infinite generator. Its first value is PYBITES_BORN + 100 days. Each later value is 100 days after the previous value. Separate generator objects must keep separate state.',
    PAGES[0]['template'],
    r'''from datetime import datetime, timedelta
PYBITES_BORN = datetime(2016, 12, 19)
def gen_special_pybites_dates():
    current = PYBITES_BORN
    while True:
        current += timedelta(days=100)
        yield current
''', [
    ("next(gen_special_pybites_dates())", "datetime(2017, 3, 29)"),
    ("list(__import__('itertools').islice(gen_special_pybites_dates(), 3))", "[datetime(2017, 3, 29), datetime(2017, 7, 7), datetime(2017, 10, 15)]"),
    ("list(__import__('itertools').islice(gen_special_pybites_dates(), 100, 101))", "[datetime(2044, 8, 14)]"),
    ("next(gen_special_pybites_dates()) == next(gen_special_pybites_dates())", 'True')],
    [('wrong interval', 'days=100', 'days=99'), ('include birth day', 'current = PYBITES_BORN', 'current = PYBITES_BORN - timedelta(days=100)')])
SPECS[-1]['original'] = True
SPECS[-1]['template'] = PAGES[0]['template']
SPECS[-1]['tests'] = PAGES[0]['tests'] + '\n\n# Added boundary and independence tests.\n' + SPECS[-1]['tests']

SPECS.append({**PROPERTY, 'title': PAGES[1]['title'], 'template': PAGES[1]['template'],
              'tests': 'import pytest\n' + PROPERTY['tests'].replace('import pytest\n\n', '', 1)})

add(3, 'dates',
    'Return datetimes from get_hundred_days_end(start=datetime(2017, 3, 30)): start + 100 days. Return whole elapsed days from get_days_between(start=datetime(2016, 12, 19), end=datetime(2018, 5, 8)). Inputs are naive datetimes at midnight. Negative intervals are allowed.',
    r'''from datetime import datetime, timedelta
def get_hundred_days_end(start=datetime(2017, 3, 30)):
    pass
def get_days_between(start=datetime(2016, 12, 19), end=datetime(2018, 5, 8)):
    pass''',
    r'''from datetime import datetime, timedelta
def get_hundred_days_end(start=datetime(2017, 3, 30)):
    return start + timedelta(days=100)
def get_days_between(start=datetime(2016, 12, 19), end=datetime(2018, 5, 8)):
    return (end - start).days''',
    [('get_hundred_days_end()', 'datetime(2017, 7, 8)'), ('get_days_between()', '505'),
     ('get_hundred_days_end(datetime(2020, 2, 28))', 'datetime(2020, 6, 7)'),
     ('get_days_between(datetime(2020, 2, 28), datetime(2020, 3, 1))', '2'),
     ('get_days_between(datetime(2020, 1, 2), datetime(2020, 1, 1))', '-1')],
    [('count start day', 'days=100', 'days=99'), ('reverse difference', '(end - start)', '(start - end)')])

add(4, 'format_dates',
    'years_ago(date_string, reference=date(2018, 8, 1)) returns completed anniversaries since an ISO YYYY-MM-DD date. Reject future dates. convert_eu_to_us_date converts DD/MM/YYYY to MM/DD/YYYY. Invalid dates raise ValueError.',
    r'''from datetime import date, datetime
def years_ago(date_string, reference=date(2018, 8, 1)):
    pass
def convert_eu_to_us_date(value):
    pass''',
    r'''from datetime import date, datetime
def years_ago(date_string, reference=date(2018, 8, 1)):
    born = date.fromisoformat(date_string)
    if born > reference:
        raise ValueError('Future date')
    return reference.year - born.year - ((reference.month, reference.day) < (born.month, born.day))
def convert_eu_to_us_date(value):
    dt = datetime.strptime(value, '%d/%m/%Y')
    return f'{dt.month:02}/{dt.day:02}/{dt.year:04}'
''',
    [("years_ago('2000-08-01')", '18'), ("years_ago('2000-08-02')", '17'), ("years_ago('2018-08-01')", '0'),
     ("convert_eu_to_us_date('29/02/2020')", "'02/29/2020'"), ("convert_eu_to_us_date('31/12/1999')", "'12/31/1999'")],
    [('ignore anniversary', '((reference.month, reference.day) < (born.month, born.day))', '0'),
     ('swap output fields', 'dt.month:02}/{dt.day:02', 'dt.day:02}/{dt.month:02')],
    r'''def test_invalid_dates():
    assert convert_eu_to_us_date('01/01/0001') == '01/01/0001'
    with pytest.raises(ValueError):
        convert_eu_to_us_date('29/02/2019')
    with pytest.raises(ValueError):
        years_ago('2019-01-01')
''')

add(5, 'tomorrow_date',
    'tomorrow(today=None) returns a date object for the next calendar day. If today is omitted, use date.today(). The optional date argument makes boundary checks deterministic.',
    r'''from datetime import date, timedelta
def tomorrow(today=None):
    pass''',
    r'''from datetime import date, timedelta
def tomorrow(today=None):
    if today is None:
        today = date.today()
    return today + timedelta(days=1)''',
    [('tomorrow(date(2019, 12, 31))', 'date(2020, 1, 1)'), ('tomorrow(date(2020, 2, 28))', 'date(2020, 2, 29)'),
     ('tomorrow(date(2019, 2, 28))', 'date(2019, 3, 1)'), ('tomorrow(date(2020, 2, 29))', 'date(2020, 3, 1)'),
     ('tomorrow()', 'date.today() + timedelta(days=1)'), ('type(tomorrow()) is date', 'True')],
    [('skip a day', 'days=1', 'days=2'), ('ignore supplied date', 'if today is None:', 'if True:')])

add(6, 'shutdowns',
    'get_shutdown_times(log) extracts naive datetime timestamps from lines containing "Shutdown initiated.". Lines use LEVEL YYYY-MM-DDTHH:MM:SS text and are in ascending time order. get_time_between_shutdowns(log) returns the timedelta between first and last shutdown. Raise ValueError if there are fewer than two shutdowns. Unrelated lines are ignored.',
    r'''from datetime import datetime
def get_shutdown_times(log):
    pass
def get_time_between_shutdowns(log):
    pass''',
    r'''from datetime import datetime
def get_shutdown_times(log):
    return [datetime.fromisoformat(line.split()[1]) for line in log.splitlines() if 'Shutdown initiated.' in line]
def get_time_between_shutdowns(log):
    times = get_shutdown_times(log)
    if len(times) < 2:
        raise ValueError('Need two shutdowns')
    return times[-1] - times[0]''',
    [("get_shutdown_times('')", '[]'),
     ("get_shutdown_times('INFO 2014-07-03T23:27:51 supybot Shutdown initiated.')", '[datetime(2014, 7, 3, 23, 27, 51)]'),
     ("get_shutdown_times('INFO 2014-07-03T23:27:51 Started')", '[]'),
     ("get_time_between_shutdowns('INFO 2014-07-03T23:27:51 Shutdown initiated.\\nINFO 2014-07-03T23:31:22 Shutdown initiated.')", 'timedelta(seconds=211)'),
     ("get_time_between_shutdowns('I 2020-02-28T23:00:00 Shutdown initiated.\\nI 2020-02-29T00:00:00 Shutdown initiated.\\nI 2020-03-01T00:00:00 Shutdown initiated.')", 'timedelta(days=1, hours=1)')],
    [('use second event', 'times[-1]', 'times[1]'), ('include unrelated lines', "if 'Shutdown initiated.' in line", 'if line')],
    r'''def test_too_few_events():
    with pytest.raises(ValueError):
        get_time_between_shutdowns('')
''')

add(7, 'publish_dates',
    'convert_to_datetime parses strings such as Thu, 04 May 2017 20:46:00 +0200. Return the naive local datetime without timezone conversion. get_month_most_posts accepts datetimes and returns YYYY-MM; ties select the earliest month. Empty input raises ValueError.',
    r'''from datetime import datetime
from collections import Counter
def convert_to_datetime(value):
    pass
def get_month_most_posts(dates):
    pass''',
    r'''from datetime import datetime
from collections import Counter
def convert_to_datetime(value):
    return datetime.strptime(value.rsplit(' ', 1)[0], '%a, %d %b %Y %H:%M:%S')
def get_month_most_posts(dates):
    counts = Counter(f'{d.year:04}-{d.month:02}' for d in dates)
    if not counts:
        raise ValueError('No dates')
    return min(counts, key=lambda month: (-counts[month], month))''',
    [("convert_to_datetime('Thu, 04 May 2017 20:46:00 +0200')", 'datetime(2017, 5, 4, 20, 46)'),
     ("convert_to_datetime('Sat, 29 Feb 2020 00:01:02 -0500')", 'datetime(2020, 2, 29, 0, 1, 2)'),
     ("get_month_most_posts([datetime(2019, 2, 1), datetime(2019, 1, 1)])", "'2019-01'"),
     ("get_month_most_posts([datetime(2019, 2, 1)] * 2 + [datetime(2019, 1, 1)])", "'2019-02'"),
     ("get_month_most_posts([datetime(2019, 1, 1), datetime(2020, 1, 1), datetime(2020, 1, 2)])", "'2020-01'")],
    [('ignore year', "f'{d.year:04}-{d.month:02}'", "f'{d.month:02}'"), ('prefer latest tied month', 'return min(counts,', 'return max(counts,')],
    r'''def test_empty():
    assert get_month_most_posts([datetime(1, 1, 1)]) == '0001-01'
    with pytest.raises(ValueError):
        get_month_most_posts([])
''')

add(8, 'course_duration',
    'get_total_duration(text) reads one video per nonblank line. A line ends in MM:SS with an optional title before it. Minutes can exceed 59; seconds must be 00-59. Return HH:MM:SS with at least two hour digits. Empty input returns 00:00:00. Invalid lines raise ValueError.',
    r'''import re
def get_total_duration(text):
    pass''',
    r'''import re
def get_total_duration(text):
    total = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.search(r'(?:^|\s)(\d+):([0-5]\d)\s*$', line)
        if not match:
            raise ValueError('Invalid duration')
        total += int(match[1]) * 60 + int(match[2])
    hours, rest = divmod(total, 3600)
    minutes, seconds = divmod(rest, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}' ''',
    [("get_total_duration('')", "'00:00:00'"), ("get_total_duration('Intro 00:59\\nNext 00:01')", "'00:01:00'"),
     ("get_total_duration('59:59\\n00:01')", "'01:00:00'"), ("get_total_duration('120:30')", "'02:00:30'"),
     ("get_total_duration('6000:00\\n\\n00:01')", "'100:00:01'")],
    [('lose seconds', 'int(match[2])', '0'), ('wrong minute scale', 'int(match[1]) * 60', 'int(match[1]) * 100')],
    r'''def test_invalid_seconds():
    with pytest.raises(ValueError):
        get_total_duration('01:60')
''')

add(9, 'miller',
    'BITE_CREATED_DT is 2018-02-26 00:00; PY2_DEATH_DT is 2020-01-01 00:00. calc_hours_left(start=BITE_CREATED_DT, end=PY2_DEATH_DT) returns Earth hours as float. calc_minutes_miller with the same arguments returns Miller minutes: Earth hours / (365 * 24 * 7) * 60. Use exactly 365 days per Earth year. Reject end before start.',
    r'''from datetime import datetime
BITE_CREATED_DT = datetime(2018, 2, 26)
PY2_DEATH_DT = datetime(2020, 1, 1)
def calc_hours_left(start=BITE_CREATED_DT, end=PY2_DEATH_DT):
    pass
def calc_minutes_miller(start=BITE_CREATED_DT, end=PY2_DEATH_DT):
    pass''',
    r'''from datetime import datetime
BITE_CREATED_DT = datetime(2018, 2, 26)
PY2_DEATH_DT = datetime(2020, 1, 1)
def calc_hours_left(start=BITE_CREATED_DT, end=PY2_DEATH_DT):
    if end < start:
        raise ValueError('Reversed dates')
    return (end - start).total_seconds() / 3600
def calc_minutes_miller(start=BITE_CREATED_DT, end=PY2_DEATH_DT):
    return calc_hours_left(start, end) / (365 * 24 * 7) * 60''',
    [('calc_hours_left()', '16176.0'), ('round(calc_minutes_miller(), 6)', '15.827789'),
     ('calc_hours_left(datetime(2020, 1, 1), datetime(2020, 1, 1, 0, 30))', '0.5'),
     ('calc_minutes_miller(datetime(2020, 1, 1), datetime(2027, 1, 1))', 'pytest.approx(60.04696673189824)'),
     ('calc_hours_left(BITE_CREATED_DT, BITE_CREATED_DT)', '0')],
    [('discard partial day', '(end - start).total_seconds() / 3600', '(end - start).days * 24'),
     ('reverse time dilation', '/ (365 * 24 * 7)', '* (365 * 24 * 7)'),
     ('allow negative interval', 'if end < start:', 'if False:')],
    r'''def test_negative_interval():
    for function in (calc_hours_left, calc_minutes_miller):
        with pytest.raises(ValueError):
            function(PY2_DEATH_DT, BITE_CREATED_DT)
''')

add(10, 'meeting',
    'is_good_meeting_time(utc_datetime, timezones) returns True if local hours are in [MIN_MEETING_HOUR, MAX_MEETING_HOUR) for every IANA timezone. Constants are 9 and 18. A naive input is interpreted as UTC; an aware input is converted from its offset. Use zoneinfo, including daylight saving time. Empty zones returns True. An unknown timezone raises ValueError, even if another zone is outside meeting hours.',
    r'''from datetime import timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
MIN_MEETING_HOUR = 9
MAX_MEETING_HOUR = 18
def is_good_meeting_time(utc_datetime, timezones):
    pass''',
    r'''from datetime import timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
MIN_MEETING_HOUR = 9
MAX_MEETING_HOUR = 18
def is_good_meeting_time(utc_datetime, timezones):
    try:
        zones = [ZoneInfo(name) for name in timezones]
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise ValueError('Unknown timezone') from error
    dt = utc_datetime.replace(tzinfo=timezone.utc) if utc_datetime.tzinfo is None else utc_datetime
    return all(MIN_MEETING_HOUR <= dt.astimezone(zone).hour < MAX_MEETING_HOUR for zone in zones)''',
    [("is_good_meeting_time(datetime(2020, 1, 1, 9), ['UTC'])", 'True'),
     ("is_good_meeting_time(datetime(2020, 1, 1, 18), ['UTC'])", 'False'),
     ("is_good_meeting_time(datetime(2020, 1, 1, 16), ['US/Arizona', 'Europe/Madrid'])", 'True'),
     ("is_good_meeting_time(datetime(2020, 7, 1, 16), ['US/Arizona', 'Europe/Madrid'])", 'False'),
     ("is_good_meeting_time(datetime(2020, 1, 1, 0), [])", 'True'),
     ("is_good_meeting_time(datetime(2020, 1, 1, 10, tzinfo=timezone(timedelta(hours=2))), ['UTC'])", 'False')],
    [('inclusive closing hour', 'hour < MAX_MEETING_HOUR', 'hour <= MAX_MEETING_HOUR'),
     ('any zone instead of all', 'return all(', 'return any(')],
    r'''def test_unknown_timezone():
    with pytest.raises(ValueError):
        is_good_meeting_time(datetime(2020, 1, 1, 0), ['UTC', 'Wrong/Zone'])
''')

add(11, 'pretty_dates',
    'pretty_date(value, now=NOW) accepts naive datetimes. NOW is fixed at 2019-03-20 12:00. Return "just now" for less than one second; otherwise use whole seconds, minutes, hours, or days with singular/plural and " ago". Use the largest whole unit. At exactly two days return "2 days ago". For older dates return MM/DD/YY. Future dates and non-datetime inputs raise ValueError.',
    r'''from datetime import datetime
NOW = datetime(2019, 3, 20, 12)
TIME_OFFSETS = ((86400, 'day'), (3600, 'hour'), (60, 'minute'), (1, 'second'))
def pretty_date(value, now=NOW):
    pass''',
    r'''from datetime import datetime
NOW = datetime(2019, 3, 20, 12)
TIME_OFFSETS = ((86400, 'day'), (3600, 'hour'), (60, 'minute'), (1, 'second'))
def pretty_date(value, now=NOW):
    if not isinstance(value, datetime) or value > now:
        raise ValueError('Expected a past datetime')
    seconds = (now - value).total_seconds()
    if seconds > 172800:
        return value.strftime('%m/%d/%y')
    for size, unit in TIME_OFFSETS:
        count = int(seconds // size)
        if count:
            return f'{count} {unit}{"s" if count != 1 else ""} ago'
    return 'just now' ''',
    [('pretty_date(NOW)', "'just now'"), ('pretty_date(NOW - timedelta(seconds=1))', "'1 second ago'"),
     ('pretty_date(NOW - timedelta(seconds=59))', "'59 seconds ago'"), ('pretty_date(NOW - timedelta(seconds=60))', "'1 minute ago'"),
     ('pretty_date(NOW - timedelta(seconds=3599))', "'59 minutes ago'"), ('pretty_date(NOW - timedelta(hours=1))', "'1 hour ago'"),
     ('pretty_date(NOW - timedelta(days=1))', "'1 day ago'"), ('pretty_date(NOW - timedelta(days=2))', "'2 days ago'"),
     ('pretty_date(NOW - timedelta(days=2, seconds=1))', "'03/18/19'")],
    [('exclude two-day boundary', 'seconds > 172800', 'seconds >= 172800'),
     ('always plural', 'count != 1', 'True')],
    r'''def test_invalid():
    for value in ('yesterday', 123, None, NOW + timedelta(seconds=1)):
        with pytest.raises(ValueError):
            pretty_date(value)
''')

add(12, 'date_inferrer',
    'DateFormat is an Enum of allowed strptime patterns. get_dates(values) counts every pattern that can parse each string. An ambiguous string votes for each matching pattern. A value that matches none votes once for nonparsable. Choose the unique most frequent pattern; reject empty input, a pattern tie, or a nonparsable count greater than the winning pattern count with InfDateFmtError. Parse all values with the winning pattern into YYYY-MM-DD, using "Invalid" for failures. Read the current DateFormat dynamically; tests can replace it.',
    r'''from enum import Enum
from datetime import datetime
class DateFormat(Enum):
    EU = '%d/%m/%Y'
    US = '%m/%d/%Y'
    ISO = '%Y-%m-%d'
class InfDateFmtError(ValueError):
    pass
def get_dates(values):
    pass''',
    r'''from enum import Enum
from datetime import datetime
class DateFormat(Enum):
    EU = '%d/%m/%Y'
    US = '%m/%d/%Y'
    ISO = '%Y-%m-%d'
class InfDateFmtError(ValueError):
    pass
def get_dates(values):
    formats = [item.value for item in DateFormat]
    counts = dict.fromkeys(formats, 0)
    parsed = []
    invalid = 0
    for value in values:
        matches = {}
        for pattern in formats:
            try:
                matches[pattern] = datetime.strptime(value, pattern)
                counts[pattern] += 1
            except (ValueError, TypeError):
                pass
        parsed.append(matches)
        invalid += not bool(matches)
    best = max(counts.values(), default=0)
    winners = [pattern for pattern, count in counts.items() if count == best]
    if not best or len(winners) != 1 or invalid > best:
        raise InfDateFmtError('Cannot infer a unique format')
    pattern = winners[0]
    return [row[pattern].date().isoformat() if pattern in row else 'Invalid' for row in parsed]''',
    [("get_dates(['13/02/2020', '01/02/2020'])", "['2020-02-13', '2020-02-01']"),
     ("get_dates(['02/13/2020', '02/01/2020'])", "['2020-02-13', '2020-02-01']"),
     ("get_dates(['2020-02-29', 'bad'])", "['2020-02-29', 'Invalid']"),
     ("get_dates(['13/02/2020', '14/02/2020', '02/15/2020'])", "['2020-02-13', '2020-02-14', 'Invalid']"),
     ("get_dates(['2020-01-01', '2019-02-29', '2020-02-29'])", "['2020-01-01', 'Invalid', '2020-02-29']")],
    [('reject invalid-count equality', 'invalid > best', 'invalid >= best'),
     ('lose order', 'for row in parsed]', 'for row in reversed(parsed)]')],
    r'''def test_ambiguous_or_invalid_majority():
    for values in ([], ['01/02/2020'], ['13/02/2020', '02/13/2020'], ['2020-01-01', 'x', 'y']):
        with pytest.raises(InfDateFmtError):
            get_dates(values)

def test_four_digit_year():
    assert get_dates(['0001-01-01', '0999-12-31']) == ['0001-01-01', '0999-12-31']

def test_replaced_enum(monkeypatch):
    from enum import Enum
    alternate = Enum('DateFormat', {'SHORT': '%d.%m.%y'})
    monkeypatch.setattr(subject, 'DateFormat', alternate)
    assert get_dates(['29.02.20', 'no']) == ['2020-02-29', 'Invalid']
''')

add(13, 'months_passed',
    'START_DATE is date(2018, 11, 1). get_months_passed(year, month, day) constructs an end date and returns completed calendar months plus one if the remaining days are at least 10. Dates before START_DATE and invalid calendar dates raise ValueError. Non-integer date components raise TypeError. Use the standard library.',
    r'''from datetime import date
START_DATE = date(2018, 11, 1)
def get_months_passed(year, month, day):
    pass''',
    r'''from datetime import date
START_DATE = date(2018, 11, 1)
def get_months_passed(year, month, day):
    end = date(year, month, day)
    if end < START_DATE:
        raise ValueError('End before start')
    months = (end.year - START_DATE.year) * 12 + end.month - START_DATE.month
    return months + (end.day - START_DATE.day >= 10)''',
    [('get_months_passed(2018, 11, 1)', '0'), ('get_months_passed(2018, 11, 10)', '0'),
     ('get_months_passed(2018, 11, 11)', '1'), ('get_months_passed(2019, 1, 1)', '2'),
     ('get_months_passed(2020, 2, 29)', '16'), ('get_months_passed(2019, 11, 1)', '12')],
    [('round after eleven days', '>= 10', '> 10'), ('omit years', '(end.year - START_DATE.year) * 12', '0')],
    r'''def test_invalid_calendar_and_past():
    for args in ((2018, 10, 31), (2019, 2, 29), (2020, 13, 1)):
        with pytest.raises(ValueError):
            get_months_passed(*args)
    with pytest.raises(TypeError):
        get_months_passed('2020', 1, 1)
''')

add(14, 'weekdays',
    'get_hundred_weekdays(start_date=TODAY) returns a list of exactly 100 date objects, in ascending order. Include start_date if it is Monday-Friday; otherwise begin the next Monday. Skip Saturdays and Sundays. TODAY is fixed at date(2019, 1, 1). No holiday filtering. Use the standard library.',
    r'''from datetime import date, timedelta
TODAY = date(2019, 1, 1)
def get_hundred_weekdays(start_date=TODAY):
    pass''',
    r'''from datetime import date, timedelta
TODAY = date(2019, 1, 1)
def get_hundred_weekdays(start_date=TODAY):
    result = []
    current = start_date
    while len(result) < 100:
        if current.weekday() < 5:
            result.append(current)
        current += timedelta(days=1)
    return result''',
    [('len(get_hundred_weekdays())', '100'), ('get_hundred_weekdays(date(2020, 2, 28))[:3]', '[date(2020, 2, 28), date(2020, 3, 2), date(2020, 3, 3)]'),
     ('get_hundred_weekdays(date(2020, 2, 29))[0]', 'date(2020, 3, 2)'),
     ('get_hundred_weekdays(date(2020, 3, 1))[0]', 'date(2020, 3, 2)'),
     ('get_hundred_weekdays()[0]', 'date(2019, 1, 1)'), ('get_hundred_weekdays()[-1]', 'date(2019, 5, 20)'),
     ('all(d.weekday() < 5 for d in get_hundred_weekdays())', 'True'),
     ('len(set(get_hundred_weekdays()))', '100')],
    [('include Saturday', 'weekday() < 5', 'weekday() < 6'), ('too few days', 'len(result) < 100', 'len(result) < 99')])

_COMPOSERS = r'''from collections import namedtuple
from datetime import datetime
Opera = namedtuple('Opera', 'author play date')
Composer = namedtuple('Composer', 'name born died')
# Constructed fixture names and dates; not a historical opera database.
composers = {
    'Aster': Composer('Aster', '1700-01-01', '1760-01-01'),
    'Birch': Composer('Birch', '1730-06-01', '1790-01-01'),
    'Cedar': Composer('Cedar', '1761-01-01', '1820-01-01'),
}
operas = [Opera('Aster', 'Early', '1729-01-01'),
          Opera('Aster', 'Together', '1750-01-01'),
          Opera('Aster', 'Farewell', '1760-01-01'),
          Opera('Birch', 'Later', '1780-01-01')]
def _get_date(value):
    return datetime.strptime(value, '%Y-%m-%d')
'''
add(15, 'composers_dates',
    'operas_both_at_premiere(guest, composer) returns a list of the given author\'s opera titles where both people were alive at the premiere, in fixture order. Birth and death dates are inclusive. Use the module composers dictionary and operas list. Unknown names raise ValueError. Equal guest and composer names are allowed. Dates use YYYY-MM-DD. The supplied namedtuple fixtures are constructed examples.',
    _COMPOSERS + r'''def operas_both_at_premiere(guest, composer):
    pass''',
    _COMPOSERS + r'''def operas_both_at_premiere(guest, composer):
    if guest not in composers or composer not in composers:
        raise ValueError('Unknown composer')
    people = [composers[guest], composers[composer]]
    return [opera.play for opera in operas if opera.author == composer and
            all(_get_date(person.born) <= _get_date(opera.date) <= _get_date(person.died) for person in people)]''',
    [("operas_both_at_premiere('Birch', 'Aster')", "['Together', 'Farewell']"),
     ("operas_both_at_premiere('Cedar', 'Aster')", '[]'),
     ("operas_both_at_premiere('Aster', 'Birch')", '[]'),
     ("operas_both_at_premiere('Cedar', 'Birch')", "['Later']"),
     ("operas_both_at_premiere('Aster', 'Aster')", "['Early', 'Together', 'Farewell']")],
    [('exclude death day', '<= _get_date(person.died)', '< _get_date(person.died)'),
     ('ignore author filter', 'opera.author == composer and', 'True and')],
    r'''def test_unknown_people():
    with pytest.raises(ValueError):
        operas_both_at_premiere('unknown', 'Aster')
    with pytest.raises(ValueError):
        operas_both_at_premiere('Aster', 'unknown')

def test_birth_day_and_author_lifetime(monkeypatch):
    monkeypatch.setattr(subject, 'operas', [Opera('Aster', 'Birth', '1730-06-01'), Opera('Aster', 'Posthumous', '1770-01-01')])
    assert operas_both_at_premiere('Birch', 'Aster') == ['Birth']
''')

add(16, 'timer',
    'add_todo(duration, description, start_time=NOW) returns "description @ YYYY-MM-DD HH:MM:SS". NOW is 2019-02-06 22:00. duration contains space-separated nonnegative integer tokens with suffix d, h, m, or s. Accept repeated units and any order. Reject empty strings, unknown units, negative values, and malformed tokens with ValueError.',
    r'''from datetime import datetime, timedelta
import re
NOW = datetime(2019, 2, 6, 22)
def add_todo(duration, description, start_time=NOW):
    pass''',
    r'''from datetime import datetime, timedelta
import re
NOW = datetime(2019, 2, 6, 22)
def add_todo(duration, description, start_time=NOW):
    units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    tokens = duration.split()
    if not tokens:
        raise ValueError('Empty duration')
    seconds = 0
    for token in tokens:
        match = re.fullmatch(r'(\d+)([dhms])', token)
        if not match:
            raise ValueError('Invalid token')
        seconds += int(match[1]) * units[match[2]]
    when = start_time + timedelta(seconds=seconds)
    return f'{description} @ {when.year:04}-{when:%m-%d %H:%M:%S}' ''',
    [("add_todo('11h 10m', 'Wash my car')", "'Wash my car @ 2019-02-07 09:10:00'"),
     ("add_todo('30d', 'Code a Bite')", "'Code a Bite @ 2019-03-08 22:00:00'"),
     ("add_todo('5m 3s', 'Go to Bed')", "'Go to Bed @ 2019-02-06 22:05:03'"),
     ("add_todo('1m 2m 0s', 'repeat')", "'repeat @ 2019-02-06 22:03:00'"),
     ("add_todo('1s', '', datetime(2019, 12, 31, 23, 59, 59))", "' @ 2020-01-01 00:00:00'"),
     ("add_todo('0s', 'now')", "'now @ 2019-02-06 22:00:00'")],
    [('ignore minutes', "'m': 60", "'m': 1"), ('accept trailing junk', 're.fullmatch(', 're.match(')],
    r'''def test_four_digit_year():
    assert add_todo('0s', 'test', datetime(1, 1, 1)) == 'test @ 0001-01-01 00:00:00'

def test_invalid_tokens():
    for value in ('', '-1h', '1w', '2mJUNK', '1 h'):
        with pytest.raises(ValueError):
            add_todo(value, 'bad')
''')

add(17, 'missing_dates',
    'Keep the source spelling: get_misssing_dates(dates) returns a set of missing date objects strictly between the minimum and maximum supplied dates. Accept unordered values and duplicates. Empty and singleton sequences return an empty set.',
    r'''from datetime import timedelta
def get_misssing_dates(dates):
    pass''',
    r'''from datetime import timedelta
def get_misssing_dates(dates):
    present = set(dates)
    if not present:
        return set()
    current, end = min(present), max(present)
    missing = set()
    while current < end:
        if current not in present:
            missing.add(current)
        current += timedelta(days=1)
    return missing''',
    [('get_misssing_dates([])', 'set()'), ('get_misssing_dates([date(2020, 1, 1)])', 'set()'),
     ('get_misssing_dates([date(2020, 1, 3), date(2020, 1, 1), date(2020, 1, 1)])', '{date(2020, 1, 2)}'),
     ('get_misssing_dates([date(2020, 2, 28), date(2020, 3, 1)])', '{date(2020, 2, 29)}'),
     ('get_misssing_dates([date(2019, 12, 31), date(2020, 1, 2)])', '{date(2020, 1, 1)}'),
     ('get_misssing_dates([date(2020, 1, 1), date(2020, 1, 2)])', 'set()')],
    [('skip every other day', 'timedelta(days=1)', 'timedelta(days=2)'), ('include present days', 'current not in present', 'True')])

add(18, 'commit_log',
    'get_min_max_amount_of_commits(log, year=None) parses nonblank git-stat rows of the form "Date: Tue Mar 5 22:34:33 2019 +0100 | 2 files changed, 4 insertions(+), 3 deletions(-)". Sum insertions plus deletions by YYYY-MM in the printed local date. A missing insertion/deletion term counts as zero. Ignore file counts. Optional year filters months. Return (least_month, most_month), selecting the earliest month for ties in either position. No matching rows returns (None, None). Malformed rows raise ValueError.',
    r'''from datetime import datetime
from collections import Counter
import re
YEAR_MONTH = '%Y-%m'
def get_min_max_amount_of_commits(log, year=None):
    pass''',
    r'''from datetime import datetime
from collections import Counter
import re
YEAR_MONTH = '%Y-%m'
def get_min_max_amount_of_commits(log, year=None):
    counts = Counter()
    for line in log.splitlines():
        if not line.strip():
            continue
        stamp, changes = line.split('|', 1)
        if not stamp.strip().startswith('Date:') or not re.fullmatch(r'\d+ files? changed(?:, \d+ insertions?\(\+\))?(?:, \d+ deletions?\(-\))?', changes.strip()):
            raise ValueError('Malformed git stat row')
        dt = datetime.strptime(stamp.strip().removeprefix('Date:').strip(), '%a %b %d %H:%M:%S %Y %z')
        if year is not None and dt.year != year:
            continue
        amount = sum(int(n) for n in re.findall(r'(\d+) (?:insertion|deletion)s?\(', changes))
        counts[f'{dt.year:04}-{dt.month:02}'] += amount
    if not counts:
        return None, None
    low = min(counts, key=lambda month: (counts[month], month))
    high = min(counts, key=lambda month: (-counts[month], month))
    return low, high''',
    [("get_min_max_amount_of_commits('')", '(None, None)'),
     ("get_min_max_amount_of_commits('Date: Tue Mar 5 22:34:33 2019 +0100 | 2 files changed, 4 insertions(+), 3 deletions(-)')", "('2019-03', '2019-03')"),
     ("get_min_max_amount_of_commits('Date: Tue Mar 5 22:34:33 2019 +0100 | 2 files changed, 4 insertions(+)\\nDate: Tue Jan 1 22:00:00 2019 +0100 | 9 files changed, 6 deletions(-)')", "('2019-03', '2019-01')"),
     ("get_min_max_amount_of_commits('Date: Tue Mar 5 22:34:33 2019 +0100 | 2 files changed, 4 insertions(+)\\nDate: Tue Jan 1 22:00:00 2019 +0100 | 1 file changed, 4 deletions(-)')", "('2019-01', '2019-01')"),
     ("get_min_max_amount_of_commits('Date: Tue Mar 5 22:34:33 2019 +0100 | 2 files changed, 4 insertions(+)', 2018)", '(None, None)')],
    [('exclude deletions', '(?:insertion|deletion)', '(?:insertion)'),
     ('ignore year filter', 'year is not None and dt.year != year', 'False')],
    r'''def test_four_digit_year():
    assert get_min_max_amount_of_commits('Date: Mon Jan 1 00:00:00 0001 +0000 | 1 file changed') == ('0001-01', '0001-01')

def test_malformed_stat_rows():
    for line in ('Date: Tue Mar 5 22:34:33 2019 +0100 | garbage', 'Date: Tue Mar 5 22:34:33 2019 +0100 | 1 file changed, four insertions(+)', 'Tue Mar 5 22:34:33 2019 +0100 | 1 file changed, 1 insertion(+)'):
        with pytest.raises(ValueError):
            get_min_max_amount_of_commits(line)

def test_accumulate_same_month_and_keep_local_month():
    log = """Date: Tue Jan 1 00:00:00 2019 +1400 | 1 file changed, 3 insertions(+)
Date: Wed Jan 2 00:00:00 2019 +1400 | 1 file changed, 3 deletions(-)
Date: Fri Feb 1 00:00:00 2019 +0000 | 1 file changed, 5 insertions(+)"""
    assert get_min_max_amount_of_commits(log) == ('2019-02', '2019-01')
''')

add(19, 'books',
    'get_number_books_read(goal, at_date=NOW) returns int(round(ISO_week / 52 * goal)); Python round uses ties to even. goal must be a positive integer. NOW is fixed at date(2019, 1, 1). Reject dates before NOW. Accept date objects, ISO YYYY-MM-DD, M-D-YYYY, and strings like "Sunday, March 25th, 2019". For the last form, ignore the weekday text and remove ordinal suffixes. Bad goals or dates raise ValueError. Week 53 is allowed and can exceed the annual goal. WEEKS_PER_YEAR is 52.',
    r'''from datetime import date, datetime
import re
NOW = date(2019, 1, 1)
WEEKS_PER_YEAR = 52
def get_number_books_read(goal, at_date=NOW):
    pass''',
    r'''from datetime import date, datetime
import re
NOW = date(2019, 1, 1)
WEEKS_PER_YEAR = 52
def get_number_books_read(goal, at_date=NOW):
    if type(goal) is not int or goal <= 0:
        raise ValueError('Positive integer goal required')
    value = at_date
    if isinstance(value, str):
        cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', value)
        if ',' in cleaned:
            cleaned = cleaned.split(',', 1)[1].strip()
        for pattern in ('%Y-%m-%d', '%m-%d-%Y', '%B %d, %Y'):
            try:
                value = datetime.strptime(cleaned, pattern).date()
                break
            except ValueError:
                pass
    if type(value) is not date or value < NOW:
        raise ValueError('Valid current or future date required')
    return int(round(value.isocalendar().week / WEEKS_PER_YEAR * goal))''',
    [("get_number_books_read(100, 'Sunday, March 25th, 2019')", '25'),
     ("get_number_books_read(52, 'Sunday, March 18th, 2019')", '12'),
     ("get_number_books_read(100, '2019-11-18')", '90'),
     ("get_number_books_read(52, '3-18-2019')", '12'), ('get_number_books_read(52)', '1'), ('get_number_books_read(100)', '2'),
     ("get_number_books_read(52, date(2020, 12, 31))", '53'),
     ("get_number_books_read(52, '2019-12-30')", '1'),
     ("get_number_books_read(26, '2019-01-01')", '0')],
    [('truncate instead of round', 'int(round(value.isocalendar().week / WEEKS_PER_YEAR * goal))', 'int(value.isocalendar().week / WEEKS_PER_YEAR * goal)'),
     ('use calendar day count', 'value.isocalendar().week', '(value.timetuple().tm_yday // 7)')],
    r'''def test_invalid_goal_and_date():
    for goal, value in ((0, NOW), (-2, NOW), (True, NOW), (1.5, NOW), (52, '5-20-2018'), (52, 'not a date'), (52, None)):
        with pytest.raises(ValueError):
            get_number_books_read(goal, value)
''')

_ACTORS = r'''from dataclasses import dataclass
from datetime import datetime
@dataclass
class Actor:
    name: str
    born: str
@dataclass
class Movie:
    title: str
    release_date: str
'''
add(20, 'actor_age',
    'Actor(name, born) and Movie(title, release_date) are supplied dataclasses. Dates use full English month names: "July 31, 1962". get_age(actor, movie) returns "NAME was N years old when TITLE came out." Use completed birthdays. For a February 29 birth in a non-leap year, the birthday completes on March 1. Invalid dates or a release before birth raise ValueError.',
    _ACTORS + r'''def get_age(actor, movie):
    pass''',
    _ACTORS + r'''def get_age(actor, movie):
    born = datetime.strptime(actor.born, '%B %d, %Y').date()
    released = datetime.strptime(movie.release_date, '%B %d, %Y').date()
    if released < born:
        raise ValueError('Release before birth')
    age = released.year - born.year - ((released.month, released.day) < (born.month, born.day))
    return f'{actor.name} was {age} years old when {movie.title} came out.' ''',
    [("get_age(Actor('Wesley Snipes', 'July 31, 1962'), Movie('New Jack City', 'January 17, 1991'))", "'Wesley Snipes was 28 years old when New Jack City came out.'"),
     ("get_age(Actor('Jennifer Aniston', 'February 11, 1969'), Movie('Horrible Bosses', 'September 16, 2011'))", "'Jennifer Aniston was 42 years old when Horrible Bosses came out.'"),
     ("get_age(Actor('A', 'May 10, 2000'), Movie('B', 'May 10, 2020'))", "'A was 20 years old when B came out.'"),
     ("get_age(Actor('A', 'May 10, 2000'), Movie('B', 'May 9, 2020'))", "'A was 19 years old when B came out.'"),
     ("get_age(Actor('A', 'February 29, 2000'), Movie('B', 'February 28, 2021'))", "'A was 20 years old when B came out.'"),
     ("get_age(Actor('A', 'February 29, 2000'), Movie('B', 'March 1, 2021'))", "'A was 21 years old when B came out.'")],
    [('ignore birthday', '((released.month, released.day) < (born.month, born.day))', '0'),
     ('exclude birthday itself', '(released.month, released.day) < (born.month, born.day)', '(released.month, released.day) <= (born.month, born.day)')],
    r'''def test_release_before_birth():
    with pytest.raises(ValueError):
        get_age(Actor('A', 'May 10, 2000'), Movie('B', 'May 9, 2000'))
''')

add(21, 'mothers_day',
    'get_mothers_day_date(year) returns a date object for the second Sunday of May in the supplied year. Support valid Python date years 1-9999. Invalid years raise the standard date constructor errors. The source table covers 2014-2024; this version also checks later years.',
    r'''from datetime import date, timedelta
def get_mothers_day_date(year):
    pass''',
    r'''from datetime import date, timedelta
def get_mothers_day_date(year):
    first = date(year, 5, 1)
    return first + timedelta(days=(6 - first.weekday()) % 7 + 7)''',
    [('get_mothers_day_date(2014)', 'date(2014, 5, 11)'), ('get_mothers_day_date(2016)', 'date(2016, 5, 8)'),
     ('get_mothers_day_date(2019)', 'date(2019, 5, 12)'), ('get_mothers_day_date(2021)', 'date(2021, 5, 9)'),
     ('get_mothers_day_date(2022)', 'date(2022, 5, 8)'), ('get_mothers_day_date(2023)', 'date(2023, 5, 14)'),
     ('get_mothers_day_date(2024)', 'date(2024, 5, 12)'), ('get_mothers_day_date(2026)', 'date(2026, 5, 10)')],
    [('first Sunday', '% 7 + 7', '% 7'), ('Monday instead', '(6 - first.weekday())', '(0 - first.weekday())')])

add(22, 'srt',
    'get_srt_section_ids(text) parses blank-line-separated SRT blocks: integer ID, HH:MM:SS,mmm --> HH:MM:SS,mmm, and one or more caption lines. Join caption lines with one space; count all characters, including punctuation and internal spaces. Strip line edges. Rank by characters per second, descending. Preserve block order for equal rates. Return integer IDs. Empty input returns []. Reject invalid timestamps, duplicate IDs, and nonpositive duration with ValueError. Accept CRLF newlines.',
    r'''import re
def get_srt_section_ids(text):
    pass''',
    r'''import re
def get_srt_section_ids(text):
    def milliseconds(value):
        match = re.fullmatch(r'(\d{2,}):([0-5]\d):([0-5]\d),(\d{3})', value.strip())
        if not match:
            raise ValueError('Invalid SRT time')
        h, m, s, ms = map(int, match.groups())
        return ((h * 60 + m) * 60 + s) * 1000 + ms
    if not text.strip():
        return []
    result, seen = [], set()
    for block in re.split(r'\n\s*\n', text.replace('\r\n', '\n').strip()):
        lines = block.splitlines()
        if len(lines) < 3:
            raise ValueError('Missing caption')
        section = int(lines[0].strip())
        if section in seen:
            raise ValueError('Duplicate section')
        seen.add(section)
        start, end = lines[1].split('-->')
        duration = milliseconds(end) - milliseconds(start)
        if duration <= 0:
            raise ValueError('Nonpositive duration')
        caption = ' '.join(line.strip() for line in lines[2:])
        result.append((section, len(caption) / duration))
    return [section for section, rate in sorted(result, key=lambda row: -row[1])]''',
    [("get_srt_section_ids('')", '[]'),
     ("get_srt_section_ids('1\\n00:00:00,000 --> 00:00:01,000\\nhello')", '[1]'),
     ("get_srt_section_ids('1\\n00:00:00,000 --> 00:00:02,000\\nhello\\n\\n2\\n00:00:02,000 --> 00:00:03,000\\nhello')", '[2, 1]'),
     ("get_srt_section_ids('9\\n00:00:00,000 --> 00:00:01,000\\nhello\\n\\n2\\n00:00:01,000 --> 00:00:02,000\\nworld')", '[9, 2]'),
     ("get_srt_section_ids('1\\n00:00:59,900 --> 00:01:00,100\\nab\\n\\n2\\n00:01:00,100 --> 00:01:01,100\\nabcdef')", '[1, 2]'),
     ("get_srt_section_ids('1\\r\\n00:00:00,000 --> 00:00:01,000\\r\\na\\r\\nb\\r\\n\\r\\n2\\r\\n00:00:01,000 --> 00:00:02,000\\r\\nxy')", '[1, 2]')],
    [('slowest first', 'key=lambda row: -row[1]', 'key=lambda row: row[1]'),
     ('ignore multiline spaces', "caption = ' '.join", "caption = ''.join")],
    r'''def test_multiline_space_affects_ranking():
    text = '1\n00:00:00,000 --> 00:00:01,000\nxy\n\n2\n00:00:01,000 --> 00:00:02,000\na\nb'
    assert get_srt_section_ids(text) == [2, 1]

def test_invalid_srt():
    for text in ('1\n00:00:00,000 --> 00:00:00,000\na', '1\n00:00:01,000 --> 00:00:00,000\na', '1\n00:60:00,000 --> 00:61:00,000\na', '1\n00:00:00,000 --> 00:00:01,000\na\n\n1\n00:00:01,000 --> 00:00:02,000\nb'):
        with pytest.raises(ValueError):
            get_srt_section_ids(text)
''')

add(23, 'coding_streak',
    'extract_dates(text) returns a list of date objects from pipe-table rows whose first cell is YYYY-MM-DD. Ignore headers and borders. Keep duplicates and input order. Invalid ISO-shaped dates raise ValueError. calculate_streak(dates, today=TODAY) returns consecutive unique coding days ending today, or yesterday if today is absent. If both are absent, return 0. Ignore future dates. TODAY is fixed at date(2018, 11, 12).',
    r'''from datetime import date, timedelta
import re
TODAY = date(2018, 11, 12)
def extract_dates(text):
    pass
def calculate_streak(dates, today=TODAY):
    pass''',
    r'''from datetime import date, timedelta
import re
TODAY = date(2018, 11, 12)
def extract_dates(text):
    return [date.fromisoformat(value) for value in re.findall(r'^\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|', text, re.M)]
def calculate_streak(dates, today=TODAY):
    present = set(dates)
    current = today if today in present else today - timedelta(days=1)
    count = 0
    while current in present:
        count += 1
        current -= timedelta(days=1)
    return count''',
    [("extract_dates('| date | activity |\\n| 2018-11-11 | pcc | 1 |\\n| 2018-11-11 | bite | 2 |')", '[date(2018, 11, 11), date(2018, 11, 11)]'),
     ('calculate_streak([])', '0'), ('calculate_streak([date(2018, 11, 10)])', '0'),
     ('calculate_streak([date(2018, 11, 11), date(2018, 11, 10), date(2018, 11, 9)])', '3'),
     ('calculate_streak([date(2018, 11, 12), date(2018, 11, 11), date(2018, 11, 11)])', '2'),
     ('calculate_streak([date(2018, 11, 13)])', '0'),
     ('calculate_streak([date(2020, 3, 1), date(2020, 2, 29), date(2020, 2, 28)], date(2020, 3, 1))', '3'),
     ('calculate_streak([date(2019, 12, 31), date(2020, 1, 1)], date(2020, 1, 1))', '2')],
    [('require today', 'today if today in present else today - timedelta(days=1)', 'today'),
     ('count all historical days', 'return count', 'return len(present)'),
     ('parse just one date', r'(\d{4}-\d{2}-\d{2})', '(2018-11-11)')],
    r'''def test_extract_distinct_dates_and_boundaries():
    text = '| date | activity | count |\n|------------+----------+-------|\n| 2019-12-31 | pcc | 1 |\n| 2020-01-01 | bite | 2 |\n| 2020-02-29 | bite | 1 |'
    assert extract_dates(text) == [date(2019, 12, 31), date(2020, 1, 1), date(2020, 2, 29)]
    assert extract_dates('| date | activity |\n+------------+----------+') == []
    assert extract_dates('') == []
    with pytest.raises(ValueError):
        extract_dates('| 2019-02-29 | bite | 1 |')
''')

add(24, 'uptime',
    'get_longest_uptime(text, year=2019) reads lines such as "reboot    ~    Wed Apr 10 22:39". All events belong to year. Sort events, then return the largest timedelta between adjacent events. Duplicate events are allowed. Fewer than two events returns timedelta(0). Ignore blank lines and non-reboot lines. Invalid reboot dates raise ValueError. Do not include the time since the last reboot. Year boundaries are outside this contract; the year argument supports leap years.',
    r'''from datetime import datetime, timedelta
def get_longest_uptime(text, year=2019):
    pass''',
    r'''from datetime import datetime, timedelta
def get_longest_uptime(text, year=2019):
    events = []
    for line in text.splitlines():
        if not line.strip() or line.split()[0] != 'reboot':
            continue
        parts = line.split()
        stamp = ' '.join(parts[-4:])
        events.append(datetime.strptime(f'{year:04d} {stamp}', '%Y %a %b %d %H:%M'))
    events.sort()
    return max((b - a for a, b in zip(events, events[1:])), default=timedelta(0))''',
    [("get_longest_uptime('')", 'timedelta(0)'),
     ("get_longest_uptime('reboot ~ Wed Apr 10 22:39')", 'timedelta(0)'),
     ("get_longest_uptime('reboot ~ Wed Apr 10 22:39\\nreboot ~ Wed Mar 27 16:24')", 'timedelta(days=14, hours=6, minutes=15)'),
     ("get_longest_uptime('reboot ~ Wed Mar 27 15:01\\nreboot ~ Wed Mar 27 16:24')", 'timedelta(minutes=83)'),
     ("get_longest_uptime('reboot ~ Wed Mar 27 16:24\\nreboot ~ Wed Mar 27 15:01\\nreboot ~ Wed Mar 27 16:24')", 'timedelta(minutes=83)'),
     ("get_longest_uptime('reboot ~ Sun Mar 1 00:00\\nreboot ~ Fri Feb 28 00:00', 2020)", 'timedelta(days=2)'),
     ("get_longest_uptime('wtmp begins Mon Jan 1\\nreboot ~ Mon Jan 14 09:25\\nreboot ~ Thu Jan 17 21:54\\nreboot ~ Sun Feb 17 11:36')", 'timedelta(days=30, hours=13, minutes=42)')],
    [('return shortest interval', 'return max(', 'return min('),
     ('keep only whole days', 'b - a for a, b', 'timedelta(days=(b - a).days) for a, b')],
    r'''def test_invalid_reboot_dates():
    for text in ('reboot ~ Fri Feb 29 00:00', 'reboot ~ garbage', 'reboot ~ Wed Apr 10 24:00'):
        with pytest.raises(ValueError):
            get_longest_uptime(text)

def test_four_digit_year():
    assert get_longest_uptime('reboot ~ Mon Jan 1 00:00\nreboot ~ Tue Jan 2 01:00', 1) == timedelta(days=1, hours=1)
''')

# The judge image need not have system tzdata. Both code versions use the same
# supplied database and return real standard-library ZoneInfo objects.
from cojudge.datetimes_path.fixtures import TIMEZONE_SUPPORT
for _key in ('template', 'reference'):
    SPECS[9][_key] = TIMEZONE_SUPPORT + SPECS[9][_key].replace(
        'from zoneinfo import ZoneInfo, ZoneInfoNotFoundError\n', '')
SPECS[9]['contract'] += ' The supplied ZoneInfo loader reads bundled IANA 2026b timezone data, including legacy aliases. Keep this supplied loader; it returns standard-library ZoneInfo objects.'
