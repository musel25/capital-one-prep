# Instructor: digital card-number validation

## Checked classification

| Label | Required | Current code | Reason under the rules |
|---|---|---|---|
| A | True | True | Sum 19, check digit 9 |
| B | True | True | Sum 22, check digit 2 |
| C | False | True | Check digit 0 differs from required 9 |
| D | False | True | Four 2s at the end; checksum itself is valid |
| E | False | False | Four consecutive 0s |
| F | False | False | Prefix 09 is not allowed |
| G | False | False | Seven characters |
| H | False | False | A is not a digit |
| I | False | False | Full-width zero is not ASCII |
| J | True | True | Three consecutive 3s are allowed; sum 13, check digit 3 |

C is the first mismatch in table order. `<=` accepts incorrect smaller check digits. The run check examines starts 0–3, omitting start 4: D exposes that boundary. Fix the actual predicates rather than adding exceptions for sample numbers.

```python
def is_valid(number):
    if len(number) != 8 or not number.isascii() or not number.isdigit():
        return False
    if number[:2] not in ("04", "07"):
        return False
    if any(number[i:i+4] == number[i] * 4 for i in range(len(number) - 3)):
        return False
    return int(number[-1]) == sum(int(digit) for digit in number[:7]) % 10

def classify(numbers):
    return [is_valid(number) for number in numbers]
```

`classify` preserves order and duplicates and never changes its input; empty input returns []. A single check takes constant time for these fixed-length numbers. For n inputs, classification takes O(n) time and O(n) result space. If number length were variable, account for characters scanned.

Additional manual checks: empty string, leading/trailing space, nine digits, a non-ASCII digit, and a valid number repeated twice. Test each rule independently; a bad checksum can hide a missing run check.

The business discussion has multiple defensible answers. Explain how a virtual number could reduce exposure of a primary card credential at a merchant, and discuss customer controls and lifecycle/support costs. Do not claim virtual cards eliminate fraud. A success measure could be legitimate purchase completion; a harm measure could be false declines. Validate assumptions in a limited rollout. These are proposals, not claims about Capital One's implementation.
