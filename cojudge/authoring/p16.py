"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 16,
 'slug': 'explicit-order-states',
 'title': 'Model explicit order transitions',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Classes, dictionaries, and stateful operations.',
 'learn': 'A state machine lists which actions are valid in each state. It separates the current '
          'state from the events that request a change. A transition table makes the allowed paths '
          'easy to inspect. An action that has no transition must leave the state unchanged. This '
          'matters when events repeat or arrive in the wrong order. Do not assume that every event '
          'moves the process forward. Terminal states may have no valid outgoing actions. This '
          'exercise models one order with a small set of named states. It uses a boolean result '
          'for each request so a caller can see exactly which requests were accepted.',
 'task': ('**Input:** `data` has:\n'
    '- `actions`: a list of strings. Each is `authorize`, `capture`, `cancel`, or `refund`.\n'
    '\n'
    '**Rules:** the order starts in `NEW`. Only these transitions are allowed:\n'
    '\n'
    '| State | Action | New state |\n'
    '| --- | --- | --- |\n'
    '| NEW | authorize | AUTHORIZED |\n'
    '| NEW | cancel | CANCELLED |\n'
    '| AUTHORIZED | capture | CAPTURED |\n'
    '| AUTHORIZED | cancel | CANCELLED |\n'
    '| CAPTURED | refund | REFUNDED |\n'
    '\n'
    'Any other action is rejected (`false`) and does not change the state. `CANCELLED` and `REFUNDED` are final states.\n'
    '\n'
    '**Return** `{"accepted": [bool], "state": string}`: one boolean per action, and the final state.'),
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['Use the pair of current state and action as a lookup key.',
           'Change state only when that lookup has a result.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'class Order:\n'
              '    TRANSITIONS = {\n'
              "        ('NEW', 'authorize'): 'AUTHORIZED',\n"
              "        ('NEW', 'cancel'): 'CANCELLED',\n"
              "        ('AUTHORIZED', 'capture'): 'CAPTURED',\n"
              "        ('AUTHORIZED', 'cancel'): 'CANCELLED',\n"
              "        ('CAPTURED', 'refund'): 'REFUNDED',\n"
              '    }\n'
              '\n'
              '    def __init__(self):\n'
              "        self.state = 'NEW'\n"
              '\n'
              '    def apply(self, action: str) -> bool:\n'
              '        next_state = self.TRANSITIONS.get((self.state, action))\n'
              '        if next_state is None:\n'
              '            return False\n'
              '        self.state = next_state\n'
              '        return True\n'
              '\n'
              'def solve(data: dict) -> dict:\n'
              '    order = Order()\n'
              "    accepted = [order.apply(action) for action in data['actions']]\n"
              "    return {'accepted': accepted, 'state': order.state}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    String state="NEW"; List<Object> accepted=new ArrayList<>();\n'
         '    for(Object x:arr(d.get("actions"))) { String action=s(x),next=null;\n'
         '        if(state.equals("NEW")) {if(action.equals("authorize"))next="AUTHORIZED";else '
         'if(action.equals("cancel"))next="CANCELLED";}\n'
         '        else if(state.equals("AUTHORIZED")) '
         '{if(action.equals("capture"))next="CAPTURED";else '
         'if(action.equals("cancel"))next="CANCELLED";}\n'
         '        else if(state.equals("CAPTURED") && action.equals("refund")) next="REFUNDED";\n'
         '        accepted.add(next!=null); if(next!=null)state=next;\n'
         '    }\n'
         '    return map("accepted",accepted,"state",state);\n'
         '}',
 'approach': 'The reference stores allowed transitions in a dictionary. Each action takes expected '
             'O(1) time; total time and output space are O(n). The judge checks transition '
             'behavior, not table use. This is a deterministic simulation. It does not test '
             'concurrent state changes or persistence.',
 'cases': [{'input': {'actions': ['authorize', 'capture', 'refund']},
            'expected': {'accepted': [True, True, True], 'state': 'REFUNDED'},
            'label': 'complete valid path'},
           {'input': {'actions': ['capture', 'authorize', 'authorize', 'capture']},
            'expected': {'accepted': [False, True, False, True], 'state': 'CAPTURED'},
            'label': 'invalid order and repeated action'},
           {'input': {'actions': []},
            'expected': {'accepted': [], 'state': 'NEW'},
            'label': 'no events'},
           {'input': {'actions': ['authorize']},
            'expected': {'accepted': [True], 'state': 'AUTHORIZED'},
            'label': 'first transition'},
           {'input': {'actions': ['cancel']},
            'expected': {'accepted': [True], 'state': 'CANCELLED'},
            'label': 'cancel new order'},
           {'input': {'actions': ['refund']},
            'expected': {'accepted': [False], 'state': 'NEW'},
            'label': 'cannot refund new order'},
           {'input': {'actions': ['authorize', 'cancel']},
            'expected': {'accepted': [True, True], 'state': 'CANCELLED'},
            'label': 'cancel authorized order'},
           {'input': {'actions': ['authorize', 'refund']},
            'expected': {'accepted': [True, False], 'state': 'AUTHORIZED'},
            'label': 'capture must precede refund'},
           {'input': {'actions': ['authorize', 'capture', 'cancel']},
            'expected': {'accepted': [True, True, False], 'state': 'CAPTURED'},
            'label': 'captured order cannot cancel'},
           {'input': {'actions': ['cancel', 'authorize', 'capture', 'cancel', 'refund']},
            'expected': {'accepted': [True, False, False, False, False], 'state': 'CANCELLED'},
            'label': 'cancelled is terminal'},
           {'input': {'actions': ['authorize', 'capture', 'refund', 'refund', 'authorize']},
            'expected': {'accepted': [True, True, True, False, False], 'state': 'REFUNDED'},
            'label': 'refunded is terminal'},
           {'input': {'actions': ['capture', 'capture', 'refund', 'cancel']},
            'expected': {'accepted': [False, False, False, True], 'state': 'CANCELLED'},
            'label': 'invalid events preserve new state'}],
 'generated': [{'actions': ['capture', 'authorize', 'capture', 'refund']},
               {'actions': ['capture',
                            'capture',
                            'authorize',
                            'refund',
                            'capture',
                            'cancel',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'authorize',
                            'refund',
                            'refund',
                            'capture',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'capture',
                            'authorize',
                            'capture',
                            'cancel',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'authorize',
                            'refund',
                            'capture',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'authorize',
                            'refund',
                            'refund',
                            'capture',
                            'cancel',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'authorize',
                            'capture',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'authorize',
                            'refund',
                            'capture',
                            'cancel',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'authorize',
                            'refund',
                            'refund',
                            'capture',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'authorize',
                            'capture',
                            'cancel',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'authorize',
                            'refund',
                            'capture',
                            'refund']},
               {'actions': ['capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'capture',
                            'authorize',
                            'refund',
                            'refund',
                            'capture',
                            'cancel',
                            'refund']}],
 'mutations': [{'name': 'allows cancel after capture',
                'old': "('CAPTURED', 'refund'): 'REFUNDED',",
                'new': "('CAPTURED', 'refund'): 'REFUNDED',\n"
                       "        ('CAPTURED', 'cancel'): 'CANCELLED',"}],
 'sources': ['https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict']}
