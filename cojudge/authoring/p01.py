"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 1,
 'slug': 'strict-numeric-fields',
 'title': 'Strict numeric fields',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Lists, dictionaries, and functions.',
 'learn': 'Python treats bool as a subclass of int. As a result, isinstance(True, int) returns '
          'True. This can turn a flag into one cent when you validate a numeric field. At a JSON '
          'boundary, decide which exact types the contract permits. Use type(value) is int when a '
          'field requires an integer and must exclude booleans. Validate the range in a separate '
          'condition. Do not convert strings or round floats unless the contract requires it. Keep '
          'rejected positions so a caller can identify each bad field. Zero is a valid amount in '
          'this task. An empty batch has a total of zero.',
 'task': '`data` has `values`, a list of JSON values. Accept a value only when its exact Python '
         'type is `int` and it is at least zero. JSON integers have absolute value at most '
         '1,000,000,000. Reject booleans, floats, strings, null, lists, objects, and negative '
         'integers. Return `{"total": sum_of_accepted_values, "rejected": '
         '[zero_based_positions]}`. Keep rejected positions in input order.',
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['Check the exact type before the range.', 'Use enumerate to record rejected positions.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'def solve(data: dict) -> dict:\n'
              '    total = 0\n'
              '    rejected = []\n'
              "    for index, value in enumerate(data['values']):\n"
              '        if type(value) is int and value >= 0:\n'
              '            total += value\n'
              '        else:\n'
              '            rejected.append(index)\n'
              "    return {'total': total, 'rejected': rejected}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    long total=0; List<Object> rejected=new ArrayList<>(); List<Object> '
         'values=arr(d.get("values"));\n'
         '    for(int i=0;i<values.size();i++) {\n'
         '        Object x=values.get(i);\n'
         '        boolean integer=isInteger(x);\n'
         '        if(integer && lng(x)>=0) total+=lng(x); else rejected.add(i);\n'
         '    }\n'
         '    return map("total",total,"rejected",rejected);\n'
         '}',
 'approach': 'The reference processes the input in one pass. Time is O(n), and result storage is '
             'O(n). The output judge checks results. It cannot prove the requested Python '
             'technique. This is an in-memory exercise; it does not provide storage or concurrency '
             'control.',
 'cases': [{'input': {'values': [7, True, 0, -2, '4']},
            'expected': {'total': 7, 'rejected': [1, 3, 4]},
            'label': 'flags and text are not amounts'},
           {'input': {'values': [2, 3, 5]},
            'expected': {'total': 10, 'rejected': []},
            'label': 'all amounts are valid'},
           {'input': {'values': []},
            'expected': {'total': 0, 'rejected': []},
            'label': 'empty batch'},
           {'input': {'values': [0]},
            'expected': {'total': 0, 'rejected': []},
            'label': 'zero is valid'},
           {'input': {'values': [False]},
            'expected': {'total': 0, 'rejected': [0]},
            'label': 'false is not zero'},
           {'input': {'values': [1.0]},
            'expected': {'total': 0, 'rejected': [0]},
            'label': 'integral float is still a float'},
           {'input': {'values': [None]},
            'expected': {'total': 0, 'rejected': [0]},
            'label': 'null is rejected'},
           {'input': {'values': [[], {}]},
            'expected': {'total': 0, 'rejected': [0, 1]},
            'label': 'containers are rejected'},
           {'input': {'values': [-1, -100]},
            'expected': {'total': 0, 'rejected': [0, 1]},
            'label': 'negative values'},
           {'input': {'values': [1000000000, 1000000000]},
            'expected': {'total': 2000000000, 'rejected': []},
            'label': 'large total'},
           {'input': {'values': [3, 3, 3]},
            'expected': {'total': 9, 'rejected': []},
            'label': 'repeated amounts count'},
           {'input': {'values': ['0', '', 0.5, 2]},
            'expected': {'total': 2, 'rejected': [0, 1, 2]},
            'label': 'no coercion'},
           {'input': {'values': [True, 1, False, 0]},
            'expected': {'total': 1, 'rejected': [0, 2]},
            'label': 'type boundaries'}],
 'generated': [{'values': [0, False, -1, '0', 0, None]},
               {'values': [1, False, -2, '1', 1, None]},
               {'values': [2, False, -3, '2', 4, None]},
               {'values': [3, False, -4, '3', 9, None]},
               {'values': [4, False, -5, '4', 16, None]},
               {'values': [5, False, -6, '5', 25, None]},
               {'values': [6, False, -7, '6', 36, None]},
               {'values': [7, False, -8, '7', 49, None]},
               {'values': [8, False, -9, '8', 64, None]},
               {'values': [9, False, -10, '9', 81, None]},
               {'values': [10, False, -11, '10', 100, None]},
               {'values': [11, False, -12, '11', 121, None]}],
 'mutations': [{'name': 'accepts booleans',
                'old': 'type(value) is int',
                'new': 'isinstance(value, int)'}],
 'sources': ['https://docs.python.org/3/library/stdtypes.html#boolean-type-bool']}
