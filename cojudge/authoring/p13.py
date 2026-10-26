"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 13,
 'slug': 'balance-invariants',
 'title': 'Keep an account balance nonnegative',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Classes, methods, and integer cents.',
 'learn': 'An invariant is a rule that must hold after every operation. Here the balance must '
          'never become negative. Put balance changes inside account methods so the rule has one '
          'enforcement point. A property can expose the current balance without providing a public '
          'setter. A leading underscore marks an internal attribute by Python convention; it is '
          'not a security barrier. Check a withdrawal before changing state. If it fails, the '
          'method should return a failure result and leave the balance unchanged. Keeping this '
          'rule in the object makes the calling loop simple and gives future operations a clear '
          'place to enforce the same invariant.',
 'task': '`data.balance` is a nonnegative integer number of cents. `data.actions` contains '
         '`{"op":"deposit"|"withdraw","cents":nonnegative_integer}`. A deposit always succeeds. A '
         'withdrawal succeeds exactly when cents is at most the current balance. A failed '
         'withdrawal changes nothing. Zero-cent actions succeed. Return `{"accepted": [booleans], '
         '"balance": final_integer}` with one boolean per action. Implement an Account class with '
         'controlled balance updates for practice; the output judge checks the invariant’s visible '
         'behavior.',
 'constraints': ['At most 100 actions. Initial balance and action cents are at most '
                 '1,000,000,000,000.'],
 'hints': ['Check the invariant before changing the stored balance.',
           'A failed method must leave the previous balance intact.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'class Account:\n'
              '    def __init__(self, balance: int):\n'
              '        self._balance = balance\n'
              '\n'
              '    @property\n'
              '    def balance(self) -> int:\n'
              '        return self._balance\n'
              '\n'
              '    def deposit(self, cents: int) -> bool:\n'
              '        self._balance += cents\n'
              '        return True\n'
              '\n'
              '    def withdraw(self, cents: int) -> bool:\n'
              '        if cents > self._balance:\n'
              '            return False\n'
              '        self._balance -= cents\n'
              '        return True\n'
              '\n'
              'def solve(data: dict) -> dict:\n'
              "    account = Account(data['balance'])\n"
              '    accepted = []\n'
              "    for action in data['actions']:\n"
              "        method = account.deposit if action['op'] == 'deposit' else "
              'account.withdraw\n'
              "        accepted.append(method(action['cents']))\n"
              "    return {'accepted': accepted, 'balance': account.balance}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    long balance=lng(d.get("balance")); List<Object> accepted=new ArrayList<>();\n'
         '    for(Object x:arr(d.get("actions"))) { Map<String,Object> a=obj(x); long '
         'amount=lng(a.get("cents"));\n'
         '        if(s(a.get("op")).equals("deposit")) { balance+=amount; accepted.add(true); }\n'
         '        else if(amount<=balance) { balance-=amount; accepted.add(true); } else '
         'accepted.add(false);\n'
         '    }\n'
         '    return map("accepted",accepted,"balance",balance);\n'
         '}',
 'approach': 'The reference processes the input in one pass. Time is O(n), and result storage is '
             'O(n). The output judge checks results. It cannot prove the requested Python '
             'technique. This is an in-memory exercise; it does not provide storage or concurrency '
             'control.',
 'cases': [{'input': {'balance': 10,
                      'actions': [{'op': 'withdraw', 'cents': 7}, {'op': 'withdraw', 'cents': 4}]},
            'expected': {'accepted': [True, False], 'balance': 3},
            'label': 'failed withdrawal preserves balance'},
           {'input': {'balance': 0,
                      'actions': [{'op': 'deposit', 'cents': 5}, {'op': 'withdraw', 'cents': 5}]},
            'expected': {'accepted': [True, True], 'balance': 0},
            'label': 'deposit then exact withdrawal'},
           {'input': {'balance': 9, 'actions': []},
            'expected': {'accepted': [], 'balance': 9},
            'label': 'no actions'},
           {'input': {'balance': 0, 'actions': [{'op': 'withdraw', 'cents': 0}]},
            'expected': {'accepted': [True], 'balance': 0},
            'label': 'zero from empty account'},
           {'input': {'balance': 0, 'actions': [{'op': 'withdraw', 'cents': 1}]},
            'expected': {'accepted': [False], 'balance': 0},
            'label': 'overdraft at zero'},
           {'input': {'balance': 10, 'actions': [{'op': 'deposit', 'cents': 0}]},
            'expected': {'accepted': [True], 'balance': 10},
            'label': 'zero deposit'},
           {'input': {'balance': 10, 'actions': [{'op': 'withdraw', 'cents': 10}]},
            'expected': {'accepted': [True], 'balance': 0},
            'label': 'all funds can be withdrawn'},
           {'input': {'balance': 1,
                      'actions': [{'op': 'withdraw', 'cents': 2},
                                  {'op': 'deposit', 'cents': 1},
                                  {'op': 'withdraw', 'cents': 2}]},
            'expected': {'accepted': [False, True, True], 'balance': 0},
            'label': 'failure followed by successful retry'},
           {'input': {'balance': 5,
                      'actions': [{'op': 'withdraw', 'cents': 6}, {'op': 'withdraw', 'cents': 6}]},
            'expected': {'accepted': [False, False], 'balance': 5},
            'label': 'repeated failures'},
           {'input': {'balance': 0,
                      'actions': [{'op': 'deposit', 'cents': 1},
                                  {'op': 'deposit', 'cents': 2},
                                  {'op': 'deposit', 'cents': 3}]},
            'expected': {'accepted': [True, True, True], 'balance': 6},
            'label': 'repeated deposits'},
           {'input': {'balance': 1000000000000,
                      'actions': [{'op': 'withdraw', 'cents': 1}, {'op': 'deposit', 'cents': 2}]},
            'expected': {'accepted': [True, True], 'balance': 1000000000001},
            'label': 'large exact balance'},
           {'input': {'balance': 3,
                      'actions': [{'op': 'withdraw', 'cents': 1},
                                  {'op': 'withdraw', 'cents': 1},
                                  {'op': 'withdraw', 'cents': 1},
                                  {'op': 'withdraw', 'cents': 1}]},
            'expected': {'accepted': [True, True, True, False], 'balance': 0},
            'label': 'depletion across operations'}],
 'generated': [{'balance': 20,
                'actions': [{'op': 'withdraw', 'cents': 21},
                            {'op': 'withdraw', 'cents': 20},
                            {'op': 'deposit', 'cents': 0},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 21,
                'actions': [{'op': 'withdraw', 'cents': 22},
                            {'op': 'withdraw', 'cents': 21},
                            {'op': 'deposit', 'cents': 1},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 22,
                'actions': [{'op': 'withdraw', 'cents': 23},
                            {'op': 'withdraw', 'cents': 22},
                            {'op': 'deposit', 'cents': 2},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 23,
                'actions': [{'op': 'withdraw', 'cents': 24},
                            {'op': 'withdraw', 'cents': 23},
                            {'op': 'deposit', 'cents': 3},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 24,
                'actions': [{'op': 'withdraw', 'cents': 25},
                            {'op': 'withdraw', 'cents': 24},
                            {'op': 'deposit', 'cents': 4},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 25,
                'actions': [{'op': 'withdraw', 'cents': 26},
                            {'op': 'withdraw', 'cents': 25},
                            {'op': 'deposit', 'cents': 5},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 26,
                'actions': [{'op': 'withdraw', 'cents': 27},
                            {'op': 'withdraw', 'cents': 26},
                            {'op': 'deposit', 'cents': 6},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 27,
                'actions': [{'op': 'withdraw', 'cents': 28},
                            {'op': 'withdraw', 'cents': 27},
                            {'op': 'deposit', 'cents': 7},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 28,
                'actions': [{'op': 'withdraw', 'cents': 29},
                            {'op': 'withdraw', 'cents': 28},
                            {'op': 'deposit', 'cents': 8},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 29,
                'actions': [{'op': 'withdraw', 'cents': 30},
                            {'op': 'withdraw', 'cents': 29},
                            {'op': 'deposit', 'cents': 9},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 30,
                'actions': [{'op': 'withdraw', 'cents': 31},
                            {'op': 'withdraw', 'cents': 30},
                            {'op': 'deposit', 'cents': 10},
                            {'op': 'withdraw', 'cents': 0}]},
               {'balance': 31,
                'actions': [{'op': 'withdraw', 'cents': 32},
                            {'op': 'withdraw', 'cents': 31},
                            {'op': 'deposit', 'cents': 11},
                            {'op': 'withdraw', 'cents': 0}]}],
 'mutations': [{'name': 'rejects an exact-balance withdrawal',
                'old': 'if cents > self._balance:',
                'new': 'if cents >= self._balance:'}],
 'sources': ['https://docs.python.org/3.11/tutorial/classes.html#private-variables',
             'https://docs.python.org/3.11/library/functions.html#property']}
