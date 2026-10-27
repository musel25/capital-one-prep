"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 10,
 'slug': 'stable-priority-jobs',
 'title': 'Schedule jobs with stable priorities',
 'difficulty': 'Medium',
 'time': 25,
 'prerequisites': 'Lists, dictionaries, and functions.',
 'learn': 'A heap provides efficient access to the smallest key. heapq uses Python tuple ordering, '
          'so a tuple can hold a priority, an insertion sequence, and the job payload. The '
          'sequence gives a stable tie rule and prevents the payload from deciding the order. Keep '
          'the sequence increasing across all insertions, including after a pop. A heap’s internal '
          'list is not globally sorted. If you need a final ordered report, sort a copy or drain a '
          'separate heap. Empty pops need an explicit result. This task uses null so the result '
          'list still contains one entry for each requested pop.',
 'scenario': ('A background worker runs jobs from a queue. Each job has a priority, and a smaller number is more urgent. Jobs with equal priority run in the order they were added. `solve` simulates the queue: `add` puts a job in, and `pop` takes out the next job to run.'),
 'example_notes': ['`fast` (priority 1) runs before `slow` (priority 5).', 'Equal priority: `z` was added first, so it runs first.', 'No actions.'],
 'task': ('**Input:** `data` has:\n'
    '- `actions`: a list of operations:\n'
    '  - `{"op": "add", "id": string, "priority": int}` adds a job. Priority is from -100 to 100. A smaller value runs first.\n'
    '  - `{"op": "pop"}` removes the next job.\n'
    '\n'
    '**Rules**\n'
    '- Jobs with equal priority run in insertion order.\n'
    '- IDs can repeat.\n'
    '- A `pop` records the ID of the removed job, or `null` if the queue is empty.\n'
    '- An `add` records nothing.\n'
    '\n'
    '**Return** `{"popped": [...], "pending": [...]}`\n'
    '- `popped`: the result of each `pop`, in order.\n'
    '- `pending`: the IDs still in the queue, in the order they would be popped.\n'
    '\n'
    '**Practice:** use `heapq`. The judge checks only the output.'),
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['Use a tuple of priority, insertion sequence, and ID.',
           'Do not return the internal heap array as the pending order.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'import heapq\n'
              '\n'
              'def solve(data: dict) -> dict:\n'
              '    heap = []\n'
              '    popped = []\n'
              '    sequence = 0\n'
              "    for action in data['actions']:\n"
              "        if action['op'] == 'add':\n"
              "            heapq.heappush(heap, (action['priority'], sequence, action['id']))\n"
              '            sequence += 1\n'
              '        else:\n'
              '            popped.append(heapq.heappop(heap)[2] if heap else None)\n'
              "    return {'popped': popped, 'pending': [entry[2] for entry in sorted(heap)]}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    PriorityQueue<List<Object>> q=new PriorityQueue<>((a,b)->{ int '
         'c=Integer.compare(n(a.get(0)),n(b.get(0))); return '
         'c!=0?c:Integer.compare(n(a.get(1)),n(b.get(1))); });\n'
         '    List<Object> popped=new ArrayList<>(),pending=new ArrayList<>(); int sequence=0;\n'
         '    for(Object x:arr(d.get("actions"))) { Map<String,Object> a=obj(x);\n'
         '        if(s(a.get("op")).equals("add")) '
         'q.add(list(a.get("priority"),sequence++,a.get("id")));\n'
         '        else popped.add(q.isEmpty()?null:q.remove().get(2));\n'
         '    }\n'
         '    while(!q.isEmpty()) pending.add(q.remove().get(2)); return '
         'map("popped",popped,"pending",pending);\n'
         '}',
 'approach': 'The reference uses heapq with a monotonic insertion sequence. Each add or nonempty '
             'pop costs O(log n). The final pending sort costs O(n log n); storage is O(n). The '
             'judge verifies stable behavior, not heap use or complexity. This is a single-process '
             'simulation without worker execution or persistence.',
 'cases': [{'input': {'actions': [{'op': 'add', 'id': 'slow', 'priority': 5},
                                  {'op': 'add', 'id': 'fast', 'priority': 1},
                                  {'op': 'pop'}]},
            'expected': {'popped': ['fast'], 'pending': ['slow']},
            'label': 'smallest priority first'},
           {'input': {'actions': [{'op': 'add', 'id': 'z', 'priority': 1},
                                  {'op': 'add', 'id': 'a', 'priority': 1},
                                  {'op': 'pop'}]},
            'expected': {'popped': ['z'], 'pending': ['a']},
            'label': 'equal priorities use insertion order'},
           {'input': {'actions': []},
            'expected': {'popped': [], 'pending': []},
            'label': 'empty action list'},
           {'input': {'actions': [{'op': 'pop'}, {'op': 'pop'}]},
            'expected': {'popped': [None, None], 'pending': []},
            'label': 'empty pops'},
           {'input': {'actions': [{'op': 'add', 'id': 'A', 'priority': 0}]},
            'expected': {'popped': [], 'pending': ['A']},
            'label': 'single pending job'},
           {'input': {'actions': [{'op': 'add', 'id': 'A', 'priority': 0},
                                  {'op': 'pop'},
                                  {'op': 'pop'}]},
            'expected': {'popped': ['A', None], 'pending': []},
            'label': 'drain then empty pop'},
           {'input': {'actions': [{'op': 'add', 'id': 'A', 'priority': 100},
                                  {'op': 'add', 'id': 'B', 'priority': -100}]},
            'expected': {'popped': [], 'pending': ['B', 'A']},
            'label': 'priority boundaries'},
           {'input': {'actions': [{'op': 'add', 'id': 'same', 'priority': 2},
                                  {'op': 'add', 'id': 'same', 'priority': 2},
                                  {'op': 'pop'},
                                  {'op': 'pop'}]},
            'expected': {'popped': ['same', 'same'], 'pending': []},
            'label': 'duplicate job IDs'},
           {'input': {'actions': [{'op': 'add', 'id': 'A', 'priority': 0},
                                  {'op': 'pop'},
                                  {'op': 'add', 'id': 'B', 'priority': 0},
                                  {'op': 'add', 'id': 'C', 'priority': 0}]},
            'expected': {'popped': ['A'], 'pending': ['B', 'C']},
            'label': 'new jobs after draining'},
           {'input': {'actions': [{'op': 'add', 'id': 'A', 'priority': 3},
                                  {'op': 'add', 'id': 'B', 'priority': 1},
                                  {'op': 'add', 'id': 'C', 'priority': 2},
                                  {'op': 'add', 'id': 'D', 'priority': 0}]},
            'expected': {'popped': [], 'pending': ['D', 'B', 'C', 'A']},
            'label': 'pending report is fully sorted'},
           {'input': {'actions': [{'op': 'pop'},
                                  {'op': 'add', 'id': '', 'priority': 0},
                                  {'op': 'pop'}]},
            'expected': {'popped': [None, ''], 'pending': []},
            'label': 'empty ID differs from null'},
           {'input': {'actions': [{'op': 'add', 'id': 'A', 'priority': 2},
                                  {'op': 'add', 'id': 'B', 'priority': 2},
                                  {'op': 'pop'},
                                  {'op': 'add', 'id': 'C', 'priority': 1},
                                  {'op': 'pop'}]},
            'expected': {'popped': ['A', 'C'], 'pending': ['B']},
            'label': 'new urgent job passes waiting job'}],
 'generated': [{'actions': [{'op': 'add', 'id': '0-0', 'priority': -1},
                            {'op': 'add', 'id': '0-1', 'priority': 0},
                            {'op': 'add', 'id': '0-2', 'priority': 1}]},
               {'actions': [{'op': 'add', 'id': '1-0', 'priority': 0},
                            {'op': 'add', 'id': '1-1', 'priority': 1},
                            {'op': 'add', 'id': '1-2', 'priority': -1},
                            {'op': 'add', 'id': '1-3', 'priority': 0},
                            {'op': 'pop'}]},
               {'actions': [{'op': 'add', 'id': '2-0', 'priority': 1},
                            {'op': 'add', 'id': '2-1', 'priority': -1},
                            {'op': 'add', 'id': '2-2', 'priority': 0},
                            {'op': 'add', 'id': '2-3', 'priority': 1},
                            {'op': 'add', 'id': '2-4', 'priority': -1},
                            {'op': 'pop'},
                            {'op': 'pop'}]},
               {'actions': [{'op': 'add', 'id': '3-0', 'priority': -1},
                            {'op': 'add', 'id': '3-1', 'priority': 0},
                            {'op': 'add', 'id': '3-2', 'priority': 1},
                            {'op': 'add', 'id': '3-3', 'priority': -1},
                            {'op': 'add', 'id': '3-4', 'priority': 0},
                            {'op': 'add', 'id': '3-5', 'priority': 1},
                            {'op': 'pop'},
                            {'op': 'pop'},
                            {'op': 'pop'}]},
               {'actions': [{'op': 'add', 'id': '4-0', 'priority': 0},
                            {'op': 'add', 'id': '4-1', 'priority': 1},
                            {'op': 'add', 'id': '4-2', 'priority': -1},
                            {'op': 'pop'},
                            {'op': 'pop'},
                            {'op': 'pop'},
                            {'op': 'pop'}]},
               {'actions': [{'op': 'add', 'id': '5-0', 'priority': 1},
                            {'op': 'add', 'id': '5-1', 'priority': -1},
                            {'op': 'add', 'id': '5-2', 'priority': 0},
                            {'op': 'add', 'id': '5-3', 'priority': 1}]},
               {'actions': [{'op': 'add', 'id': '6-0', 'priority': -1},
                            {'op': 'add', 'id': '6-1', 'priority': 0},
                            {'op': 'add', 'id': '6-2', 'priority': 1},
                            {'op': 'add', 'id': '6-3', 'priority': -1},
                            {'op': 'add', 'id': '6-4', 'priority': 0},
                            {'op': 'pop'}]},
               {'actions': [{'op': 'add', 'id': '7-0', 'priority': 0},
                            {'op': 'add', 'id': '7-1', 'priority': 1},
                            {'op': 'add', 'id': '7-2', 'priority': -1},
                            {'op': 'add', 'id': '7-3', 'priority': 0},
                            {'op': 'add', 'id': '7-4', 'priority': 1},
                            {'op': 'add', 'id': '7-5', 'priority': -1},
                            {'op': 'pop'},
                            {'op': 'pop'}]},
               {'actions': [{'op': 'add', 'id': '8-0', 'priority': 1},
                            {'op': 'add', 'id': '8-1', 'priority': -1},
                            {'op': 'add', 'id': '8-2', 'priority': 0},
                            {'op': 'pop'},
                            {'op': 'pop'},
                            {'op': 'pop'}]},
               {'actions': [{'op': 'add', 'id': '9-0', 'priority': -1},
                            {'op': 'add', 'id': '9-1', 'priority': 0},
                            {'op': 'add', 'id': '9-2', 'priority': 1},
                            {'op': 'add', 'id': '9-3', 'priority': -1},
                            {'op': 'pop'},
                            {'op': 'pop'},
                            {'op': 'pop'},
                            {'op': 'pop'}]},
               {'actions': [{'op': 'add', 'id': '10-0', 'priority': 0},
                            {'op': 'add', 'id': '10-1', 'priority': 1},
                            {'op': 'add', 'id': '10-2', 'priority': -1},
                            {'op': 'add', 'id': '10-3', 'priority': 0},
                            {'op': 'add', 'id': '10-4', 'priority': 1}]},
               {'actions': [{'op': 'add', 'id': '11-0', 'priority': 1},
                            {'op': 'add', 'id': '11-1', 'priority': -1},
                            {'op': 'add', 'id': '11-2', 'priority': 0},
                            {'op': 'add', 'id': '11-3', 'priority': 1},
                            {'op': 'add', 'id': '11-4', 'priority': -1},
                            {'op': 'add', 'id': '11-5', 'priority': 0},
                            {'op': 'pop'}]}],
 'mutations': [{'name': 'uses newest job first on equal priorities',
                'old': "(action['priority'], sequence, action['id'])",
                'new': "(action['priority'], -sequence, action['id'])"}],
 'sources': ['https://docs.python.org/3.11/library/heapq.html#priority-queue-implementation-notes']}
