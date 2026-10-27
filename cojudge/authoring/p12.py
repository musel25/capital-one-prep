"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 12,
 'slug': 'nested-copy-isolation',
 'title': 'Fix nested configuration copies',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Nested dictionaries, lists, and object references.',
 'learn': 'Assignment gives another name to the same object. A shallow copy creates a new outer '
          'container but keeps references to its nested containers. If you copy a dictionary and '
          'then change a nested list, both dictionaries can show that change. deepcopy recursively '
          'copies nested values so that each configuration can change independently. Copy only '
          'what the model requires; a deliberate copy of known nested fields can also work. This '
          'task uses small JSON-like dictionaries and lists, so deep copying has clear meaning. '
          'The starter copies only the outer dictionary. Repair it so each result starts from the '
          'original template, not from a previous result.',
 'task': ('**Bug fix.** The starter makes a shallow copy. Repair it.\n'
    '\n'
    '**Input:** `data` has:\n'
    '- `template`: `{"limits": {"daily": int, "monthly": int}, "tags": [string]}`. The limits are nonnegative integers.\n'
    '- `changes`: a list of objects. A change can contain `daily`, `monthly`, and `tag`. No other keys occur.\n'
    '\n'
    '**Rules:** for each change:\n'
    '1. Make an independent copy of the original template, not of an earlier copy.\n'
    '2. `daily` or `monthly`: replace that limit with the value.\n'
    '3. `tag`: append it to `tags`, even if it is an empty string or is already in the list.\n'
    '\n'
    '**Return** `{"template": ..., "copies": [...]}`\n'
    '- `template`: the original template, unchanged.\n'
    '- `copies`: the updated configurations, in change order.'),
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['Inspect the objects inside limits and tags.',
           'Each change starts from the original template.'],
 'starter': 'from copy import deepcopy\n'
            '\n'
            'def solve(data: dict) -> dict:\n'
            "    template = data['template']\n"
            '    copies = []\n'
            "    for change in data['changes']:\n"
            '        config = template.copy()\n'
            "        for key in ('daily', 'monthly'):\n"
            '            if key in change:\n'
            "                config['limits'][key] = change[key]\n"
            "        if 'tag' in change:\n"
            "            config['tags'].append(change['tag'])\n"
            '        copies.append(config)\n'
            "    return {'template': template, 'copies': copies}\n",
 'reference': 'from copy import deepcopy\n'
              '\n'
              'def solve(data: dict) -> dict:\n'
              "    template = data['template']\n"
              '    copies = []\n'
              "    for change in data['changes']:\n"
              '        config = deepcopy(template)\n'
              "        for key in ('daily', 'monthly'):\n"
              '            if key in change:\n'
              "                config['limits'][key] = change[key]\n"
              "        if 'tag' in change:\n"
              "            config['tags'].append(change['tag'])\n"
              '        copies.append(config)\n'
              "    return {'template': template, 'copies': copies}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    Map<String,Object> '
         'template=obj(d.get("template")),limits=obj(template.get("limits")); List<Object> out=new '
         'ArrayList<>();\n'
         '    for(Object x:arr(d.get("changes"))) { Map<String,Object> c=obj(x); List<Object> '
         'tags=new ArrayList<>(arr(template.get("tags"))); if(c.containsKey("tag")) '
         'tags.add(c.get("tag"));\n'
         '        '
         'out.add(map("limits",map("daily",c.containsKey("daily")?c.get("daily"):limits.get("daily"),"monthly",c.containsKey("monthly")?c.get("monthly"):limits.get("monthly")),"tags",tags));\n'
         '    }\n'
         '    return map("template",template,"copies",out);\n'
         '}',
 'approach': 'The reference uses deepcopy once per requested configuration. If the template has t '
             'values and there are n changes, time and result space are O(n t). Tests expose '
             'shared nested lists and dictionaries through the returned template and copies. The '
             'judge cannot prove copy strategy. Deep copying arbitrary application objects can '
             'need a different policy.',
 'cases': [{'input': {'template': {'limits': {'daily': 1, 'monthly': 10}, 'tags': ['base']},
                      'changes': [{'daily': 2}, {'tag': 'new'}]},
            'expected': {'template': {'limits': {'daily': 1, 'monthly': 10}, 'tags': ['base']},
                         'copies': [{'limits': {'daily': 2, 'monthly': 10}, 'tags': ['base']},
                                    {'limits': {'daily': 1, 'monthly': 10},
                                     'tags': ['base', 'new']}]},
            'label': 'copies and template stay independent'},
           {'input': {'template': {'limits': {'daily': 5, 'monthly': 50}, 'tags': []},
                      'changes': [{'daily': 0, 'monthly': 0, 'tag': 'x'}]},
            'expected': {'template': {'limits': {'daily': 5, 'monthly': 50}, 'tags': []},
                         'copies': [{'limits': {'daily': 0, 'monthly': 0}, 'tags': ['x']}]},
            'label': 'one change can update all fields'},
           {'input': {'template': {'limits': {'daily': 0, 'monthly': 0}, 'tags': []},
                      'changes': []},
            'expected': {'template': {'limits': {'daily': 0, 'monthly': 0}, 'tags': []},
                         'copies': []},
            'label': 'no requested copies'},
           {'input': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': ['a']},
                      'changes': [{}]},
            'expected': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': ['a']},
                         'copies': [{'limits': {'daily': 1, 'monthly': 2}, 'tags': ['a']}]},
            'label': 'unchanged copy'},
           {'input': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': ['a']},
                      'changes': [{'tag': 'a'}]},
            'expected': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': ['a']},
                         'copies': [{'limits': {'daily': 1, 'monthly': 2}, 'tags': ['a', 'a']}]},
            'label': 'duplicate tag appended'},
           {'input': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': []},
                      'changes': [{'tag': ''}]},
            'expected': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': []},
                         'copies': [{'limits': {'daily': 1, 'monthly': 2}, 'tags': ['']}]},
            'label': 'empty tag is present'},
           {'input': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': []},
                      'changes': [{'monthly': 9}]},
            'expected': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': []},
                         'copies': [{'limits': {'daily': 1, 'monthly': 9}, 'tags': []}]},
            'label': 'monthly only'},
           {'input': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': []},
                      'changes': [{'daily': 3}, {'daily': 4}]},
            'expected': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': []},
                         'copies': [{'limits': {'daily': 3, 'monthly': 2}, 'tags': []},
                                    {'limits': {'daily': 4, 'monthly': 2}, 'tags': []}]},
            'label': 'later copy cannot rewrite earlier copy'},
           {'input': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': []},
                      'changes': [{'tag': 'x'}, {'tag': 'y'}]},
            'expected': {'template': {'limits': {'daily': 1, 'monthly': 2}, 'tags': []},
                         'copies': [{'limits': {'daily': 1, 'monthly': 2}, 'tags': ['x']},
                                    {'limits': {'daily': 1, 'monthly': 2}, 'tags': ['y']}]},
            'label': 'tags do not accumulate across copies'},
           {'input': {'template': {'limits': {'daily': 0, 'monthly': 10}, 'tags': ['x', 'y']},
                      'changes': [{'daily': 0}]},
            'expected': {'template': {'limits': {'daily': 0, 'monthly': 10}, 'tags': ['x', 'y']},
                         'copies': [{'limits': {'daily': 0, 'monthly': 10}, 'tags': ['x', 'y']}]},
            'label': 'assign existing value'},
           {'input': {'template': {'limits': {'daily': 1000000, 'monthly': 1000000}, 'tags': []},
                      'changes': [{'daily': 1}]},
            'expected': {'template': {'limits': {'daily': 1000000, 'monthly': 1000000}, 'tags': []},
                         'copies': [{'limits': {'daily': 1, 'monthly': 1000000}, 'tags': []}]},
            'label': 'large template values'},
           {'input': {'template': {'limits': {'daily': 2, 'monthly': 3}, 'tags': ['雪']},
                      'changes': [{}, {'tag': '水'}, {}]},
            'expected': {'template': {'limits': {'daily': 2, 'monthly': 3}, 'tags': ['雪']},
                         'copies': [{'limits': {'daily': 2, 'monthly': 3}, 'tags': ['雪']},
                                    {'limits': {'daily': 2, 'monthly': 3}, 'tags': ['雪', '水']},
                                    {'limits': {'daily': 2, 'monthly': 3}, 'tags': ['雪']}]},
            'label': 'unchanged copies surround mutation'}],
 'generated': [{'template': {'limits': {'daily': 0, 'monthly': 0}, 'tags': ['t0']},
                'changes': [{'daily': 1}, {'tag': '0'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 1, 'monthly': 10}, 'tags': ['t1']},
                'changes': [{'daily': 2}, {'tag': '1'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 2, 'monthly': 20}, 'tags': ['t2']},
                'changes': [{'daily': 3}, {'tag': '2'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 3, 'monthly': 30}, 'tags': ['t3']},
                'changes': [{'daily': 4}, {'tag': '3'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 4, 'monthly': 40}, 'tags': ['t4']},
                'changes': [{'daily': 5}, {'tag': '4'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 5, 'monthly': 50}, 'tags': ['t5']},
                'changes': [{'daily': 6}, {'tag': '5'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 6, 'monthly': 60}, 'tags': ['t6']},
                'changes': [{'daily': 7}, {'tag': '6'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 7, 'monthly': 70}, 'tags': ['t7']},
                'changes': [{'daily': 8}, {'tag': '7'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 8, 'monthly': 80}, 'tags': ['t8']},
                'changes': [{'daily': 9}, {'tag': '8'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 9, 'monthly': 90}, 'tags': ['t9']},
                'changes': [{'daily': 10}, {'tag': '9'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 10, 'monthly': 100}, 'tags': ['t10']},
                'changes': [{'daily': 11}, {'tag': '10'}, {'monthly': 0}, {}]},
               {'template': {'limits': {'daily': 11, 'monthly': 110}, 'tags': ['t11']},
                'changes': [{'daily': 12}, {'tag': '11'}, {'monthly': 0}, {}]}],
 'mutations': [{'name': 'copies only outer dictionary',
                'old': 'deepcopy(template)',
                'new': 'template.copy()'}],
 'sources': ['https://docs.python.org/3.11/library/copy.html']}
