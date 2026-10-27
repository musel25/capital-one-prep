# 14. Extend an account with a fee rule

[Course list](/?course=capital-one-engineering-50) · Level 2 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Classes and the balance invariant exercise.

Inheritance lets a subclass reuse a base implementation while replacing a specific behavior. A subclass initializer can call super().__init__ to establish the base state before adding its own fields. A base method can call another instance method such as withdrawal_fee. Python then selects the override on the actual object. This keeps the withdrawal check in one place while allowing a premium account to use a different fee rule. Avoid copying the whole withdrawal method just to change one calculation. Both amount and fee must fit in the balance. A rejected operation must charge neither of them.

</details>

**Input:** `data` has (all amounts in cents):
- `kind`: `"standard"` or `"premium"`.
- `balance`, `fee`, `threshold`: nonnegative integers.
- `withdrawals`: a list of positive integers.

**Rules:** for each withdrawal amount, in order:
- The fee: a standard account charges `fee`. A premium account charges 0 when the amount is at least `threshold`, otherwise `fee`.
- The withdrawal succeeds when amount + fee is at most the current balance. Subtract amount + fee.
- A failed withdrawal changes nothing.

**Return** `{"accepted": [bool], "balance": int}`: one boolean per withdrawal, and the final balance.

**Practice:** use inheritance, `super()`, and a fee method override. The judge checks only the output.

**Constraints:**

- At most 100 withdrawals. Numeric input values are at most 1,000,000,000,000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/tutorial/classes.html#inheritance), [2](https://docs.python.org/3.11/library/functions.html#super)
