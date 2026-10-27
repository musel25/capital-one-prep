# 15. Compose a calculator with a fee policy

[Course list](/?course=capital-one-engineering-50) · Level 2 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Classes, type annotations, and integer arithmetic.

Composition gives an object another object that performs part of its work. A small protocol describes the methods that the dependency must provide. Python Protocol supports structural typing: a class can satisfy the interface without explicitly inheriting from it. A calculator can depend on fee(amount) instead of checking policy types for every amount. Select the policy once at the boundary, then let the calculator call it. This is polymorphism through a shared interface. Integer arithmetic can also make a percentage fee exact. To round a nonnegative integer fraction upward, add denominator minus one before integer division.

</details>

**Input:** `data` has:
- `policy`: one of these:
  - `{"kind": "flat", "cents": int}`, with nonnegative `cents`.
  - `{"kind": "rate", "bps": int}`, with `bps` from 0 to 10,000. One basis point is 1/100 of one percent.
- `amounts`: a list of nonnegative integer amounts in cents.

**Rules:** the fee for each amount:
- Flat: the fee is `cents`, also when the amount is 0.
- Rate: the fee is amount × bps / 10000, rounded up to a whole cent.

**Return** a list of `{"fee": int, "total": int}` in input order, where `total` = amount + fee.

**Practice:** use a `Protocol` and composition. The judge checks only the output.

**Constraints:**

- At most 100 amounts. Cent values are at most 1,000,000,000,000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/typing.html#typing.Protocol)
