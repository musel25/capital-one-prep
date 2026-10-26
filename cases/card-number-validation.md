# Digital card-number validation

## A staged product-and-code case

Start with the business discussion, then reveal the number rules and classify examples before looking at code. Work without executing code or asking an AI to solve the case. Save your required and actual outcomes before revealing the answer. This is original constructed practice; the specific rules are not presented as an employer's question.

# Product discussion

A bank is considering letting customers generate an alternative card number in its app for online purchases. Purchases would still charge the same underlying account; the customer would give the merchant the generated number instead of the primary card number. The bank has not yet decided whether these numbers should be single-use, tied to one merchant, or reusable.

In 60–90 seconds, recommend a pilot, explain a customer benefit and a business benefit, identify one limitation or risk, and propose one success metric and one harm metric. State which usage model you assume and what you would clarify. Do not invent measured results. The later eight-digit validation rules are a separate fictional coding exercise, not a proposed payment-card format.

# Rules and examples

These are invented practice rules, not real payment-card standards or confirmed interview questions. Do not substitute Luhn or any other remembered validation scheme.

Inputs are strings. A valid number must meet **all four** rules:
1. Exactly eight ASCII digits (0–9). Preserve leading zeros. Do not trim spaces or convert the entire string to an integer.
2. The first two characters are `04` or `07`.
3. No four identical digits appear consecutively anywhere in the full eight-character string.
4. The final digit equals the sum of the first seven digits modulo 10.

Classify these examples by hand and give the first failed rule for each rejection. For checksum arithmetic, write the sum and remainder.

| Label | Input string |
|---|---|
| A | `04123459` |
| B | `07123452` |
| C | `04123450` |
| D | `04112222` |
| E | `04000004` |
| F | `09123454` |
| G | `0412345` |
| H | `04123A59` |
| I | `０4123459` (first character is a full-width zero, not ASCII) |
| J | `04333003` |

# Read the implementation

Trace this code on the same examples. Record actual outcomes separately from your earlier rule-based predictions. Identify the first mismatch and explain the condition responsible.

```python
def is_valid(number):
    if len(number) != 8 or not number.isascii() or not number.isdigit():
        return False
    if number[:2] not in ("04", "07"):
        return False
    if any(number[i:i+4] == number[i] * 4 for i in range(4)):
        return False
    return int(number[-1]) <= sum(int(digit) for digit in number[:7]) % 10
```

# Correct and extend

Correct is_valid without changing the rules. Then write classify(numbers), returning one boolean per input string in the original order, preserving duplicates and leaving the input unchanged. Explain an empty-list example and one new counterexample for each fix. Keep this on paper or in the editor without execution until your practice review.

Save required and actual outcomes before opening the instructor answer key.
