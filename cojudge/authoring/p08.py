"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 8,
 'slug': 'aware-utc-normalization',
 'title': 'Normalize aware timestamps to UTC',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Lists, dictionaries, and functions.',
 'learn': 'An aware datetime has a time zone offset. It identifies an instant rather than an '
          'unqualified wall-clock reading. To express that instant in another time zone, use '
          'astimezone. Replacing tzinfo changes the label without adjusting the clock and usually '
          'changes the instant. An offset conversion can move the date to the previous or next '
          'day. Fixed offsets already contain the information needed for this task. They do not '
          'require local time zone rules. Parse each timestamp, convert it to UTC, and format all '
          'outputs in one consistent form. Preserve the input order because normalization does not '
          'imply sorting.',
 'scenario': ("A travel company receives booking times from partners in many time zones. Each time has an offset, such as `-07:00`. The company's database stores all times in UTC. `solve` converts each timestamp to UTC."),
 'example_notes': ['09:30 at -07:00 is 16:30 UTC. It is the same instant as the second timestamp.', '00:15 at +02:00 on January 1 is 22:15 UTC on the previous day, in the previous year.', 'No timestamps.'],
 'task': ('**Input:** `data` has:\n'
    '- `timestamps`: a list of valid strings, each in one of these forms:\n'
    '  - `YYYY-MM-DDTHH:MM:SSZ`\n'
    '  - `YYYY-MM-DDTHH:MM:SS±HH:MM`, with an offset from `-14:00` to `+14:00`\n'
    '\n'
    'Years are 2000–2099. All dates and times are valid. There are no leap seconds, no fractional seconds, and no zone names such as `America/Tijuana`.\n'
    '\n'
    '**Return** the same instants converted to UTC, in input order, each as `YYYY-MM-DDTHH:MM:SSZ`. A UTC result can fall outside 2000–2099.'),
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['Parse an aware datetime for each input.',
           'Convert the instant with astimezone, then format it.'],
 'starter': 'def solve(data: dict) -> list[str]:\n    raise NotImplementedError\n',
 'reference': 'from datetime import datetime, timezone\n'
              '\n'
              'def solve(data: dict) -> list[str]:\n'
              '    result = []\n'
              "    for text in data['timestamps']:\n"
              "        instant = datetime.fromisoformat(text.replace('Z', '+00:00'))\n"
              '        '
              "result.append(instant.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))\n"
              '    return result\n',
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    List<Object> out=new ArrayList<>(); DateTimeFormatter '
         'fmt=DateTimeFormatter.ofPattern("uuuu-MM-dd\'T\'HH:mm:ss\'Z\'");\n'
         '    for(Object x:arr(d.get("timestamps"))) '
         'out.add(OffsetDateTime.parse(s(x)).withOffsetSameInstant(ZoneOffset.UTC).format(fmt));\n'
         '    return out;\n'
         '}',
 'approach': 'The reference processes the input in one pass. Time is O(n), and result storage is '
             'O(n). The output judge checks results. It cannot prove the requested Python '
             'technique. This is an in-memory exercise; it does not provide storage or concurrency '
             'control.',
 'cases': [{'input': {'timestamps': ['2026-10-26T09:30:00-07:00', '2026-10-26T16:30:00Z']},
            'expected': ['2026-10-26T16:30:00Z', '2026-10-26T16:30:00Z'],
            'label': 'same instant from two offsets'},
           {'input': {'timestamps': ['2026-01-01T00:15:00+02:00']},
            'expected': ['2025-12-31T22:15:00Z'],
            'label': 'previous day and year'},
           {'input': {'timestamps': []}, 'expected': [], 'label': 'empty list'},
           {'input': {'timestamps': ['2026-01-01T00:00:00Z']},
            'expected': ['2026-01-01T00:00:00Z'],
            'label': 'already UTC'},
           {'input': {'timestamps': ['2026-12-31T23:30:00-02:00']},
            'expected': ['2027-01-01T01:30:00Z'],
            'label': 'next year'},
           {'input': {'timestamps': ['2024-03-01T00:30:00+01:00']},
            'expected': ['2024-02-29T23:30:00Z'],
            'label': 'leap day rollover'},
           {'input': {'timestamps': ['2023-03-01T00:30:00+01:00']},
            'expected': ['2023-02-28T23:30:00Z'],
            'label': 'non-leap year rollover'},
           {'input': {'timestamps': ['2026-06-01T12:00:00+05:30']},
            'expected': ['2026-06-01T06:30:00Z'],
            'label': 'half-hour offset'},
           {'input': {'timestamps': ['2026-06-01T12:00:00+05:45']},
            'expected': ['2026-06-01T06:15:00Z'],
            'label': 'quarter-hour offset'},
           {'input': {'timestamps': ['2000-01-01T00:00:00+14:00']},
            'expected': ['1999-12-31T10:00:00Z'],
            'label': 'largest positive offset'},
           {'input': {'timestamps': ['2099-12-31T23:59:59-14:00']},
            'expected': ['2100-01-01T13:59:59Z'],
            'label': 'largest negative offset'},
           {'input': {'timestamps': ['2026-01-02T00:00:00+00:00', '2026-01-01T00:00:00-00:00']},
            'expected': ['2026-01-02T00:00:00Z', '2026-01-01T00:00:00Z'],
            'label': 'zero offsets and unsorted input'},
           {'input': {'timestamps': ['2026-10-26T01:02:03-03:30']},
            'expected': ['2026-10-26T04:32:03Z'],
            'label': 'negative fractional-hour offset'}],
 'generated': [{'timestamps': ['2026-07-01T00:15:45+05:30', '2026-07-01T23:45:15-08:00']},
               {'timestamps': ['2026-07-02T00:15:45+05:30', '2026-07-02T23:45:15-08:00']},
               {'timestamps': ['2026-07-03T00:15:45+05:30', '2026-07-03T23:45:15-08:00']},
               {'timestamps': ['2026-07-04T00:15:45+05:30', '2026-07-04T23:45:15-08:00']},
               {'timestamps': ['2026-07-05T00:15:45+05:30', '2026-07-05T23:45:15-08:00']},
               {'timestamps': ['2026-07-06T00:15:45+05:30', '2026-07-06T23:45:15-08:00']},
               {'timestamps': ['2026-07-07T00:15:45+05:30', '2026-07-07T23:45:15-08:00']},
               {'timestamps': ['2026-07-08T00:15:45+05:30', '2026-07-08T23:45:15-08:00']},
               {'timestamps': ['2026-07-09T00:15:45+05:30', '2026-07-09T23:45:15-08:00']},
               {'timestamps': ['2026-07-10T00:15:45+05:30', '2026-07-10T23:45:15-08:00']},
               {'timestamps': ['2026-07-11T00:15:45+05:30', '2026-07-11T23:45:15-08:00']},
               {'timestamps': ['2026-07-12T00:15:45+05:30', '2026-07-12T23:45:15-08:00']}],
 'mutations': [{'name': 'relabels local clock as UTC',
                'old': 'instant.astimezone(timezone.utc)',
                'new': 'instant.replace(tzinfo=timezone.utc)'}],
 'sources': ['https://docs.python.org/3.11/library/datetime.html#datetime.datetime.astimezone']}
