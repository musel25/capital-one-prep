"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 20,
 'slug': 'typed-memory-ledger',
 'title': 'Build a typed in-memory ledger',
 'difficulty': 'Medium',
 'time': 35,
 'prerequisites': 'Exercises 11–19: object state, invariants, atomic changes, and event IDs.',
 'learn': 'A small ledger combines several rules that must agree. Account objects hold balances. A '
          'ledger object coordinates transfers so one debit and one credit form a complete '
          'operation. A TypedDict describes the transfer input, while immutable tuples record '
          'event payloads for duplicate checks. The event ID policy must also define failed '
          'requests. In this task, the first request reserves its ID even if it has insufficient '
          'funds. Retrying it cannot later turn the same ID into a different operation. A new ID '
          'is required for a new attempt. Keep duplicate detection before balance changes and '
          'check funds before either side of a transfer changes.',
 'task': '`data.accounts` maps account IDs to nonnegative integer cents. `data.events` contains '
         '`{"id":string,"from":account_id,"to":account_id,"cents":nonnegative_integer}`. Both '
         'accounts exist. Process events in order. The first event for an ID stores its payload '
         '`(from,to,cents)`. It returns `applied` and transfers cents if the source has enough '
         'funds; otherwise it returns `insufficient` and changes no balances. The ID remains '
         'stored after either result. A later identical payload returns `duplicate`; a different '
         'payload with that ID returns `conflict`. Neither changes balances or the stored payload. '
         'A self-transfer checks funds, then leaves balances unchanged. Return `{"status": '
         '[strings], "balances": final_account_map}`. Practice typed objects and composition. The '
         'judge checks outputs only.',
 'constraints': ['At most 30 accounts and 100 events. Initial balances and event cents are at most '
                 '1,000,000,000,000. Input objects follow the stated types; runtime boundary '
                 'validation is outside this task.'],
 'hints': ['Store the original payload before attempting the first transfer.',
           'Let one ledger method coordinate duplicate checks and both balance changes.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'from dataclasses import dataclass\n'
              'from typing import TypedDict\n'
              '\n'
              "Transfer = TypedDict('Transfer', {'id': str, 'from': str, 'to': str, 'cents': "
              'int})\n'
              '\n'
              '@dataclass\n'
              'class Account:\n'
              '    balance: int\n'
              '\n'
              '    def debit(self, cents: int) -> bool:\n'
              '        if cents > self.balance:\n'
              '            return False\n'
              '        self.balance -= cents\n'
              '        return True\n'
              '\n'
              '    def credit(self, cents: int) -> None:\n'
              '        self.balance += cents\n'
              '\n'
              'class Ledger:\n'
              '    def __init__(self, balances: dict[str, int]):\n'
              '        self.accounts = {key: Account(value) for key, value in balances.items()}\n'
              '        self.seen: dict[str, tuple[str, str, int]] = {}\n'
              '\n'
              '    def apply(self, event: Transfer) -> str:\n'
              "        identifier = event['id']\n"
              "        payload = (event['from'], event['to'], event['cents'])\n"
              '        if identifier in self.seen:\n'
              "            return 'duplicate' if self.seen[identifier] == payload else 'conflict'\n"
              '        self.seen[identifier] = payload\n'
              '        source, target, cents = payload\n'
              '        if not self.accounts[source].debit(cents):\n'
              "            return 'insufficient'\n"
              '        self.accounts[target].credit(cents)\n'
              "        return 'applied'\n"
              '\n'
              'def solve(data: dict) -> dict:\n'
              "    ledger = Ledger(data['accounts'])\n"
              "    status = [ledger.apply(event) for event in data['events']]\n"
              "    return {'status': status, 'balances': {key: account.balance for key, account in "
              'ledger.accounts.items()}}\n',
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    Map<String,Long> balances=new LinkedHashMap<>();for(Map.Entry<String,Object> '
         'e:obj(d.get("accounts")).entrySet())balances.put(e.getKey(),lng(e.getValue()));\n'
         '    Map<String,List<Object>> seen=new HashMap<>();List<Object> status=new '
         'ArrayList<>();\n'
         '    for(Object x:arr(d.get("events"))){Map<String,Object> e=obj(x);String '
         'id=s(e.get("id")),from=s(e.get("from")),to=s(e.get("to"));long '
         'cents=lng(e.get("cents"));List<Object> payload=list(from,to,cents);\n'
         '        '
         'if(seen.containsKey(id)){status.add(J.equal(seen.get(id),payload)?"duplicate":"conflict");continue;}\n'
         '        '
         'seen.put(id,payload);if(balances.get(from)<cents){status.add("insufficient");continue;}\n'
         '        '
         'balances.put(from,balances.get(from)-cents);balances.put(to,balances.get(to)+cents);status.add("applied");\n'
         '    }\n'
         '    return map("status",status,"balances",balances);\n'
         '}',
 'approach': 'The reference demonstrates TypedDict, dataclasses, account methods, and a ledger '
             'that composes account objects. Expected time is O(a + e), and memory is O(a + e), '
             'for a accounts and e events. The judge checks status and balances. It cannot certify '
             'typing or object design. Atomicity here covers this deterministic in-memory call '
             'only; production ledgers require durable transactions and concurrent access control.',
 'cases': [{'input': {'accounts': {'A': 10, 'B': 0},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'B', 'cents': 4},
                                 {'id': 'x', 'from': 'A', 'to': 'B', 'cents': 4},
                                 {'id': 'x', 'from': 'A', 'to': 'B', 'cents': 5}]},
            'expected': {'status': ['applied', 'duplicate', 'conflict'],
                         'balances': {'A': 6, 'B': 4}},
            'label': 'transfer, duplicate, and conflict'},
           {'input': {'accounts': {'A': 0, 'B': 10},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'B', 'cents': 5},
                                 {'id': 'fund', 'from': 'B', 'to': 'A', 'cents': 10},
                                 {'id': 'x', 'from': 'A', 'to': 'B', 'cents': 5},
                                 {'id': 'new', 'from': 'A', 'to': 'B', 'cents': 5}]},
            'expected': {'status': ['insufficient', 'applied', 'duplicate', 'applied'],
                         'balances': {'A': 5, 'B': 5}},
            'label': 'failed ID stays reserved after new funds arrive'},
           {'input': {'accounts': {}, 'events': []},
            'expected': {'status': [], 'balances': {}},
            'label': 'empty ledger'},
           {'input': {'accounts': {'A': 5, 'B': 0}, 'events': []},
            'expected': {'status': [], 'balances': {'A': 5, 'B': 0}},
            'label': 'unchanged account map'},
           {'input': {'accounts': {'A': 5, 'B': 0},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'B', 'cents': 5}]},
            'expected': {'status': ['applied'], 'balances': {'A': 0, 'B': 5}},
            'label': 'exact-balance transfer'},
           {'input': {'accounts': {'A': 0, 'B': 0},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'B', 'cents': 0},
                                 {'id': 'x', 'from': 'A', 'to': 'B', 'cents': 0}]},
            'expected': {'status': ['applied', 'duplicate'], 'balances': {'A': 0, 'B': 0}},
            'label': 'zero-cent event has identity'},
           {'input': {'accounts': {'A': 5},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'A', 'cents': 5},
                                 {'id': 'y', 'from': 'A', 'to': 'A', 'cents': 6}]},
            'expected': {'status': ['applied', 'insufficient'], 'balances': {'A': 5}},
            'label': 'self-transfer preserves funds and checks limit'},
           {'input': {'accounts': {'A': 10, 'B': 0, 'C': 0},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'B', 'cents': 3},
                                 {'id': 'x', 'from': 'A', 'to': 'C', 'cents': 3},
                                 {'id': 'x', 'from': 'A', 'to': 'B', 'cents': 3}]},
            'expected': {'status': ['applied', 'conflict', 'duplicate'],
                         'balances': {'A': 7, 'B': 3, 'C': 0}},
            'label': 'destination is part of payload'},
           {'input': {'accounts': {'A': 10, 'B': 10, 'C': 0},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'C', 'cents': 3},
                                 {'id': 'x', 'from': 'B', 'to': 'C', 'cents': 3}]},
            'expected': {'status': ['applied', 'conflict'], 'balances': {'A': 7, 'B': 10, 'C': 3}},
            'label': 'source is part of payload'},
           {'input': {'accounts': {'A': 10, 'B': 0},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'B', 'cents': 3},
                                 {'id': 'y', 'from': 'A', 'to': 'B', 'cents': 3}]},
            'expected': {'status': ['applied', 'applied'], 'balances': {'A': 4, 'B': 6}},
            'label': 'new ID applies same payload again'},
           {'input': {'accounts': {'A': 1, 'B': 0},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'B', 'cents': 2},
                                 {'id': 'x', 'from': 'A', 'to': 'B', 'cents': 1},
                                 {'id': 'x', 'from': 'A', 'to': 'B', 'cents': 2}]},
            'expected': {'status': ['insufficient', 'conflict', 'duplicate'],
                         'balances': {'A': 1, 'B': 0}},
            'label': 'failed event still defines its original payload'},
           {'input': {'accounts': {'A': 1000000000000, 'B': 0},
                      'events': [{'id': 'x', 'from': 'A', 'to': 'B', 'cents': 1000000000000},
                                 {'id': 'y', 'from': 'B', 'to': 'A', 'cents': 1000000000000}]},
            'expected': {'status': ['applied', 'applied'],
                         'balances': {'A': 1000000000000, 'B': 0}},
            'label': 'large exact round trip'},
           {'input': {'accounts': {'': 2, 'B': 0},
                      'events': [{'id': '', 'from': '', 'to': 'B', 'cents': 1},
                                 {'id': '', 'from': '', 'to': 'B', 'cents': 1}]},
            'expected': {'status': ['applied', 'duplicate'], 'balances': {'': 1, 'B': 1}},
            'label': 'empty account and event identifiers'}],
 'generated': [{'accounts': {'A': 20, 'B': 0, 'C': 0},
                'events': [{'id': 'x0', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'x0', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'x0', 'from': 'A', 'to': 'C', 'cents': 1},
                           {'id': 'y0', 'from': 'B', 'to': 'C', 'cents': 2},
                           {'id': 'z0', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y0', 'from': 'B', 'to': 'C', 'cents': 2}]},
               {'accounts': {'A': 21, 'B': 0, 'C': 0},
                'events': [{'id': 'x1', 'from': 'A', 'to': 'B', 'cents': 2},
                           {'id': 'x1', 'from': 'A', 'to': 'B', 'cents': 2},
                           {'id': 'x1', 'from': 'A', 'to': 'C', 'cents': 2},
                           {'id': 'y1', 'from': 'B', 'to': 'C', 'cents': 3},
                           {'id': 'z1', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y1', 'from': 'B', 'to': 'C', 'cents': 3}]},
               {'accounts': {'A': 22, 'B': 0, 'C': 0},
                'events': [{'id': 'x2', 'from': 'A', 'to': 'B', 'cents': 3},
                           {'id': 'x2', 'from': 'A', 'to': 'B', 'cents': 3},
                           {'id': 'x2', 'from': 'A', 'to': 'C', 'cents': 3},
                           {'id': 'y2', 'from': 'B', 'to': 'C', 'cents': 4},
                           {'id': 'z2', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y2', 'from': 'B', 'to': 'C', 'cents': 4}]},
               {'accounts': {'A': 23, 'B': 0, 'C': 0},
                'events': [{'id': 'x3', 'from': 'A', 'to': 'B', 'cents': 4},
                           {'id': 'x3', 'from': 'A', 'to': 'B', 'cents': 4},
                           {'id': 'x3', 'from': 'A', 'to': 'C', 'cents': 4},
                           {'id': 'y3', 'from': 'B', 'to': 'C', 'cents': 5},
                           {'id': 'z3', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y3', 'from': 'B', 'to': 'C', 'cents': 5}]},
               {'accounts': {'A': 24, 'B': 0, 'C': 0},
                'events': [{'id': 'x4', 'from': 'A', 'to': 'B', 'cents': 5},
                           {'id': 'x4', 'from': 'A', 'to': 'B', 'cents': 5},
                           {'id': 'x4', 'from': 'A', 'to': 'C', 'cents': 5},
                           {'id': 'y4', 'from': 'B', 'to': 'C', 'cents': 6},
                           {'id': 'z4', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y4', 'from': 'B', 'to': 'C', 'cents': 6}]},
               {'accounts': {'A': 25, 'B': 0, 'C': 0},
                'events': [{'id': 'x5', 'from': 'A', 'to': 'B', 'cents': 6},
                           {'id': 'x5', 'from': 'A', 'to': 'B', 'cents': 6},
                           {'id': 'x5', 'from': 'A', 'to': 'C', 'cents': 6},
                           {'id': 'y5', 'from': 'B', 'to': 'C', 'cents': 7},
                           {'id': 'z5', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y5', 'from': 'B', 'to': 'C', 'cents': 7}]},
               {'accounts': {'A': 26, 'B': 0, 'C': 0},
                'events': [{'id': 'x6', 'from': 'A', 'to': 'B', 'cents': 7},
                           {'id': 'x6', 'from': 'A', 'to': 'B', 'cents': 7},
                           {'id': 'x6', 'from': 'A', 'to': 'C', 'cents': 7},
                           {'id': 'y6', 'from': 'B', 'to': 'C', 'cents': 8},
                           {'id': 'z6', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y6', 'from': 'B', 'to': 'C', 'cents': 8}]},
               {'accounts': {'A': 27, 'B': 0, 'C': 0},
                'events': [{'id': 'x7', 'from': 'A', 'to': 'B', 'cents': 8},
                           {'id': 'x7', 'from': 'A', 'to': 'B', 'cents': 8},
                           {'id': 'x7', 'from': 'A', 'to': 'C', 'cents': 8},
                           {'id': 'y7', 'from': 'B', 'to': 'C', 'cents': 9},
                           {'id': 'z7', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y7', 'from': 'B', 'to': 'C', 'cents': 9}]},
               {'accounts': {'A': 28, 'B': 0, 'C': 0},
                'events': [{'id': 'x8', 'from': 'A', 'to': 'B', 'cents': 9},
                           {'id': 'x8', 'from': 'A', 'to': 'B', 'cents': 9},
                           {'id': 'x8', 'from': 'A', 'to': 'C', 'cents': 9},
                           {'id': 'y8', 'from': 'B', 'to': 'C', 'cents': 10},
                           {'id': 'z8', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y8', 'from': 'B', 'to': 'C', 'cents': 10}]},
               {'accounts': {'A': 29, 'B': 0, 'C': 0},
                'events': [{'id': 'x9', 'from': 'A', 'to': 'B', 'cents': 10},
                           {'id': 'x9', 'from': 'A', 'to': 'B', 'cents': 10},
                           {'id': 'x9', 'from': 'A', 'to': 'C', 'cents': 10},
                           {'id': 'y9', 'from': 'B', 'to': 'C', 'cents': 11},
                           {'id': 'z9', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y9', 'from': 'B', 'to': 'C', 'cents': 11}]},
               {'accounts': {'A': 30, 'B': 0, 'C': 0},
                'events': [{'id': 'x10', 'from': 'A', 'to': 'B', 'cents': 11},
                           {'id': 'x10', 'from': 'A', 'to': 'B', 'cents': 11},
                           {'id': 'x10', 'from': 'A', 'to': 'C', 'cents': 11},
                           {'id': 'y10', 'from': 'B', 'to': 'C', 'cents': 12},
                           {'id': 'z10', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y10', 'from': 'B', 'to': 'C', 'cents': 12}]},
               {'accounts': {'A': 31, 'B': 0, 'C': 0},
                'events': [{'id': 'x11', 'from': 'A', 'to': 'B', 'cents': 12},
                           {'id': 'x11', 'from': 'A', 'to': 'B', 'cents': 12},
                           {'id': 'x11', 'from': 'A', 'to': 'C', 'cents': 12},
                           {'id': 'y11', 'from': 'B', 'to': 'C', 'cents': 13},
                           {'id': 'z11', 'from': 'A', 'to': 'B', 'cents': 1},
                           {'id': 'y11', 'from': 'B', 'to': 'C', 'cents': 13}]}],
 'mutations': [{'name': 'credits destination without debiting source',
                'old': 'self.balance -= cents',
                'new': 'self.balance -= 0'}],
 'sources': ['https://docs.python.org/3.11/library/typing.html#typing.TypedDict',
             'https://docs.python.org/3.11/library/dataclasses.html']}
