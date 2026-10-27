"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 5,
 'slug': 'counter-reconciliation',
 'title': 'Reconcile repeated item IDs',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Lists, dictionaries, and functions.',
 'learn': 'A set records whether an item is present. It does not record how many times the item '
          'occurs. Counter stores a count for each key and acts as a multiset. In a reconciliation '
          'task, repeated IDs can represent separate units. Counter subtraction keeps only '
          'positive counts. Therefore expected minus observed gives missing units, and observed '
          'minus expected gives extra units. Neither result includes zero or negative counts. Keep '
          'the input meaning separate from output order. Sorting the result keys makes the report '
          'deterministic even when two batches list their units in different orders. The output '
          'should preserve counts, not expand each count into repeated rows.',
 'task': ('**Input:** `data` has:\n'
    '- `expected`: a list of item IDs (ASCII strings).\n'
    '- `observed`: a list of item IDs (ASCII strings).\n'
    '\n'
    'A repeated ID counts as a separate unit each time.\n'
    '\n'
    '**Rules:** for each ID:\n'
    '- missing count = max(count in `expected` − count in `observed`, 0)\n'
    '- extra count = max(count in `observed` − count in `expected`, 0)\n'
    '\n'
    '**Return** `{"missing": [...], "extra": [...]}`\n'
    '- Each list contains `{"id": string, "count": int}` for each ID whose count is above 0. Do not include zero counts.\n'
    '- Sort each list by ID in ascending ASCII order.'),
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['Build one Counter per batch.',
           'Subtract in both directions, then sort the positive result keys.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'from collections import Counter\n'
              '\n'
              'def solve(data: dict) -> dict:\n'
              "    expected = Counter(data['expected'])\n"
              "    observed = Counter(data['observed'])\n"
              '    def rows(counts):\n'
              "        return [{'id': key, 'count': counts[key]} for key in sorted(counts)]\n"
              "    return {'missing': rows(expected - observed), 'extra': rows(observed - "
              'expected)}\n',
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    Map<String,Integer> counts=new TreeMap<>();\n'
         '    for(Object x:arr(d.get("expected"))) counts.merge(s(x),1,Integer::sum);\n'
         '    for(Object x:arr(d.get("observed"))) counts.merge(s(x),-1,Integer::sum);\n'
         '    List<Object> missing=new ArrayList<>(),extra=new ArrayList<>();\n'
         '    for(Map.Entry<String,Integer> e:counts.entrySet()) { int v=e.getValue(); if(v>0) '
         'missing.add(map("id",e.getKey(),"count",v)); if(v<0) '
         'extra.add(map("id",e.getKey(),"count",-v)); }\n'
         '    return map("missing",missing,"extra",extra);\n'
         '}',
 'approach': 'Counter subtraction implements positive multiset differences. Sorting only the '
             'distinct changed IDs gives O(n + k log k) time and O(k) space, where n is the total '
             'input size and k is the number of distinct IDs. The judge checks counts and order. '
             'It cannot prove Counter use. Production reconciliation also needs a clear source '
             'snapshot.',
 'cases': [{'input': {'expected': ['A', 'A', 'B'], 'observed': ['A', 'C']},
            'expected': {'missing': [{'id': 'A', 'count': 1}, {'id': 'B', 'count': 1}],
                         'extra': [{'id': 'C', 'count': 1}]},
            'label': 'counts in both directions'},
           {'input': {'expected': ['B', 'A'], 'observed': ['A', 'B']},
            'expected': {'missing': [], 'extra': []},
            'label': 'order does not matter'},
           {'input': {'expected': [], 'observed': []},
            'expected': {'missing': [], 'extra': []},
            'label': 'empty batches'},
           {'input': {'expected': ['x'], 'observed': []},
            'expected': {'missing': [{'id': 'x', 'count': 1}], 'extra': []},
            'label': 'only missing'},
           {'input': {'expected': [], 'observed': ['x', 'x']},
            'expected': {'missing': [], 'extra': [{'id': 'x', 'count': 2}]},
            'label': 'only extra'},
           {'input': {'expected': ['x', 'x', 'x'], 'observed': ['x']},
            'expected': {'missing': [{'id': 'x', 'count': 2}], 'extra': []},
            'label': 'set comparison loses units'},
           {'input': {'expected': ['x'], 'observed': ['x', 'x', 'x']},
            'expected': {'missing': [], 'extra': [{'id': 'x', 'count': 2}]},
            'label': 'extra duplicates'},
           {'input': {'expected': ['b', 'A', 'a'], 'observed': []},
            'expected': {'missing': [{'id': 'A', 'count': 1},
                                     {'id': 'a', 'count': 1},
                                     {'id': 'b', 'count': 1}],
                         'extra': []},
            'label': 'ASCII order'},
           {'input': {'expected': [''], 'observed': ['']},
            'expected': {'missing': [], 'extra': []},
            'label': 'empty ID'},
           {'input': {'expected': ['a', 'a', 'b'], 'observed': ['b', 'a', 'a']},
            'expected': {'missing': [], 'extra': []},
            'label': 'equal multiplicities'},
           {'input': {'expected': ['z', 'z'], 'observed': ['a', 'a']},
            'expected': {'missing': [{'id': 'z', 'count': 2}], 'extra': [{'id': 'a', 'count': 2}]},
            'label': 'disjoint batches'},
           {'input': {'expected': ['2', '10', '2'], 'observed': ['10', '3']},
            'expected': {'missing': [{'id': '2', 'count': 2}], 'extra': [{'id': '3', 'count': 1}]},
            'label': 'numeric-looking string IDs'}],
 'generated': [{'expected': ['A', 'C'], 'observed': ['B', 'B']},
               {'expected': ['A', 'A', 'B', 'C'], 'observed': ['A', 'B', 'B', 'D']},
               {'expected': ['A', 'A', 'A', 'B', 'B', 'C'], 'observed': ['A', 'A', 'B', 'B']},
               {'expected': ['A', 'A', 'A', 'A', 'C'], 'observed': ['A', 'A', 'A', 'B', 'B', 'D']},
               {'expected': ['A', 'A', 'A', 'A', 'A', 'B', 'C'], 'observed': ['B', 'B']},
               {'expected': ['A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C'],
                'observed': ['A', 'B', 'B', 'D']},
               {'expected': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'C'],
                'observed': ['A', 'A', 'B', 'B']},
               {'expected': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'C'],
                'observed': ['A', 'A', 'A', 'B', 'B', 'D']},
               {'expected': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C'],
                'observed': ['B', 'B']},
               {'expected': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'C'],
                'observed': ['A', 'B', 'B', 'D']},
               {'expected': ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'C'],
                'observed': ['A', 'A', 'B', 'B']},
               {'expected': ['A',
                             'A',
                             'A',
                             'A',
                             'A',
                             'A',
                             'A',
                             'A',
                             'A',
                             'A',
                             'A',
                             'A',
                             'B',
                             'B',
                             'C'],
                'observed': ['A', 'A', 'A', 'B', 'B', 'D']}],
 'mutations': [{'name': 'collapses expected duplicates',
                'old': "Counter(data['expected'])",
                'new': "Counter(set(data['expected']))"}],
 'sources': ['https://docs.python.org/3/library/collections.html#collections.Counter']}
