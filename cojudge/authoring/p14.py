"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 14,
 'slug': 'inheritance-fee-policy',
 'title': 'Extend an account with a fee rule',
 'difficulty': 'Medium',
 'time': 25,
 'prerequisites': 'Classes and the balance invariant exercise.',
 'learn': 'Inheritance lets a subclass reuse a base implementation while replacing a specific '
          'behavior. A subclass initializer can call super().__init__ to establish the base state '
          'before adding its own fields. A base method can call another instance method such as '
          'withdrawal_fee. Python then selects the override on the actual object. This keeps the '
          'withdrawal check in one place while allowing a premium account to use a different fee '
          'rule. Avoid copying the whole withdrawal method just to change one calculation. Both '
          'amount and fee must fit in the balance. A rejected operation must charge neither of '
          'them.',
 'scenario': ('A bank has standard and premium checking accounts. Each ATM withdrawal costs a fee, but premium customers pay no fee for large withdrawals (at least `threshold`). The fee is part of the withdrawal, so the account must have enough money for both.'),
 'example_notes': ['Standard: 10 + 2 = 12 leaves 8. Then 8 + 2 = 10 is more than 8, so it is rejected.', 'Premium: 10 is at the threshold, so there is no fee and 10 remains. Then 8 + 2 = 10 leaves 0.', 'No withdrawals.'],
 'task': ('**Input:** `data` has (all amounts in cents):\n'
    '- `kind`: `"standard"` or `"premium"`.\n'
    '- `balance`, `fee`, `threshold`: nonnegative integers.\n'
    '- `withdrawals`: a list of positive integers.\n'
    '\n'
    '**Rules:** for each withdrawal amount, in order:\n'
    '- The fee: a standard account charges `fee`. A premium account charges 0 when the amount is at least `threshold`, otherwise `fee`.\n'
    '- The withdrawal succeeds when amount + fee is at most the current balance. Subtract amount + fee.\n'
    '- A failed withdrawal changes nothing.\n'
    '\n'
    '**Return** `{"accepted": [bool], "balance": int}`: one boolean per withdrawal, and the final balance.\n'
    '\n'
    '**Practice:** use inheritance, `super()`, and a fee method override. The judge checks only the output.'),
 'constraints': ['At most 100 withdrawals. Numeric input values are at most 1,000,000,000,000.'],
 'hints': ['Let the base withdrawal method call a fee method.',
           'Initialize base fields with super(), then store the premium threshold.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'class Account:\n'
              '    def __init__(self, balance: int, fee: int):\n'
              '        self.balance = balance\n'
              '        self.fee = fee\n'
              '\n'
              '    def withdrawal_fee(self, amount: int) -> int:\n'
              '        return self.fee\n'
              '\n'
              '    def withdraw(self, amount: int) -> bool:\n'
              '        total = amount + self.withdrawal_fee(amount)\n'
              '        if total > self.balance:\n'
              '            return False\n'
              '        self.balance -= total\n'
              '        return True\n'
              '\n'
              'class PremiumAccount(Account):\n'
              '    def __init__(self, balance: int, fee: int, threshold: int):\n'
              '        super().__init__(balance, fee)\n'
              '        self.threshold = threshold\n'
              '\n'
              '    def withdrawal_fee(self, amount: int) -> int:\n'
              '        return 0 if amount >= self.threshold else super().withdrawal_fee(amount)\n'
              '\n'
              'def solve(data: dict) -> dict:\n'
              "    account = (PremiumAccount(data['balance'], data['fee'], data['threshold'])\n"
              "               if data['kind'] == 'premium' else Account(data['balance'], "
              "data['fee']))\n"
              "    accepted = [account.withdraw(amount) for amount in data['withdrawals']]\n"
              "    return {'accepted': accepted, 'balance': account.balance}\n",
 'java': 'static class FeeAccount {\n'
         '    long balance,fee; FeeAccount(long b,long f) {balance=b;fee=f;}\n'
         '    long charge(long amount) {return fee;}\n'
         '    boolean withdraw(long amount) {long total=amount+charge(amount); '
         'if(total>balance)return false;balance-=total;return true;}\n'
         '}\n'
         'static class PremiumFeeAccount extends FeeAccount {\n'
         '    long threshold; PremiumFeeAccount(long b,long f,long t) {super(b,f);threshold=t;}\n'
         '    long charge(long amount) {return amount>=threshold?0:super.charge(amount);}\n'
         '}\n'
         'public Object solve(Map<String,Object> d) {\n'
         '    FeeAccount account=s(d.get("kind")).equals("premium")?new '
         'PremiumFeeAccount(lng(d.get("balance")),lng(d.get("fee")),lng(d.get("threshold"))):new '
         'FeeAccount(lng(d.get("balance")),lng(d.get("fee")));\n'
         '    List<Object> accepted=new ArrayList<>(); for(Object a:arr(d.get("withdrawals"))) '
         'accepted.add(account.withdraw(lng(a))); return '
         'map("accepted",accepted,"balance",account.balance);\n'
         '}',
 'approach': 'The Python reference uses a base account, a subclass initializer with super(), and '
             'an overridden fee method. Each withdrawal is O(1); total time and output space are '
             'O(n). The output judge cannot certify inheritance or constructor design. This is a '
             'constructed fee model, not a real bank policy.',
 'cases': [{'input': {'kind': 'standard',
                      'balance': 20,
                      'fee': 2,
                      'threshold': 10,
                      'withdrawals': [10, 8]},
            'expected': {'accepted': [True, False], 'balance': 8},
            'label': 'fee is part of the funds check'},
           {'input': {'kind': 'premium',
                      'balance': 20,
                      'fee': 2,
                      'threshold': 10,
                      'withdrawals': [10, 8]},
            'expected': {'accepted': [True, True], 'balance': 0},
            'label': 'premium fee override'},
           {'input': {'kind': 'premium',
                      'balance': 10,
                      'fee': 3,
                      'threshold': 10,
                      'withdrawals': []},
            'expected': {'accepted': [], 'balance': 10},
            'label': 'no withdrawals'},
           {'input': {'kind': 'standard',
                      'balance': 0,
                      'fee': 0,
                      'threshold': 0,
                      'withdrawals': [1]},
            'expected': {'accepted': [False], 'balance': 0},
            'label': 'empty account'},
           {'input': {'kind': 'premium',
                      'balance': 10,
                      'fee': 3,
                      'threshold': 10,
                      'withdrawals': [10]},
            'expected': {'accepted': [True], 'balance': 0},
            'label': 'threshold equality waives fee'},
           {'input': {'kind': 'premium',
                      'balance': 10,
                      'fee': 3,
                      'threshold': 10,
                      'withdrawals': [9]},
            'expected': {'accepted': [False], 'balance': 10},
            'label': 'below threshold still pays fee'},
           {'input': {'kind': 'standard',
                      'balance': 12,
                      'fee': 2,
                      'threshold': 0,
                      'withdrawals': [10]},
            'expected': {'accepted': [True], 'balance': 0},
            'label': 'exact amount plus fee'},
           {'input': {'kind': 'premium',
                      'balance': 5,
                      'fee': 100,
                      'threshold': 0,
                      'withdrawals': [5]},
            'expected': {'accepted': [True], 'balance': 0},
            'label': 'zero threshold'},
           {'input': {'kind': 'standard',
                      'balance': 10,
                      'fee': 0,
                      'threshold': 100,
                      'withdrawals': [5, 5]},
            'expected': {'accepted': [True, True], 'balance': 0},
            'label': 'zero fee'},
           {'input': {'kind': 'premium',
                      'balance': 10,
                      'fee': 1,
                      'threshold': 100,
                      'withdrawals': [11, 9]},
            'expected': {'accepted': [False, True], 'balance': 0},
            'label': 'failure charges nothing'},
           {'input': {'kind': 'standard',
                      'balance': 10,
                      'fee': 1,
                      'threshold': 1,
                      'withdrawals': [10, 9]},
            'expected': {'accepted': [False, True], 'balance': 0},
            'label': 'standard ignores threshold'},
           {'input': {'kind': 'premium',
                      'balance': 30,
                      'fee': 2,
                      'threshold': 10,
                      'withdrawals': [5, 10, 5]},
            'expected': {'accepted': [True, True, True], 'balance': 6},
            'label': 'mixed waived and charged fees'},
           {'input': {'kind': 'premium',
                      'balance': 1000000000000,
                      'fee': 10,
                      'threshold': 1000000000000,
                      'withdrawals': [1000000000000]},
            'expected': {'accepted': [True], 'balance': 0},
            'label': 'large threshold boundary'}],
 'generated': [{'kind': 'standard',
                'balance': 30,
                'fee': 0,
                'threshold': 5,
                'withdrawals': [4, 5, 20, 1]},
               {'kind': 'premium',
                'balance': 37,
                'fee': 1,
                'threshold': 6,
                'withdrawals': [5, 6, 21, 1]},
               {'kind': 'standard',
                'balance': 44,
                'fee': 2,
                'threshold': 7,
                'withdrawals': [6, 7, 22, 1]},
               {'kind': 'premium',
                'balance': 51,
                'fee': 3,
                'threshold': 8,
                'withdrawals': [7, 8, 23, 1]},
               {'kind': 'standard',
                'balance': 58,
                'fee': 0,
                'threshold': 9,
                'withdrawals': [8, 9, 24, 1]},
               {'kind': 'premium',
                'balance': 65,
                'fee': 1,
                'threshold': 10,
                'withdrawals': [9, 10, 25, 1]},
               {'kind': 'standard',
                'balance': 72,
                'fee': 2,
                'threshold': 11,
                'withdrawals': [10, 11, 26, 1]},
               {'kind': 'premium',
                'balance': 79,
                'fee': 3,
                'threshold': 12,
                'withdrawals': [11, 12, 27, 1]},
               {'kind': 'standard',
                'balance': 86,
                'fee': 0,
                'threshold': 13,
                'withdrawals': [12, 13, 28, 1]},
               {'kind': 'premium',
                'balance': 93,
                'fee': 1,
                'threshold': 14,
                'withdrawals': [13, 14, 29, 1]},
               {'kind': 'standard',
                'balance': 100,
                'fee': 2,
                'threshold': 15,
                'withdrawals': [14, 15, 30, 1]},
               {'kind': 'premium',
                'balance': 107,
                'fee': 3,
                'threshold': 16,
                'withdrawals': [15, 16, 31, 1]}],
 'mutations': [{'name': 'excludes the waiver threshold',
                'old': 'amount >= self.threshold',
                'new': 'amount > self.threshold'}],
 'sources': ['https://docs.python.org/3.11/tutorial/classes.html#inheritance',
             'https://docs.python.org/3.11/library/functions.html#super']}
