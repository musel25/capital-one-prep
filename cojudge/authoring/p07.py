"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 7,
 'slug': 'typed-json-boundary',
 'title': 'Validate JSON before using TypedDict',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Lists, dictionaries, and functions.',
 'learn': 'TypedDict describes the expected keys and value types in a dictionary for a static type '
          'checker. It does not validate a decoded JSON value at runtime. A value from json.loads '
          'can still be a list, a number, or an object with missing fields. Put a validator at the '
          'boundary. Check the outer type before you read keys. Check each required field and then '
          'build a small accepted object. That object can have a TypedDict return annotation '
          'because the function has established its shape. Extra fields need a stated policy. This '
          'task ignores them and returns only the validated fields.',
 'scenario': ('A partner bank sends payment records to your API as JSON. Some records are broken: wrong types, missing fields, or not objects at all. `solve` is the boundary check. It keeps the clean records (only `id` and `amount`) and reports the positions of the rejected ones, so the partner can send them again.'),
 'example_notes': ['Record 0 is valid (an amount of 0 is allowed). Record 1 has the amount `true`. Record 2 has no amount.', 'The extra `debug` key is not copied to the output.', 'An empty list.'],
 'task': ('**Input:** `data` has:\n'
    '- `records`: a list of any JSON values.\n'
    '\n'
    '**Rules:** accept a record only if all of these are true:\n'
    '- It is an object.\n'
    '- It has `id`, a nonempty string.\n'
    '- It has `amount`, a nonnegative integer. Booleans and floats are not integers for this rule. Integers have absolute value at most 1,000,000.\n'
    '\n'
    'Extra keys do not cause a rejection.\n'
    '\n'
    '**Return** `{"valid": [...], "rejected": [...]}`\n'
    '- `valid`: one `{"id": string, "amount": int}` per accepted record, in input order. Keep only these two fields.\n'
    '- `rejected`: the zero-based positions of the rejected records, in input order.\n'
    '\n'
    '**Practice:** use `TypedDict` in your solution. The judge checks only the output.'),
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['TypedDict does not replace runtime checks.',
           'Return a newly constructed Entry only after all checks pass.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'from typing import TypedDict\n'
              '\n'
              'class Entry(TypedDict):\n'
              '    id: str\n'
              '    amount: int\n'
              '\n'
              'def validate(value: object) -> Entry | None:\n'
              '    if not isinstance(value, dict):\n'
              '        return None\n'
              "    identifier = value.get('id')\n"
              "    amount = value.get('amount')\n"
              '    if not isinstance(identifier, str) or not identifier:\n'
              '        return None\n'
              '    if type(amount) is not int or amount < 0:\n'
              '        return None\n'
              "    return {'id': identifier, 'amount': amount}\n"
              '\n'
              'def solve(data: dict) -> dict:\n'
              '    valid: list[Entry] = []\n'
              '    rejected: list[int] = []\n'
              "    for index, value in enumerate(data['records']):\n"
              '        entry = validate(value)\n'
              '        if entry is None:\n'
              '            rejected.append(index)\n'
              '        else:\n'
              '            valid.append(entry)\n'
              "    return {'valid': valid, 'rejected': rejected}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    List<Object> valid=new ArrayList<>(),rejected=new ArrayList<>(); List<Object> '
         'records=arr(d.get("records"));\n'
         '    for(int i=0;i<records.size();i++) { Object x=records.get(i); boolean ok=false;\n'
         '        if(x instanceof Map) { Map<String,Object> r=obj(x); Object '
         'id=r.get("id"),a=r.get("amount");\n'
         '            ok=id instanceof String && !s(id).isEmpty() && isInteger(a) && lng(a)>=0;\n'
         '            if(ok) valid.add(map("id",id,"amount",a));\n'
         '        }\n'
         '        if(!ok) rejected.add(i);\n'
         '    }\n'
         '    return map("valid",valid,"rejected",rejected);\n'
         '}',
 'approach': 'The reference processes the input in one pass. Time is O(n), and result storage is '
             'O(n). The output judge checks results. It cannot prove the requested Python '
             'technique. This is an in-memory exercise; it does not provide storage or concurrency '
             'control.',
 'cases': [{'input': {'records': [{'id': 'A', 'amount': 0},
                                  {'id': 'B', 'amount': True},
                                  {'id': 'C'}]},
            'expected': {'valid': [{'id': 'A', 'amount': 0}], 'rejected': [1, 2]},
            'label': 'validate fields at the boundary'},
           {'input': {'records': [{'id': 'X', 'amount': 4, 'debug': True}]},
            'expected': {'valid': [{'id': 'X', 'amount': 4}], 'rejected': []},
            'label': 'drop extra fields'},
           {'input': {'records': []},
            'expected': {'valid': [], 'rejected': []},
            'label': 'empty list'},
           {'input': {'records': [None, [], 4, 'text', False]},
            'expected': {'valid': [], 'rejected': [0, 1, 2, 3, 4]},
            'label': 'wrong record types'},
           {'input': {'records': [{}]},
            'expected': {'valid': [], 'rejected': [0]},
            'label': 'both keys missing'},
           {'input': {'records': [{'id': '', 'amount': 1}]},
            'expected': {'valid': [], 'rejected': [0]},
            'label': 'empty ID'},
           {'input': {'records': [{'id': 0, 'amount': 1}, {'id': None, 'amount': 1}]},
            'expected': {'valid': [], 'rejected': [0, 1]},
            'label': 'wrong ID types'},
           {'input': {'records': [{'id': 'A', 'amount': -1}]},
            'expected': {'valid': [], 'rejected': [0]},
            'label': 'negative amount'},
           {'input': {'records': [{'id': 'A', 'amount': 1.0}, {'id': 'B', 'amount': '1'}]},
            'expected': {'valid': [], 'rejected': [0, 1]},
            'label': 'no numeric coercion'},
           {'input': {'records': [{'id': 'A', 'amount': None}, {'id': 'B', 'amount': False}]},
            'expected': {'valid': [], 'rejected': [0, 1]},
            'label': 'null and false'},
           {'input': {'records': [{'id': 'A', 'amount': 1000000}, {'id': 'A', 'amount': 2}]},
            'expected': {'valid': [{'id': 'A', 'amount': 1000000}, {'id': 'A', 'amount': 2}],
                         'rejected': []},
            'label': 'duplicate ID is permitted'},
           {'input': {'records': [{'id': ' ', 'amount': 3}, {'id': 'é', 'amount': 1}]},
            'expected': {'valid': [{'id': ' ', 'amount': 3}, {'id': 'é', 'amount': 1}],
                         'rejected': []},
            'label': 'nonempty is the only ID text rule'},
           {'input': {'records': [{'amount': 0}, {'id': 'ok', 'amount': 2}, None]},
            'expected': {'valid': [{'id': 'ok', 'amount': 2}], 'rejected': [0, 2]},
            'label': 'accepted position in middle'}],
 'generated': [{'records': [{'id': 'id0', 'amount': 0},
                            {'id': 'bad0', 'amount': False},
                            {'id': '', 'amount': 0},
                            {'id': 'end0', 'amount': 9, 'extra': [0]}]},
               {'records': [{'id': 'id1', 'amount': 1},
                            {'id': 'bad1', 'amount': False},
                            {'id': '', 'amount': 1},
                            {'id': 'end1', 'amount': 10, 'extra': [1]}]},
               {'records': [{'id': 'id2', 'amount': 2},
                            {'id': 'bad2', 'amount': False},
                            {'id': '', 'amount': 2},
                            {'id': 'end2', 'amount': 11, 'extra': [2]}]},
               {'records': [{'id': 'id3', 'amount': 3},
                            {'id': 'bad3', 'amount': False},
                            {'id': '', 'amount': 3},
                            {'id': 'end3', 'amount': 12, 'extra': [3]}]},
               {'records': [{'id': 'id4', 'amount': 4},
                            {'id': 'bad4', 'amount': False},
                            {'id': '', 'amount': 4},
                            {'id': 'end4', 'amount': 13, 'extra': [4]}]},
               {'records': [{'id': 'id5', 'amount': 5},
                            {'id': 'bad5', 'amount': False},
                            {'id': '', 'amount': 5},
                            {'id': 'end5', 'amount': 14, 'extra': [5]}]},
               {'records': [{'id': 'id6', 'amount': 6},
                            {'id': 'bad6', 'amount': False},
                            {'id': '', 'amount': 6},
                            {'id': 'end6', 'amount': 15, 'extra': [6]}]},
               {'records': [{'id': 'id7', 'amount': 7},
                            {'id': 'bad7', 'amount': False},
                            {'id': '', 'amount': 7},
                            {'id': 'end7', 'amount': 16, 'extra': [7]}]},
               {'records': [{'id': 'id8', 'amount': 8},
                            {'id': 'bad8', 'amount': False},
                            {'id': '', 'amount': 8},
                            {'id': 'end8', 'amount': 17, 'extra': [8]}]},
               {'records': [{'id': 'id9', 'amount': 9},
                            {'id': 'bad9', 'amount': False},
                            {'id': '', 'amount': 9},
                            {'id': 'end9', 'amount': 18, 'extra': [9]}]},
               {'records': [{'id': 'id10', 'amount': 10},
                            {'id': 'bad10', 'amount': False},
                            {'id': '', 'amount': 10},
                            {'id': 'end10', 'amount': 19, 'extra': [10]}]},
               {'records': [{'id': 'id11', 'amount': 11},
                            {'id': 'bad11', 'amount': False},
                            {'id': '', 'amount': 11},
                            {'id': 'end11', 'amount': 20, 'extra': [11]}]}],
 'mutations': [{'name': 'accepts bool as integer',
                'old': 'type(amount) is not int',
                'new': 'not isinstance(amount, int)'}],
 'sources': ['https://docs.python.org/3.11/library/typing.html#typing.TypedDict']}
