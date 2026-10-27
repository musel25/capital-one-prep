"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 17,
 'slug': 'atomic-memory-batch',
 'title': 'Fix an in-memory transfer batch',
 'difficulty': 'Medium',
 'time': 25,
 'prerequisites': 'Dictionary copies, account invariants, and ordered operations.',
 'learn': 'Atomic means that an operation has one complete result: all intended changes happen, or '
          'none happen. A loop that updates live balances can leave a partial result when a later '
          'transfer fails. For a small in-memory model, start with a working copy. Apply each '
          'transfer to that copy in order. Earlier transfers in the same batch can fund later '
          'transfers. Publish the working copy only after every transfer succeeds. On failure, '
          'discard it. This method is a simulation of atomic behavior within one call. It does not '
          'create a database transaction or protect the state from concurrent callers.',
 'task': ('**Bug fix.** The starter keeps part of a rejected batch (a partial write). Repair it.\n'
    '\n'
    '**Input:** `data` has:\n'
    '- `accounts`: maps account IDs to nonnegative integer cents.\n'
    '- `batches`: a list of batches. Each batch is a list of transfers `{"from": string, "to": string, "cents": int}`, with nonnegative `cents`. Both accounts always exist.\n'
    '\n'
    '**Rules**\n'
    '- Process batches in order. Inside a batch, process transfers in order. Each transfer uses the balances after the earlier transfers in the same batch.\n'
    '- If any source has less than `cents`, reject the whole batch and restore the balances from the start of that batch.\n'
    '- Otherwise accept the batch and keep all its transfers.\n'
    '- A self-transfer needs enough funds but does not change the balance.\n'
    '- An empty batch is accepted.\n'
    '\n'
    '**Return** `{"accepted": [bool], "balances": {...}}`: one boolean per batch, and the final account map.'),
 'constraints': ['At most 30 accounts, 30 batches, and 100 transfers per batch. Input cents and '
                 'initial balances are at most 1,000,000,000,000.'],
 'hints': ['Apply changes to a separate candidate state.',
           'Assign the candidate state to live state only after the complete batch passes.'],
 'starter': 'class Ledger:\n'
            '    def __init__(self, balances: dict[str, int]):\n'
            '        self.balances = balances.copy()\n'
            '\n'
            '    def apply_batch(self, transfers: list[dict]) -> bool:\n'
            '        trial = self.balances\n'
            '        for transfer in transfers:\n'
            "            source, target, cents = transfer['from'], transfer['to'], "
            "transfer['cents']\n"
            '            if trial[source] < cents:\n'
            '                return False\n'
            '            trial[source] -= cents\n'
            '            trial[target] += cents\n'
            '        self.balances = trial\n'
            '        return True\n'
            '\n'
            'def solve(data: dict) -> dict:\n'
            "    ledger = Ledger(data['accounts'])\n"
            "    accepted = [ledger.apply_batch(batch) for batch in data['batches']]\n"
            "    return {'accepted': accepted, 'balances': ledger.balances}\n",
 'reference': 'class Ledger:\n'
              '    def __init__(self, balances: dict[str, int]):\n'
              '        self.balances = balances.copy()\n'
              '\n'
              '    def apply_batch(self, transfers: list[dict]) -> bool:\n'
              '        trial = self.balances.copy()\n'
              '        for transfer in transfers:\n'
              "            source, target, cents = transfer['from'], transfer['to'], "
              "transfer['cents']\n"
              '            if trial[source] < cents:\n'
              '                return False\n'
              '            trial[source] -= cents\n'
              '            trial[target] += cents\n'
              '        self.balances = trial\n'
              '        return True\n'
              '\n'
              'def solve(data: dict) -> dict:\n'
              "    ledger = Ledger(data['accounts'])\n"
              "    accepted = [ledger.apply_batch(batch) for batch in data['batches']]\n"
              "    return {'accepted': accepted, 'balances': ledger.balances}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    Map<String,Long> balances=new LinkedHashMap<>(); for(Map.Entry<String,Object> '
         'e:obj(d.get("accounts")).entrySet())balances.put(e.getKey(),lng(e.getValue()));\n'
         '    List<Object> accepted=new ArrayList<>();\n'
         '    for(Object x:arr(d.get("batches"))) { Map<String,Long> trial=new '
         'LinkedHashMap<>(balances); boolean ok=true;\n'
         '        for(Object y:arr(x)) {Map<String,Object> t=obj(y);String '
         'from=s(t.get("from")),to=s(t.get("to"));long amount=lng(t.get("cents"));\n'
         '            if(trial.get(from)<amount){ok=false;break;} '
         'trial.put(from,trial.get(from)-amount);trial.put(to,trial.get(to)+amount);\n'
         '        }\n'
         '        if(ok)balances=trial; accepted.add(ok);\n'
         '    }\n'
         '    return map("accepted",accepted,"balances",balances);\n'
         '}',
 'approach': 'Each batch copies the account map, then validates and applies transfers on that '
             'copy. With a accounts and t transfers, one batch costs O(a + t) time and O(a) '
             'temporary space. Official tests expose partial writes and sequential funding. The '
             'judge does not test database transactions, process crashes, or concurrent writers.',
 'cases': [{'input': {'accounts': {'A': 10, 'B': 0},
                      'batches': [[{'from': 'A', 'to': 'B', 'cents': 6},
                                   {'from': 'A', 'to': 'B', 'cents': 5}]]},
            'expected': {'accepted': [False], 'balances': {'A': 10, 'B': 0}},
            'label': 'late failure rolls back earlier transfer'},
           {'input': {'accounts': {'A': 10, 'B': 0, 'C': 0},
                      'batches': [[{'from': 'A', 'to': 'B', 'cents': 7},
                                   {'from': 'B', 'to': 'C', 'cents': 7}]]},
            'expected': {'accepted': [True], 'balances': {'A': 3, 'B': 0, 'C': 7}},
            'label': 'earlier transfer funds later transfer'},
           {'input': {'accounts': {}, 'batches': []},
            'expected': {'accepted': [], 'balances': {}},
            'label': 'no accounts or batches'},
           {'input': {'accounts': {}, 'batches': [[]]},
            'expected': {'accepted': [True], 'balances': {}},
            'label': 'empty batch succeeds'},
           {'input': {'accounts': {'A': 5, 'B': 0},
                      'batches': [[{'from': 'A', 'to': 'B', 'cents': 5}]]},
            'expected': {'accepted': [True], 'balances': {'A': 0, 'B': 5}},
            'label': 'exact available funds'},
           {'input': {'accounts': {'A': 0, 'B': 0},
                      'batches': [[{'from': 'A', 'to': 'B', 'cents': 1}]]},
            'expected': {'accepted': [False], 'balances': {'A': 0, 'B': 0}},
            'label': 'failure on first transfer'},
           {'input': {'accounts': {'A': 0, 'B': 0},
                      'batches': [[{'from': 'A', 'to': 'B', 'cents': 0}]]},
            'expected': {'accepted': [True], 'balances': {'A': 0, 'B': 0}},
            'label': 'zero transfer'},
           {'input': {'accounts': {'A': 5}, 'batches': [[{'from': 'A', 'to': 'A', 'cents': 5}]]},
            'expected': {'accepted': [True], 'balances': {'A': 5}},
            'label': 'funded self-transfer'},
           {'input': {'accounts': {'A': 5}, 'batches': [[{'from': 'A', 'to': 'A', 'cents': 6}]]},
            'expected': {'accepted': [False], 'balances': {'A': 5}},
            'label': 'self-transfer still checks funds'},
           {'input': {'accounts': {'A': 10, 'B': 0},
                      'batches': [[{'from': 'A', 'to': 'B', 'cents': 6},
                                   {'from': 'A', 'to': 'B', 'cents': 5}],
                                  [{'from': 'A', 'to': 'B', 'cents': 10}]]},
            'expected': {'accepted': [False, True], 'balances': {'A': 0, 'B': 10}},
            'label': 'next batch sees restored funds'},
           {'input': {'accounts': {'A': 5, 'B': 0},
                      'batches': [[{'from': 'A', 'to': 'B', 'cents': 2}],
                                  [{'from': 'A', 'to': 'B', 'cents': 4}],
                                  [{'from': 'B', 'to': 'A', 'cents': 1}]]},
            'expected': {'accepted': [True, False, True], 'balances': {'A': 4, 'B': 1}},
            'label': 'successful batches survive a rejected batch'},
           {'input': {'accounts': {'A': 1000000000000, 'B': 0},
                      'batches': [[{'from': 'A', 'to': 'B', 'cents': 1000000000000},
                                   {'from': 'B', 'to': 'A', 'cents': 1000000000000}]]},
            'expected': {'accepted': [True], 'balances': {'A': 1000000000000, 'B': 0}},
            'label': 'large round trip'},
           {'input': {'accounts': {'A': 1, 'B': 2},
                      'batches': [[], [], [{'from': 'B', 'to': 'A', 'cents': 2}], []]},
            'expected': {'accepted': [True, True, True, True], 'balances': {'A': 3, 'B': 0}},
            'label': 'empty batches around real work'}],
 'generated': [{'accounts': {'A': 10, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 4},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 10}],
                            []]},
               {'accounts': {'A': 11, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 5},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 11}],
                            []]},
               {'accounts': {'A': 12, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 6},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 12}],
                            []]},
               {'accounts': {'A': 13, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 7},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 13}],
                            []]},
               {'accounts': {'A': 14, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 8},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 14}],
                            []]},
               {'accounts': {'A': 15, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 9},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 15}],
                            []]},
               {'accounts': {'A': 16, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 10},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 16}],
                            []]},
               {'accounts': {'A': 17, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 11},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 17}],
                            []]},
               {'accounts': {'A': 18, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 12},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 18}],
                            []]},
               {'accounts': {'A': 19, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 13},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 19}],
                            []]},
               {'accounts': {'A': 20, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 14},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 20}],
                            []]},
               {'accounts': {'A': 21, 'B': 0, 'C': 0},
                'batches': [[{'from': 'A', 'to': 'B', 'cents': 15},
                             {'from': 'A', 'to': 'C', 'cents': 7}],
                            [{'from': 'A', 'to': 'C', 'cents': 21}],
                            []]}],
 'mutations': [{'name': 'writes directly to live balances',
                'old': 'trial = self.balances.copy()',
                'new': 'trial = self.balances'}],
 'sources': ['https://docs.python.org/3.11/library/stdtypes.html#dict.copy']}
