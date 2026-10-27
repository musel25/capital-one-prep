# 06. Trace a composed fee dependency

[Course list](/?course=capital-one-codebase-practice) · Level 2 · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 05. Follow an object method call and read an integer calculation.

The calculator receives a policy object and calls its `fee` method. The rate policy has a rounding defect. Your objective is to separate dependency selection, fee calculation, and result construction, then repair only the responsible layer.

Composition gives an object another object that performs part of its work. A small protocol describes the methods that the dependency must provide. Python Protocol supports structural typing: a class can satisfy the interface without explicitly inheriting from it. A calculator can depend on fee(amount) instead of checking policy types for every amount. Select the policy once at the boundary, then let the calculator call it. This is polymorphism through a shared interface. Integer arithmetic can also make a percentage fee exact. To round a nonnegative integer fraction upward, add denominator minus one before integer division.

</details>

**Scenario:** A payment processor charges merchants a fee on each sale. Some merchants pay a flat fee. Others pay a percentage, given in basis points. The processor never undercharges, so a percentage fee rounds up to the next cent.

> **Bug report:** "Our rate is 2.5%. On a sale of 100 cents we were charged 2 cents. Your terms say fees round up, so it must be 3."

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

**What to fix:** The starter runs, but it has one intentional bug.

- Repair the integer calculation in `RateFee.fee`.
- Keep the Protocol interface, constructor inputs, and quote shape.
- Preserve `FlatFee` behavior, including a flat charge for amount zero.
- Do not add policy-type branches to `Calculator.quote`.
- Keep exact integer arithmetic and the input amount unchanged.

**Constraints:**

- At most 100 amounts. Cent values are at most 1,000,000,000,000.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Select a rate policy of `125` basis points and amounts `[0, 80, 81]`. The exact unrounded fees are `0`, `1`, and `1.0125` cents. Round each upward to obtain fees `[0, 1, 2]` and totals `[0, 81, 83]`. `solve` selects the policy once. Each `Calculator.quote` delegates one amount to that policy and adds the returned fee.

### Read the existing code

Inspect the `FeePolicy.fee` signature. Follow construction in `solve` to `Calculator.__init__` and `Calculator.quote`. Compare `FlatFee.fee` and `RateFee.fee`. Identify which layer knows the policy kind and which layer knows how a quote is represented. Check units: amounts and fees are cents; `bps` is a rate.

### Test before and after the change

Before Run, compute a rate fee with a zero remainder and one with a nonzero remainder. Use `bps = 125` with amounts `80` and `81` as a pair. Also test amount zero, rate zero, rate `10000`, and a one-cent amount at a small positive rate. Test a nonzero flat fee on amount zero as a compatibility check. Assert both `fee` and `total`; a correct total shape can still contain the wrong fee.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “A zero amount must always have a zero fee, regardless of the selected policy.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`. Explain how `Calculator` uses `FeePolicy` without selecting a concrete policy on every quote. Cite the selection, storage, delegation, and output lines. Identify the units in the rate calculation. Do not give a rounding expression, implementation, or test code. I will derive the arithmetic cases.

### Technical completion checks

- Map the dependency from policy selection to quote output.
- Run exact-division, fractional-cent, and flat-policy cases.
- Review integer arithmetic and delegation. The judge does not inspect Protocol use or dependency design.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 07](/problems/cb-07-explicit-order-states).

Official documentation: [1](https://docs.python.org/3.11/library/typing.html#typing.Protocol)
