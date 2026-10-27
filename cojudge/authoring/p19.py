"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 19,
 'slug': 'exact-partial-refunds',
 'title': 'Cap partial refunds with exact cents',
 'difficulty': 'Medium',
 'time': 25,
 'prerequisites': 'Integer cents, dataclasses, and account invariants.',
 'learn': 'A payment can have several partial refunds. The limit applies to their cumulative '
          'total, not to each request in isolation. Store the original charge and the refunded '
          'amount, or store a remaining refundable amount. Integer cents keep every subtraction '
          'exact. Validate a request before changing state so a failed refund cannot reduce the '
          'remaining amount. Keep each payment’s state separate. A request for the exact remaining '
          'amount is valid and leaves zero. This exercise also permits zero-cent requests, which '
          'succeed without changing the amount. Real refund systems need additional rules for '
          'request IDs and external settlement; this task isolates the cumulative amount '
          'invariant.',
 'scenario': ('An online store allows partial refunds. The total refunded for a payment must never be more than the amount charged. `solve` processes refund requests in order and tracks how much each payment can still refund.'),
 'example_notes': ['A refund of 30 leaves 70. 80 is too much, so it is rejected. 70 is accepted and leaves 0.', 'Each payment has its own remaining amount.', 'No payments.'],
 'task': ('**Input:** `data` has:\n'
    '- `payments`: maps payment IDs to charged cents (nonnegative integers).\n'
    '- `refunds`: a list of `{"payment": string, "cents": int}`, with nonnegative `cents`. Every payment ID exists.\n'
    '\n'
    '**Rules:** process the refunds in order.\n'
    "- Accept a refund when `cents` is at most the payment's remaining refundable cents. Subtract only accepted refunds.\n"
    '- A zero-cent refund is accepted, also after a full refund.\n'
    '\n'
    '**Return** `{"accepted": [bool], "remaining": {payment_id: int}}`\n'
    '- `accepted`: one boolean per refund.\n'
    '- `remaining`: the remaining refundable cents of every payment, including payments with no refund requests.'),
 'constraints': ['At most 30 payments and 100 refund requests. Charged and requested cents are at '
                 'most 1,000,000,000,000.'],
 'hints': ['Compare with the remaining amount, not the original charge.',
           'Update the refunded amount only after the request passes.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'from dataclasses import dataclass\n'
              '\n'
              '@dataclass\n'
              'class Payment:\n'
              '    charged: int\n'
              '    refunded: int = 0\n'
              '\n'
              '    @property\n'
              '    def remaining(self) -> int:\n'
              '        return self.charged - self.refunded\n'
              '\n'
              '    def refund(self, cents: int) -> bool:\n'
              '        if cents > self.remaining:\n'
              '            return False\n'
              '        self.refunded += cents\n'
              '        return True\n'
              '\n'
              'def solve(data: dict) -> dict:\n'
              "    payments = {key: Payment(cents) for key, cents in data['payments'].items()}\n"
              "    accepted = [payments[r['payment']].refund(r['cents']) for r in "
              "data['refunds']]\n"
              "    return {'accepted': accepted, 'remaining': {key: p.remaining for key, p in "
              'payments.items()}}\n',
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    Map<String,Long> remaining=new LinkedHashMap<>();for(Map.Entry<String,Object> '
         'e:obj(d.get("payments")).entrySet())remaining.put(e.getKey(),lng(e.getValue()));\n'
         '    List<Object> accepted=new ArrayList<>();for(Object '
         'x:arr(d.get("refunds"))){Map<String,Object> r=obj(x);String id=s(r.get("payment"));long '
         'amount=lng(r.get("cents"));boolean '
         'ok=amount<=remaining.get(id);accepted.add(ok);if(ok)remaining.put(id,remaining.get(id)-amount);}\n'
         '    return map("accepted",accepted,"remaining",remaining);\n'
         '}',
 'approach': 'The reference gives each payment a dataclass with a cumulative refunded amount and a '
             'derived remaining property. Time is O(p + r), and space is O(p + r), for p payments '
             'and r requests. The judge checks arithmetic and isolation, not dataclass use. No '
             'request deduplication, remote payment processing, or settlement occurs.',
 'cases': [{'input': {'payments': {'p': 100},
                      'refunds': [{'payment': 'p', 'cents': 30},
                                  {'payment': 'p', 'cents': 80},
                                  {'payment': 'p', 'cents': 70}]},
            'expected': {'accepted': [True, False, True], 'remaining': {'p': 0}},
            'label': 'cumulative cap and failure preservation'},
           {'input': {'payments': {'a': 50, 'b': 20},
                      'refunds': [{'payment': 'b', 'cents': 20}, {'payment': 'a', 'cents': 10}]},
            'expected': {'accepted': [True, True], 'remaining': {'a': 40, 'b': 0}},
            'label': 'separate payment state'},
           {'input': {'payments': {}, 'refunds': []},
            'expected': {'accepted': [], 'remaining': {}},
            'label': 'no payments'},
           {'input': {'payments': {'a': 12, 'b': 0}, 'refunds': []},
            'expected': {'accepted': [], 'remaining': {'a': 12, 'b': 0}},
            'label': 'unrefunded payments remain'},
           {'input': {'payments': {'a': 0},
                      'refunds': [{'payment': 'a', 'cents': 0}, {'payment': 'a', 'cents': 1}]},
            'expected': {'accepted': [True, False], 'remaining': {'a': 0}},
            'label': 'zero charge'},
           {'input': {'payments': {'a': 1}, 'refunds': [{'payment': 'a', 'cents': 1}]},
            'expected': {'accepted': [True], 'remaining': {'a': 0}},
            'label': 'one-cent full refund'},
           {'input': {'payments': {'a': 10}, 'refunds': [{'payment': 'a', 'cents': 11}]},
            'expected': {'accepted': [False], 'remaining': {'a': 10}},
            'label': 'request exceeds original charge'},
           {'input': {'payments': {'a': 10},
                      'refunds': [{'payment': 'a', 'cents': 10},
                                  {'payment': 'a', 'cents': 10},
                                  {'payment': 'a', 'cents': 0}]},
            'expected': {'accepted': [True, False, True], 'remaining': {'a': 0}},
            'label': 'repeated full refund and zero'},
           {'input': {'payments': {'a': 3},
                      'refunds': [{'payment': 'a', 'cents': 1},
                                  {'payment': 'a', 'cents': 1},
                                  {'payment': 'a', 'cents': 1},
                                  {'payment': 'a', 'cents': 1}]},
            'expected': {'accepted': [True, True, True, False], 'remaining': {'a': 0}},
            'label': 'small cumulative refunds'},
           {'input': {'payments': {'a': 29},
                      'refunds': [{'payment': 'a', 'cents': 10}, {'payment': 'a', 'cents': 19}]},
            'expected': {'accepted': [True, True], 'remaining': {'a': 0}},
            'label': 'exact cents avoid floating error'},
           {'input': {'payments': {'a': 1000000000000},
                      'refunds': [{'payment': 'a', 'cents': 999999999999},
                                  {'payment': 'a', 'cents': 1}]},
            'expected': {'accepted': [True, True], 'remaining': {'a': 0}},
            'label': 'large exact remaining amount'},
           {'input': {'payments': {'a': 5, 'b': 5},
                      'refunds': [{'payment': 'a', 'cents': 5},
                                  {'payment': 'b', 'cents': 6},
                                  {'payment': 'b', 'cents': 5}]},
            'expected': {'accepted': [True, False, True], 'remaining': {'a': 0, 'b': 0}},
            'label': 'rejected payment does not affect another'}],
 'generated': [{'payments': {'p': 20, 'q': 0},
                'refunds': [{'payment': 'p', 'cents': 1},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 0},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 21, 'q': 1},
                'refunds': [{'payment': 'p', 'cents': 2},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 1},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 22, 'q': 2},
                'refunds': [{'payment': 'p', 'cents': 3},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 2},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 23, 'q': 3},
                'refunds': [{'payment': 'p', 'cents': 4},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 3},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 24, 'q': 4},
                'refunds': [{'payment': 'p', 'cents': 5},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 4},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 25, 'q': 5},
                'refunds': [{'payment': 'p', 'cents': 6},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 5},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 26, 'q': 6},
                'refunds': [{'payment': 'p', 'cents': 7},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 6},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 27, 'q': 7},
                'refunds': [{'payment': 'p', 'cents': 8},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 7},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 28, 'q': 8},
                'refunds': [{'payment': 'p', 'cents': 9},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 8},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 29, 'q': 9},
                'refunds': [{'payment': 'p', 'cents': 10},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 9},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 30, 'q': 10},
                'refunds': [{'payment': 'p', 'cents': 11},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 10},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]},
               {'payments': {'p': 31, 'q': 11},
                'refunds': [{'payment': 'p', 'cents': 12},
                            {'payment': 'p', 'cents': 20},
                            {'payment': 'q', 'cents': 11},
                            {'payment': 'p', 'cents': 19},
                            {'payment': 'q', 'cents': 0}]}],
 'mutations': [{'name': 'compares each refund only with original charge',
                'old': 'if cents > self.remaining:',
                'new': 'if cents > self.charged:'}],
 'sources': ['https://docs.python.org/3.11/library/dataclasses.html',
             'https://docs.python.org/3.11/library/stdtypes.html#numeric-types-int-float-complex']}
