"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 3,
 'slug': 'missing-null-zero',
 'title': 'Keep missing, null, and zero separate',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Lists, dictionaries, and functions.',
 'learn': 'A field can be absent, present with null, or present with zero. These states often have '
          'different meanings. Dictionary membership tells you whether a key exists. A value of '
          'None represents JSON null after decoding. Zero is a configured numeric value, even '
          'though it is false in a boolean condition. An expression such as value or default '
          'merges these states and can replace a valid zero. Write the decision in the same order '
          'as the contract: first check membership, then inspect the stored value. This makes '
          'defaults explicit and avoids an accidental change to a caller’s configuration.',
 'scenario': ('You work on the alert service of a banking app. Each customer can set a daily limit for push alerts. The app stores one settings record per customer. Before the service sends alerts, it calls `solve` to get the real limit of each customer.\n'
    '\n'
    'A record can be in three states:\n'
    '- The customer never opened the setting: there is no `limit` key, so use the company default.\n'
    '- The customer chose "no limit": `limit` is `null`. Keep `null`, so the service does not cap their alerts.\n'
    '- The customer chose a number: keep it. `0` means "send me no alerts".\n'
    '\n'
    'The product team also counts how many customers set their own limit (a number, including 0).'),
 'example_notes': ['Customer 1 never set a limit (default 10). Customer 2 chose no limit. Customer 3 muted alerts (0). Customer 4 chose 4. Customers 3 and 4 set a number, so `configured` is 2.', 'Two customers both chose 2. Count customers, not different values.', 'No customers in this batch.'],
 'task': ('**Input:** `data` has:\n'
    '- `default`: a nonnegative integer.\n'
    '- `records`: a list of objects. A record can have a `limit` key whose value is a nonnegative integer or `null`. Ignore all other keys.\n'
    '\n'
    '**Rules:** resolve the limit of each record.\n'
    '- No `limit` key → `default`.\n'
    '- `limit` is `null` → `null`.\n'
    '- `limit` is a number, including `0` → that number.\n'
    '\n'
    '**Return** `{"limits": [...], "configured": int}`\n'
    '- `limits`: the resolved limit of each record, in input order.\n'
    '- `configured`: the number of records that have a `limit` key with a non-null value. A `0` counts.'),
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['Use key membership to detect absence.', 'Use is not None to count configured values.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'def solve(data: dict) -> dict:\n'
              '    limits = []\n'
              '    configured = 0\n'
              "    for record in data['records']:\n"
              "        if 'limit' not in record:\n"
              "            limits.append(data['default'])\n"
              '        else:\n'
              "            value = record['limit']\n"
              '            limits.append(value)\n'
              '            if value is not None:\n'
              '                configured += 1\n'
              "    return {'limits': limits, 'configured': configured}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    List<Object> limits=new ArrayList<>(); int count=0;\n'
         '    for(Object x:arr(d.get("records"))) { Map<String,Object> r=obj(x);\n'
         '        if(!r.containsKey("limit")) limits.add(d.get("default"));\n'
         '        else { Object value=r.get("limit"); limits.add(value); if(value!=null) count++; '
         '}\n'
         '    }\n'
         '    return map("limits",limits,"configured",count);\n'
         '}',
 'approach': 'The reference processes the input in one pass. Time is O(n), and result storage is '
             'O(n). The output judge checks results. It cannot prove the requested Python '
             'technique. This is an in-memory exercise; it does not provide storage or concurrency '
             'control.',
 'cases': [{'input': {'default': 10, 'records': [{}, {'limit': None}, {'limit': 0}, {'limit': 4}]},
            'expected': {'limits': [10, None, 0, 4], 'configured': 2},
            'label': 'three distinct field states'},
           {'input': {'default': 5, 'records': [{'limit': 2}, {'limit': 2}]},
            'expected': {'limits': [2, 2], 'configured': 2},
            'label': 'count records, not distinct values'},
           {'input': {'default': 9, 'records': []},
            'expected': {'limits': [], 'configured': 0},
            'label': 'empty records'},
           {'input': {'default': 0, 'records': [{}]},
            'expected': {'limits': [0], 'configured': 0},
            'label': 'default zero is not configured'},
           {'input': {'default': 8, 'records': [{'limit': 0}]},
            'expected': {'limits': [0], 'configured': 1},
            'label': 'explicit zero is configured'},
           {'input': {'default': 3, 'records': [{'limit': None}]},
            'expected': {'limits': [None], 'configured': 0},
            'label': 'explicit null'},
           {'input': {'default': 6, 'records': [{}, {}]},
            'expected': {'limits': [6, 6], 'configured': 0},
            'label': 'several missing fields'},
           {'input': {'default': 1, 'records': [{'other': 0}]},
            'expected': {'limits': [1], 'configured': 0},
            'label': 'unrelated key'},
           {'input': {'default': 7, 'records': [{'limit': 8, 'other': None}]},
            'expected': {'limits': [8], 'configured': 1},
            'label': 'ignore extra fields'},
           {'input': {'default': 1000000, 'records': [{}, {'limit': 1000001}]},
            'expected': {'limits': [1000000, 1000001], 'configured': 1},
            'label': 'large values'},
           {'input': {'default': 4, 'records': [{'limit': None}, {'limit': None}, {}]},
            'expected': {'limits': [None, None, 4], 'configured': 0},
            'label': 'null and missing repeat'},
           {'input': {'default': 0, 'records': [{'limit': 0}, {'limit': None}, {}, {'limit': 1}]},
            'expected': {'limits': [0, None, 0, 1], 'configured': 2},
            'label': 'same output value has different origin'}],
 'generated': [{'default': 20,
                'records': [{'limit': 0}, {}, {'limit': None}, {'limit': 0}, {'x': 0}]},
               {'default': 21,
                'records': [{'limit': 1}, {}, {'limit': None}, {'limit': 0}, {'x': 1}]},
               {'default': 22,
                'records': [{'limit': 2}, {}, {'limit': None}, {'limit': 0}, {'x': 2}]},
               {'default': 23,
                'records': [{'limit': 3}, {}, {'limit': None}, {'limit': 0}, {'x': 3}]},
               {'default': 24,
                'records': [{'limit': 4}, {}, {'limit': None}, {'limit': 0}, {'x': 4}]},
               {'default': 25,
                'records': [{'limit': 5}, {}, {'limit': None}, {'limit': 0}, {'x': 5}]},
               {'default': 26,
                'records': [{'limit': 6}, {}, {'limit': None}, {'limit': 0}, {'x': 6}]},
               {'default': 27,
                'records': [{'limit': 7}, {}, {'limit': None}, {'limit': 0}, {'x': 7}]},
               {'default': 28,
                'records': [{'limit': 8}, {}, {'limit': None}, {'limit': 0}, {'x': 8}]},
               {'default': 29,
                'records': [{'limit': 9}, {}, {'limit': None}, {'limit': 0}, {'x': 9}]},
               {'default': 30,
                'records': [{'limit': 10}, {}, {'limit': None}, {'limit': 0}, {'x': 10}]},
               {'default': 31,
                'records': [{'limit': 11}, {}, {'limit': None}, {'limit': 0}, {'x': 11}]}],
 'mutations': [{'name': 'replaces explicit zero with default',
                'old': 'limits.append(value)',
                'new': "limits.append(value or data['default'])"}],
 'sources': ['https://docs.python.org/3/library/stdtypes.html#mapping-types-dict']}
