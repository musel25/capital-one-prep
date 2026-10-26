"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 15,
 'slug': 'composed-fee-protocol',
 'title': 'Compose a calculator with a fee policy',
 'difficulty': 'Medium',
 'time': 25,
 'prerequisites': 'Classes, type annotations, and integer arithmetic.',
 'learn': 'Composition gives an object another object that performs part of its work. A small '
          'protocol describes the methods that the dependency must provide. Python Protocol '
          'supports structural typing: a class can satisfy the interface without explicitly '
          'inheriting from it. A calculator can depend on fee(amount) instead of checking policy '
          'types for every amount. Select the policy once at the boundary, then let the calculator '
          'call it. This is polymorphism through a shared interface. Integer arithmetic can also '
          'make a percentage fee exact. To round a nonnegative integer fraction upward, add '
          'denominator minus one before integer division.',
 'task': '`data.policy` is either `{"kind":"flat","cents":nonnegative_integer}` or '
         '`{"kind":"rate","bps":integer_from_0_to_10000}`. `data.amounts` is a list of nonnegative '
         'integer cent amounts. One basis point is 1/100 of one percent. Flat fee equals `cents`, '
         'including for amount zero. Rate fee is amount × bps / 10000, rounded upward to whole '
         'cents. Return a list of `{"fee": integer, "total": amount_plus_fee}` in input order. '
         'Practice Protocol and composition; the judge checks outputs only.',
 'constraints': ['At most 100 amounts. Cent values are at most 1,000,000,000,000.'],
 'hints': ['Each policy can implement the same fee method.',
           'Keep integer cents throughout the percentage calculation.'],
 'starter': 'def solve(data: dict) -> list[dict]:\n    raise NotImplementedError\n',
 'reference': 'from dataclasses import dataclass\n'
              'from typing import Protocol\n'
              '\n'
              'class FeePolicy(Protocol):\n'
              '    def fee(self, amount: int) -> int: ...\n'
              '\n'
              '@dataclass\n'
              'class FlatFee:\n'
              '    cents: int\n'
              '    def fee(self, amount: int) -> int:\n'
              '        return self.cents\n'
              '\n'
              '@dataclass\n'
              'class RateFee:\n'
              '    bps: int\n'
              '    def fee(self, amount: int) -> int:\n'
              '        return (amount * self.bps + 9999) // 10000\n'
              '\n'
              'class Calculator:\n'
              '    def __init__(self, policy: FeePolicy):\n'
              '        self.policy = policy\n'
              '    def quote(self, amount: int) -> dict:\n'
              '        fee = self.policy.fee(amount)\n'
              "        return {'fee': fee, 'total': amount + fee}\n"
              '\n'
              'def solve(data: dict) -> list[dict]:\n'
              "    raw = data['policy']\n"
              "    policy: FeePolicy = FlatFee(raw['cents']) if raw['kind'] == 'flat' else "
              "RateFee(raw['bps'])\n"
              '    calculator = Calculator(policy)\n'
              "    return [calculator.quote(amount) for amount in data['amounts']]\n",
 'java': 'interface FeeRule {long fee(long amount);}\n'
         'static class FixedRule implements FeeRule {long cents; FixedRule(long c){cents=c;} '
         'public long fee(long amount){return cents;}}\n'
         'static class PercentRule implements FeeRule {long bps; PercentRule(long b){bps=b;} '
         'public long fee(long amount){long numerator=amount*bps;return '
         'numerator/10000+(numerator%10000==0?0:1);}}\n'
         'public Object solve(Map<String,Object> d) {\n'
         '    Map<String,Object> p=obj(d.get("policy")); FeeRule '
         'rule=s(p.get("kind")).equals("flat")?new FixedRule(lng(p.get("cents"))):new '
         'PercentRule(lng(p.get("bps")));\n'
         '    List<Object> out=new ArrayList<>(); for(Object x:arr(d.get("amounts"))) {long '
         'amount=lng(x),fee=rule.fee(amount);out.add(map("fee",fee,"total",amount+fee));}return '
         'out;\n'
         '}',
 'approach': 'The reference uses a Protocol, two policy classes, and a Calculator that holds a '
             'policy. It selects the policy once. Time is O(n), and result space is O(n). The '
             'output judge verifies fee calculations, not Protocol, composition, or polymorphism. '
             'The policy is a constructed exercise, not a pricing recommendation.',
 'cases': [{'input': {'policy': {'kind': 'flat', 'cents': 3}, 'amounts': [0, 10]},
            'expected': [{'fee': 3, 'total': 3}, {'fee': 3, 'total': 13}],
            'label': 'flat fee includes zero amount'},
           {'input': {'policy': {'kind': 'rate', 'bps': 250}, 'amounts': [100, 200, 1]},
            'expected': [{'fee': 3, 'total': 103},
                         {'fee': 5, 'total': 205},
                         {'fee': 1, 'total': 2}],
            'label': 'rate fees round upward'},
           {'input': {'policy': {'kind': 'rate', 'bps': 10}, 'amounts': []},
            'expected': [],
            'label': 'no quotes'},
           {'input': {'policy': {'kind': 'flat', 'cents': 0}, 'amounts': [0, 5]},
            'expected': [{'fee': 0, 'total': 0}, {'fee': 0, 'total': 5}],
            'label': 'zero flat fee'},
           {'input': {'policy': {'kind': 'rate', 'bps': 0}, 'amounts': [0, 1000000]},
            'expected': [{'fee': 0, 'total': 0}, {'fee': 0, 'total': 1000000}],
            'label': 'zero rate'},
           {'input': {'policy': {'kind': 'rate', 'bps': 10000}, 'amounts': [1, 99]},
            'expected': [{'fee': 1, 'total': 2}, {'fee': 99, 'total': 198}],
            'label': 'full rate'},
           {'input': {'policy': {'kind': 'rate', 'bps': 1}, 'amounts': [1, 9999, 10000, 10001]},
            'expected': [{'fee': 1, 'total': 2},
                         {'fee': 1, 'total': 10000},
                         {'fee': 1, 'total': 10001},
                         {'fee': 2, 'total': 10003}],
            'label': 'one basis point boundaries'},
           {'input': {'policy': {'kind': 'rate', 'bps': 9999}, 'amounts': [0, 1]},
            'expected': [{'fee': 0, 'total': 0}, {'fee': 1, 'total': 2}],
            'label': 'zero amount at high rate'},
           {'input': {'policy': {'kind': 'flat', 'cents': 2}, 'amounts': [3, 3, 3]},
            'expected': [{'fee': 2, 'total': 5}, {'fee': 2, 'total': 5}, {'fee': 2, 'total': 5}],
            'label': 'repeated quotes'},
           {'input': {'policy': {'kind': 'rate', 'bps': 5000}, 'amounts': [1, 2, 3]},
            'expected': [{'fee': 1, 'total': 2}, {'fee': 1, 'total': 3}, {'fee': 2, 'total': 5}],
            'label': 'half-cent rounds upward'},
           {'input': {'policy': {'kind': 'rate', 'bps': 123}, 'amounts': [1000000000000]},
            'expected': [{'fee': 12300000000, 'total': 1012300000000}],
            'label': 'large integer arithmetic'},
           {'input': {'policy': {'kind': 'flat', 'cents': 1000000000000},
                      'amounts': [1000000000000]},
            'expected': [{'fee': 1000000000000, 'total': 2000000000000}],
            'label': 'large flat fee'},
           {'input': {'policy': {'kind': 'flat', 'cents': 7}, 'amounts': []},
            'expected': [],
            'label': 'unused policy'}],
 'generated': [{'policy': {'kind': 'rate', 'bps': 1}, 'amounts': [0, 10000, 10000, 1]},
               {'policy': {'kind': 'rate', 'bps': 138}, 'amounts': [1, 9999, 10001, 101]},
               {'policy': {'kind': 'rate', 'bps': 275}, 'amounts': [2, 9998, 10002, 201]},
               {'policy': {'kind': 'rate', 'bps': 412}, 'amounts': [3, 9997, 10003, 301]},
               {'policy': {'kind': 'rate', 'bps': 549}, 'amounts': [4, 9996, 10004, 401]},
               {'policy': {'kind': 'rate', 'bps': 686}, 'amounts': [5, 9995, 10005, 501]},
               {'policy': {'kind': 'rate', 'bps': 823}, 'amounts': [6, 9994, 10006, 601]},
               {'policy': {'kind': 'rate', 'bps': 960}, 'amounts': [7, 9993, 10007, 701]},
               {'policy': {'kind': 'rate', 'bps': 1097}, 'amounts': [8, 9992, 10008, 801]},
               {'policy': {'kind': 'rate', 'bps': 1234}, 'amounts': [9, 9991, 10009, 901]},
               {'policy': {'kind': 'rate', 'bps': 1371}, 'amounts': [10, 9990, 10010, 1001]},
               {'policy': {'kind': 'rate', 'bps': 1508}, 'amounts': [11, 9989, 10011, 1101]}],
 'mutations': [{'name': 'rounds rate fees down',
                'old': 'amount * self.bps + 9999',
                'new': 'amount * self.bps'}],
 'sources': ['https://docs.python.org/3.11/library/typing.html#typing.Protocol']}
