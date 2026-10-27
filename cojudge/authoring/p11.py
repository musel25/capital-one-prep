"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 11,
 'slug': 'dataclass-list-isolation',
 'title': 'Fix shared dataclass items',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Classes, lists, and the first ten exercises.',
 'learn': 'A dataclass can generate an initializer from annotated fields. A mutable field still '
          'needs a separate value for each instance. Use field(default_factory=list) to call list '
          'each time an instance is created. A factory must create a new value. A factory that '
          'returns one existing list still shares that list across instances. Then adding an item '
          'to one object changes another object. Dataclasses reject some direct mutable defaults, '
          'but a factory can hide the same defect. This task supplies a runnable faulty starter. '
          'Repair the shared state while keeping the dataclass model. The result for every box '
          'must depend only on actions addressed to that box.',
 'task': ('**Bug fix.** The dataclass in the starter has a field factory that returns one shared list. Fix that defect.\n'
    '\n'
    '**Input:** `data` has:\n'
    '- `names`: distinct strings, one per box, in box order.\n'
    '- `actions`: a list of `{"box": int, "item": string}`. `box` is a valid zero-based box index.\n'
    '\n'
    'If `names` is empty, `actions` is empty too.\n'
    '\n'
    '**Rules**\n'
    '- Create one empty box per name.\n'
    '- For each action, in order, append `item` to the selected box.\n'
    '\n'
    '**Return** a list of `{"name": string, "items": [string]}`, one per box, in `names` order. Keep item order and duplicates.\n'
    '\n'
    'The judge checks that the boxes are isolated. It does not check the dataclass syntax.'),
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['A default factory runs once per new instance.',
           'Check whether the factory creates a list or returns an existing list.'],
 'starter': 'from dataclasses import dataclass, field\n'
            '\n'
            '@dataclass\n'
            'class Box:\n'
            '    name: str\n'
            '    items: list[str] = field(default_factory=lambda items=[]: items)\n'
            '\n'
            'def solve(data: dict) -> list[dict]:\n'
            "    boxes = [Box(name) for name in data['names']]\n"
            "    for action in data['actions']:\n"
            "        boxes[action['box']].items.append(action['item'])\n"
            "    return [{'name': box.name, 'items': box.items} for box in boxes]\n",
 'reference': 'from dataclasses import dataclass, field\n'
              '\n'
              '@dataclass\n'
              'class Box:\n'
              '    name: str\n'
              '    items: list[str] = field(default_factory=list)\n'
              '\n'
              'def solve(data: dict) -> list[dict]:\n'
              "    boxes = [Box(name) for name in data['names']]\n"
              "    for action in data['actions']:\n"
              "        boxes[action['box']].items.append(action['item'])\n"
              "    return [{'name': box.name, 'items': box.items} for box in boxes]\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    List<Object> names=arr(d.get("names")); List<List<Object>> items=new ArrayList<>();\n'
         '    for(Object name:names) items.add(new ArrayList<>());\n'
         '    for(Object x:arr(d.get("actions"))) { Map<String,Object> a=obj(x); '
         'items.get(n(a.get("box"))).add(a.get("item")); }\n'
         '    List<Object> out=new ArrayList<>(); for(int i=0;i<names.size();i++) '
         'out.add(map("name",names.get(i),"items",items.get(i))); return out;\n'
         '}',
 'approach': 'The reference processes the input in one pass. Time is O(n), and result storage is '
             'O(n). The output judge checks results. It cannot prove the requested Python '
             'technique. This is an in-memory exercise; it does not provide storage or concurrency '
             'control.',
 'cases': [{'input': {'names': ['A', 'B'], 'actions': [{'box': 0, 'item': 'pen'}]},
            'expected': [{'name': 'A', 'items': ['pen']}, {'name': 'B', 'items': []}],
            'label': 'one box must not change another'},
           {'input': {'names': ['A', 'B'],
                      'actions': [{'box': 1, 'item': 'book'},
                                  {'box': 0, 'item': 'pen'},
                                  {'box': 1, 'item': 'paper'}]},
            'expected': [{'name': 'A', 'items': ['pen']},
                         {'name': 'B', 'items': ['book', 'paper']}],
            'label': 'independent item order'},
           {'input': {'names': [], 'actions': []}, 'expected': [], 'label': 'no boxes'},
           {'input': {'names': ['A'], 'actions': []},
            'expected': [{'name': 'A', 'items': []}],
            'label': 'empty single box'},
           {'input': {'names': ['A', 'B', 'C'], 'actions': []},
            'expected': [{'name': 'A', 'items': []},
                         {'name': 'B', 'items': []},
                         {'name': 'C', 'items': []}],
            'label': 'several empty boxes'},
           {'input': {'names': ['A'],
                      'actions': [{'box': 0, 'item': 'x'}, {'box': 0, 'item': 'x'}]},
            'expected': [{'name': 'A', 'items': ['x', 'x']}],
            'label': 'duplicates are retained'},
           {'input': {'names': ['A', 'B', 'C'], 'actions': [{'box': 2, 'item': 'last'}]},
            'expected': [{'name': 'A', 'items': []},
                         {'name': 'B', 'items': []},
                         {'name': 'C', 'items': ['last']}],
            'label': 'last box index'},
           {'input': {'names': [''], 'actions': [{'box': 0, 'item': ''}]},
            'expected': [{'name': '', 'items': ['']}],
            'label': 'empty strings are values'},
           {'input': {'names': ['B', 'A'],
                      'actions': [{'box': 0, 'item': '1'}, {'box': 1, 'item': '2'}]},
            'expected': [{'name': 'B', 'items': ['1']}, {'name': 'A', 'items': ['2']}],
            'label': 'name order is preserved'},
           {'input': {'names': ['A', 'B'],
                      'actions': [{'box': 1, 'item': 'x'}, {'box': 1, 'item': 'y'}]},
            'expected': [{'name': 'A', 'items': []}, {'name': 'B', 'items': ['x', 'y']}],
            'label': 'first box remains empty'},
           {'input': {'names': ['A', 'B', 'C'],
                      'actions': [{'box': 0, 'item': 'x'},
                                  {'box': 1, 'item': 'x'},
                                  {'box': 2, 'item': 'x'}]},
            'expected': [{'name': 'A', 'items': ['x']},
                         {'name': 'B', 'items': ['x']},
                         {'name': 'C', 'items': ['x']}],
            'label': 'same item in separate boxes'},
           {'input': {'names': ['α', 'β'],
                      'actions': [{'box': 0, 'item': '雪'}, {'box': 1, 'item': '🚀'}]},
            'expected': [{'name': 'α', 'items': ['雪']}, {'name': 'β', 'items': ['🚀']}],
            'label': 'Unicode text'}],
 'generated': [{'names': ['A0', 'B0', 'C0'], 'actions': [{'box': 0, 'item': '0:0'}]},
               {'names': ['A1', 'B1', 'C1'],
                'actions': [{'box': 0, 'item': '1:0'}, {'box': 1, 'item': '1:1'}]},
               {'names': ['A2', 'B2', 'C2'],
                'actions': [{'box': 0, 'item': '2:0'},
                            {'box': 1, 'item': '2:1'},
                            {'box': 2, 'item': '2:2'}]},
               {'names': ['A3', 'B3', 'C3'],
                'actions': [{'box': 0, 'item': '3:0'},
                            {'box': 1, 'item': '3:1'},
                            {'box': 2, 'item': '3:2'},
                            {'box': 0, 'item': '3:3'}]},
               {'names': ['A4', 'B4', 'C4'],
                'actions': [{'box': 0, 'item': '4:0'},
                            {'box': 1, 'item': '4:1'},
                            {'box': 2, 'item': '4:2'},
                            {'box': 0, 'item': '4:3'},
                            {'box': 1, 'item': '4:4'}]},
               {'names': ['A5', 'B5', 'C5'],
                'actions': [{'box': 0, 'item': '5:0'},
                            {'box': 1, 'item': '5:1'},
                            {'box': 2, 'item': '5:2'},
                            {'box': 0, 'item': '5:3'},
                            {'box': 1, 'item': '5:4'},
                            {'box': 2, 'item': '5:5'}]},
               {'names': ['A6', 'B6', 'C6'],
                'actions': [{'box': 0, 'item': '6:0'},
                            {'box': 1, 'item': '6:1'},
                            {'box': 2, 'item': '6:2'},
                            {'box': 0, 'item': '6:3'},
                            {'box': 1, 'item': '6:4'},
                            {'box': 2, 'item': '6:5'},
                            {'box': 0, 'item': '6:6'}]},
               {'names': ['A7', 'B7', 'C7'],
                'actions': [{'box': 0, 'item': '7:0'},
                            {'box': 1, 'item': '7:1'},
                            {'box': 2, 'item': '7:2'},
                            {'box': 0, 'item': '7:3'},
                            {'box': 1, 'item': '7:4'},
                            {'box': 2, 'item': '7:5'},
                            {'box': 0, 'item': '7:6'},
                            {'box': 1, 'item': '7:7'}]},
               {'names': ['A8', 'B8', 'C8'],
                'actions': [{'box': 0, 'item': '8:0'},
                            {'box': 1, 'item': '8:1'},
                            {'box': 2, 'item': '8:2'},
                            {'box': 0, 'item': '8:3'},
                            {'box': 1, 'item': '8:4'},
                            {'box': 2, 'item': '8:5'},
                            {'box': 0, 'item': '8:6'},
                            {'box': 1, 'item': '8:7'},
                            {'box': 2, 'item': '8:8'}]},
               {'names': ['A9', 'B9', 'C9'],
                'actions': [{'box': 0, 'item': '9:0'},
                            {'box': 1, 'item': '9:1'},
                            {'box': 2, 'item': '9:2'},
                            {'box': 0, 'item': '9:3'},
                            {'box': 1, 'item': '9:4'},
                            {'box': 2, 'item': '9:5'},
                            {'box': 0, 'item': '9:6'},
                            {'box': 1, 'item': '9:7'},
                            {'box': 2, 'item': '9:8'},
                            {'box': 0, 'item': '9:9'}]},
               {'names': ['A10', 'B10', 'C10'],
                'actions': [{'box': 0, 'item': '10:0'},
                            {'box': 1, 'item': '10:1'},
                            {'box': 2, 'item': '10:2'},
                            {'box': 0, 'item': '10:3'},
                            {'box': 1, 'item': '10:4'},
                            {'box': 2, 'item': '10:5'},
                            {'box': 0, 'item': '10:6'},
                            {'box': 1, 'item': '10:7'},
                            {'box': 2, 'item': '10:8'},
                            {'box': 0, 'item': '10:9'},
                            {'box': 1, 'item': '10:10'}]},
               {'names': ['A11', 'B11', 'C11'],
                'actions': [{'box': 0, 'item': '11:0'},
                            {'box': 1, 'item': '11:1'},
                            {'box': 2, 'item': '11:2'},
                            {'box': 0, 'item': '11:3'},
                            {'box': 1, 'item': '11:4'},
                            {'box': 2, 'item': '11:5'},
                            {'box': 0, 'item': '11:6'},
                            {'box': 1, 'item': '11:7'},
                            {'box': 2, 'item': '11:8'},
                            {'box': 0, 'item': '11:9'},
                            {'box': 1, 'item': '11:10'},
                            {'box': 2, 'item': '11:11'}]}],
 'mutations': [{'name': 'factory returns shared list',
                'old': 'field(default_factory=list)',
                'new': 'field(default_factory=lambda items=[]: items)'}],
 'sources': ['https://docs.python.org/3.11/library/dataclasses.html#default-factory-functions']}
