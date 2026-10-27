"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 2,
 'slug': 'exact-money-parser',
 'title': 'Parse money into exact cents',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Lists, dictionaries, and functions.',
 'learn': 'Binary floating point cannot represent many decimal fractions exactly. Money from a '
          'text boundary is easier to handle with Decimal. First validate the allowed text format. '
          'Then construct Decimal from that text, multiply by 100, and convert the exact result to '
          'an integer. This order keeps the cents. Constructing Decimal from a float would '
          'preserve the float error. Format validation is a separate concern: Decimal accepts '
          'forms that an API might forbid, such as an exponent. This task permits one or two '
          'fractional digits and rejects every other text format. Once parsed, integer cents '
          'support exact addition and comparison.',
 'scenario': ('A bank\'s import tool reads amounts that people typed into a form, such as `"12.34"`. A float cannot store cents exactly, so the tool converts the text to an integer number of cents. Text that does not match the strict format becomes `null`, so the import can flag it for review.'),
 'example_notes': ['`"12.34"` is 1234 cents, `"-0.05"` is -5, and `"7"` is 700.', 'All three are invalid: three decimal places, a leading space, and a number instead of a string.', 'No amounts.'],
 'task': ('**Input:** `data` has:\n'
    '- `amounts`: a list of JSON values. Strings have at most 30 characters.\n'
    '\n'
    '**Rules**\n'
    '- A valid amount is a string that fully matches the ASCII pattern `-?[0-9]{1,12}(?:\\.[0-9]{1,2})?`: an optional `-`, 1–12 digits, then optionally `.` and 1–2 digits.\n'
    '- Leading zeros and negative zero are valid: `"007"` → `700`, `"-0"` → `0`.\n'
    '- Invalid: spaces, a leading `+`, exponent notation, Unicode digits, and every non-string value.\n'
    '- Convert each valid amount to exact integer cents: `"1.5"` → `150`, `"-0.05"` → `-5`.\n'
    '\n'
    '**Return** `{"cents": [...]}` with one entry per amount, in input order: the integer cents for a valid amount, or `null` for an invalid one.'),
 'constraints': ['At most 100 input items. All input values follow the stated contract.'],
 'hints': ['Validate text before calling Decimal.',
           'Multiply the Decimal value before converting it to int.'],
 'starter': 'def solve(data: dict) -> dict:\n    raise NotImplementedError\n',
 'reference': 'import re\n'
              'from decimal import Decimal\n'
              '\n'
              'def solve(data: dict) -> dict:\n'
              '    cents = []\n'
              "    for value in data['amounts']:\n"
              '        if isinstance(value, str) and '
              "re.fullmatch(r'-?[0-9]{1,12}(?:\\.[0-9]{1,2})?', value):\n"
              '            cents.append(int(Decimal(value) * 100))\n'
              '        else:\n'
              '            cents.append(None)\n'
              "    return {'cents': cents}\n",
 'java': 'public Object solve(Map<String,Object> d) {\n'
         '    List<Object> out=new ArrayList<>();\n'
         '    for(Object x:arr(d.get("amounts"))) {\n'
         '        if(x instanceof String && s(x).matches("-?[0-9]{1,12}(?:\\\\.[0-9]{1,2})?")) '
         'out.add(new BigDecimal(s(x)).multiply(BigDecimal.valueOf(100)).longValueExact());\n'
         '        else out.add(null);\n'
         '    }\n'
         '    return map("cents",out);\n'
         '}',
 'approach': 'The reference processes the input in one pass. Time is O(n), and result storage is '
             'O(n). The output judge checks results. It cannot prove the requested Python '
             'technique. This is an in-memory exercise; it does not provide storage or concurrency '
             'control.',
 'cases': [{'input': {'amounts': ['12.34', '-0.05', '7']},
            'expected': {'cents': [1234, -5, 700]},
            'label': 'exact decimal conversion'},
           {'input': {'amounts': ['1.234', ' 2.00', 2]},
            'expected': {'cents': [None, None, None]},
            'label': 'invalid forms'},
           {'input': {'amounts': []}, 'expected': {'cents': []}, 'label': 'empty input'},
           {'input': {'amounts': ['0', '-0', '-0.00']},
            'expected': {'cents': [0, 0, 0]},
            'label': 'signed zero'},
           {'input': {'amounts': ['1.2', '0.01']},
            'expected': {'cents': [120, 1]},
            'label': 'one and two fractional digits'},
           {'input': {'amounts': ['0002.30', '00']},
            'expected': {'cents': [230, 0]},
            'label': 'leading zeros'},
           {'input': {'amounts': ['+1', '1e2', 'NaN', 'Infinity']},
            'expected': {'cents': [None, None, None, None]},
            'label': 'decimal parser must be constrained'},
           {'input': {'amounts': ['.25', '2.', '']},
            'expected': {'cents': [None, None, None]},
            'label': 'missing required digits'},
           {'input': {'amounts': [None, True, False, 1.5, {}, []]},
            'expected': {'cents': [None, None, None, None, None, None]},
            'label': 'wrong JSON types'},
           {'input': {'amounts': ['999999999999.99', '-999999999999.99']},
            'expected': {'cents': [99999999999999, -99999999999999]},
            'label': 'large exact values'},
           {'input': {'amounts': ['1\n', '1\t', '١.٢٣']},
            'expected': {'cents': [None, None, None]},
            'label': 'whole ASCII string only'},
           {'input': {'amounts': ['0.29', '0.58', '-1.99']},
            'expected': {'cents': [29, 58, -199]},
            'label': 'binary float traps'},
           {'input': {'amounts': ['--1', '1,00', '1 00']},
            'expected': {'cents': [None, None, None]},
            'label': 'punctuation errors'},
           {'input': {'amounts': ['1000000000000', '-1000000000000.00']},
            'expected': {'cents': [None, None]},
            'label': 'thirteen integer digits are invalid'},
           {'input': {'amounts': ['000000000001.23', '0000000000001.23']},
            'expected': {'cents': [123, None]},
            'label': 'leading zeros count toward the digit limit'}],
 'generated': [{'amounts': ['21.00', '-0.10', '0.000', 0]},
               {'amounts': ['22.17', '-0.11', '1.000', 1]},
               {'amounts': ['23.34', '-0.12', '2.000', 2]},
               {'amounts': ['24.51', '-0.13', '3.000', 3]},
               {'amounts': ['25.68', '-0.14', '4.000', 4]},
               {'amounts': ['26.85', '-0.15', '5.000', 5]},
               {'amounts': ['27.02', '-0.16', '6.000', 6]},
               {'amounts': ['28.19', '-0.17', '7.000', 7]},
               {'amounts': ['29.36', '-0.18', '8.000', 8]},
               {'amounts': ['30.53', '-0.19', '9.000', 9]},
               {'amounts': ['31.70', '-0.20', '10.000', 10]},
               {'amounts': ['32.87', '-0.21', '11.000', 11]}],
 'mutations': [{'name': 'drops fractional cents before scaling',
                'old': 'int(Decimal(value) * 100)',
                'new': 'int(Decimal(value)) * 100'}],
 'sources': ['https://docs.python.org/3/library/decimal.html',
             'https://docs.python.org/3/library/re.html#re.fullmatch']}
