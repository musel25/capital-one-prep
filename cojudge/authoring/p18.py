"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 18,
 'slug': 'event-id-conflicts',
 'title': 'Separate duplicate events from conflicts',
 'difficulty': 'Medium',
 'time': 25,
 'prerequisites': 'Dictionaries, event processing, and signed integer arithmetic.',
 'learn': 'An event ID can make a retried operation safe to handle more than once. Store the '
          'payload associated with the first use of that ID. If a later event has the same ID and '
          'the same payload, it is a duplicate and must not apply again. If it has a different '
          'payload, it is a conflict. Ignoring that distinction can hide a caller bug or apply an '
          'unintended change. Do not replace the stored payload when a conflict arrives. The first '
          'event remains the reference for later comparisons. This task uses a single signed delta '
          'as the payload, so equality has one clear meaning.',
 'scenario': ('A ledger receives balance events from a message queue. The queue can deliver the same event twice. The same ID with the same delta is a harmless duplicate. The same ID with a different delta is a data conflict that needs a person to look at it. Each event ID is applied at most once.'),
 'example_notes': ['`e1` is applied once (+5). The same `e1` again is a duplicate. `e1` with 7 is a conflict.', '`x` with 3 is a conflict. `x` with 2 again matches the first event, so it is a duplicate.', 'No events.'],
 'task': ('**Input:** `data` has:\n'
    '- `balance`: the integer starting total.\n'
    '- `events`: a list of `{"id": string, "delta": int}`.\n'
    '\n'
    'Totals and deltas can be negative.\n'
    '\n'
    '**Rules:** for each event, in order:\n'
    '- First time an ID appears: add its `delta` to the total. Status `applied`.\n'
    '- ID seen before, with the same `delta` as its first event: status `duplicate`.\n'
    '- ID seen before, with a different `delta`: status `conflict`.\n'
    '- `duplicate` and `conflict` do not change the total or the stored first delta.\n'
    '\n'
    '**Return** `{"status": [string], "balance": int}`: the statuses in event order, and the final total.'),
 'constraints': ['At most 100 events. Initial total and deltas have absolute value at most '
                 '1,000,000,000,000.'],
 'hints': ['Remember the first delta for each ID.',
           'A repeated ID needs a payload comparison before you choose its status.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'def solve(data: dict) -> dict:\n'
              "    balance = data['balance']\n"
              '    seen: dict[str, int] = {}\n'
              '    status = []\n'
              "    for event in data['events']:\n"
              "        event_id, delta = event['id'], event['delta']\n"
              '        if event_id not in seen:\n'
              '            seen[event_id] = delta\n'
              '            balance += delta\n'
              "            status.append('applied')\n"
              '        elif seen[event_id] == delta:\n'
              "            status.append('duplicate')\n"
              '        else:\n'
              "            status.append('conflict')\n"
              "    return {'status': status, 'balance': balance}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    long balance=lng(d.get("balance")); Map<String,Long> seen=new '
         'HashMap<>();List<Object> status=new ArrayList<>();\n'
         '    for(Object x:arr(d.get("events"))) {Map<String,Object> e=obj(x);String '
         'id=s(e.get("id"));long delta=lng(e.get("delta"));\n'
         '        '
         'if(!seen.containsKey(id)){seen.put(id,delta);balance+=delta;status.add("applied");}\n'
         '        else status.add(seen.get(id)==delta?"duplicate":"conflict");\n'
         '    }\n'
         '    return map("status",status,"balance",balance);\n'
         '}',
 'approach': 'The reference stores one original delta per event ID. Expected time is O(n), and '
             'memory is O(k + n) for k IDs and n status results. Tests distinguish conflicts from '
             'duplicates and check that conflicts do not rewrite history. A production event store '
             'needs a durable, atomic deduplication record; this exercise has neither persistence '
             'nor concurrency.',
 'cases': [{'input': {'balance': 10,
                      'events': [{'id': 'e1', 'delta': 5},
                                 {'id': 'e1', 'delta': 5},
                                 {'id': 'e1', 'delta': 7}]},
            'expected': {'status': ['applied', 'duplicate', 'conflict'], 'balance': 15},
            'label': 'new, duplicate, and conflicting payload'},
           {'input': {'balance': 0,
                      'events': [{'id': 'x', 'delta': 2},
                                 {'id': 'x', 'delta': 3},
                                 {'id': 'x', 'delta': 2}]},
            'expected': {'status': ['applied', 'conflict', 'duplicate'], 'balance': 2},
            'label': 'conflict does not replace the first payload'},
           {'input': {'balance': 8, 'events': []},
            'expected': {'status': [], 'balance': 8},
            'label': 'no events'},
           {'input': {'balance': 0, 'events': [{'id': 'z', 'delta': 0}, {'id': 'z', 'delta': 0}]},
            'expected': {'status': ['applied', 'duplicate'], 'balance': 0},
            'label': 'zero delta is still recorded'},
           {'input': {'balance': 0, 'events': [{'id': 'a', 'delta': 5}, {'id': 'b', 'delta': 5}]},
            'expected': {'status': ['applied', 'applied'], 'balance': 10},
            'label': 'same payload under different IDs'},
           {'input': {'balance': 3, 'events': [{'id': 'a', 'delta': -5}]},
            'expected': {'status': ['applied'], 'balance': -2},
            'label': 'signed totals allowed'},
           {'input': {'balance': 0, 'events': [{'id': 'a', 'delta': 1}, {'id': 'a', 'delta': -1}]},
            'expected': {'status': ['applied', 'conflict'], 'balance': 1},
            'label': 'sign change is a conflict'},
           {'input': {'balance': 0, 'events': [{'id': '', 'delta': 2}, {'id': '', 'delta': 2}]},
            'expected': {'status': ['applied', 'duplicate'], 'balance': 2},
            'label': 'empty ID is a valid key'},
           {'input': {'balance': 0,
                      'events': [{'id': 'a', 'delta': 1},
                                 {'id': 'b', 'delta': -1},
                                 {'id': 'a', 'delta': 1},
                                 {'id': 'b', 'delta': -1}]},
            'expected': {'status': ['applied', 'applied', 'duplicate', 'duplicate'], 'balance': 0},
            'label': 'interleaved retries'},
           {'input': {'balance': 0,
                      'events': [{'id': 'a', 'delta': 0},
                                 {'id': 'a', 'delta': 1},
                                 {'id': 'a', 'delta': 1}]},
            'expected': {'status': ['applied', 'conflict', 'conflict'], 'balance': 0},
            'label': 'repeated conflict remains a conflict'},
           {'input': {'balance': 1000000000000,
                      'events': [{'id': 'a', 'delta': 1000000000000},
                                 {'id': 'a', 'delta': 1000000000000}]},
            'expected': {'status': ['applied', 'duplicate'], 'balance': 2000000000000},
            'label': 'large exact delta'},
           {'input': {'balance': -5, 'events': [{'id': 'A', 'delta': 2}, {'id': 'a', 'delta': 3}]},
            'expected': {'status': ['applied', 'applied'], 'balance': 0},
            'label': 'case-sensitive IDs'}],
 'generated': [{'balance': 0,
                'events': [{'id': 'x0', 'delta': 1},
                           {'id': 'y0', 'delta': 0},
                           {'id': 'x0', 'delta': 1},
                           {'id': 'x0', 'delta': 2},
                           {'id': 'x0', 'delta': 1}]},
               {'balance': 1,
                'events': [{'id': 'x1', 'delta': 2},
                           {'id': 'y1', 'delta': -1},
                           {'id': 'x1', 'delta': 2},
                           {'id': 'x1', 'delta': 3},
                           {'id': 'x1', 'delta': 2}]},
               {'balance': 2,
                'events': [{'id': 'x2', 'delta': 3},
                           {'id': 'y2', 'delta': -2},
                           {'id': 'x2', 'delta': 3},
                           {'id': 'x2', 'delta': 4},
                           {'id': 'x2', 'delta': 3}]},
               {'balance': 3,
                'events': [{'id': 'x3', 'delta': 4},
                           {'id': 'y3', 'delta': -3},
                           {'id': 'x3', 'delta': 4},
                           {'id': 'x3', 'delta': 5},
                           {'id': 'x3', 'delta': 4}]},
               {'balance': 4,
                'events': [{'id': 'x4', 'delta': 5},
                           {'id': 'y4', 'delta': -4},
                           {'id': 'x4', 'delta': 5},
                           {'id': 'x4', 'delta': 6},
                           {'id': 'x4', 'delta': 5}]},
               {'balance': 5,
                'events': [{'id': 'x5', 'delta': 6},
                           {'id': 'y5', 'delta': -5},
                           {'id': 'x5', 'delta': 6},
                           {'id': 'x5', 'delta': 7},
                           {'id': 'x5', 'delta': 6}]},
               {'balance': 6,
                'events': [{'id': 'x6', 'delta': 7},
                           {'id': 'y6', 'delta': -6},
                           {'id': 'x6', 'delta': 7},
                           {'id': 'x6', 'delta': 8},
                           {'id': 'x6', 'delta': 7}]},
               {'balance': 7,
                'events': [{'id': 'x7', 'delta': 8},
                           {'id': 'y7', 'delta': -7},
                           {'id': 'x7', 'delta': 8},
                           {'id': 'x7', 'delta': 9},
                           {'id': 'x7', 'delta': 8}]},
               {'balance': 8,
                'events': [{'id': 'x8', 'delta': 9},
                           {'id': 'y8', 'delta': -8},
                           {'id': 'x8', 'delta': 9},
                           {'id': 'x8', 'delta': 10},
                           {'id': 'x8', 'delta': 9}]},
               {'balance': 9,
                'events': [{'id': 'x9', 'delta': 10},
                           {'id': 'y9', 'delta': -9},
                           {'id': 'x9', 'delta': 10},
                           {'id': 'x9', 'delta': 11},
                           {'id': 'x9', 'delta': 10}]},
               {'balance': 10,
                'events': [{'id': 'x10', 'delta': 11},
                           {'id': 'y10', 'delta': -10},
                           {'id': 'x10', 'delta': 11},
                           {'id': 'x10', 'delta': 12},
                           {'id': 'x10', 'delta': 11}]},
               {'balance': 11,
                'events': [{'id': 'x11', 'delta': 12},
                           {'id': 'y11', 'delta': -11},
                           {'id': 'x11', 'delta': 12},
                           {'id': 'x11', 'delta': 13},
                           {'id': 'x11', 'delta': 12}]}],
 'mutations': [{'name': 'treats every repeated ID as an exact duplicate',
                'old': 'elif seen[event_id] == delta:',
                'new': 'elif event_id in seen:'}],
 'sources': ['https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict']}
