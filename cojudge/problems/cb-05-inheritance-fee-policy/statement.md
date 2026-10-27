# 05. Follow an inherited call to an override

[Course list](/?course=capital-one-codebase-practice) · Level 2 · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 01–04 and local labs 01–02. The lesson introduces inherited method calls.

A premium account inherits the withdrawal workflow and changes its fee rule. The starter mishandles a boundary of that rule. Your objective is to trace the actual method selected for an instance without duplicating the shared withdrawal logic.

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

**What to fix:** The starter runs, but it has one intentional bug.

- Repair only the premium fee decision in `PremiumAccount.withdrawal_fee`.
- Preserve the shared sufficiency check and the rule that a rejection changes nothing.
- Keep standard-account behavior unchanged.
- Do not copy `withdraw` into the subclass.
- Do not change the threshold based on the remaining balance; it applies to the requested amount.

**Constraints:**

- At most 100 withdrawals. Numeric input values are at most 1,000,000,000,000.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Use a premium account with balance `24`, fee `3`, threshold `10`, and withdrawals `[9, 10, 3]`. The first withdrawal costs `12`, leaving `12`. The second costs `10`, leaving `2`. The third would cost `6`, so it fails and leaves `2`. The required result is `{"accepted": [true, true, false], "balance": 2}`. The same inherited `withdraw` method handles all three decisions.

### Read the existing code

Follow `solve` to `PremiumAccount.__init__`, then to `Account.__init__` through `super()`. Follow `Account.withdraw` to `self.withdrawal_fee`. Compare `Account.withdrawal_fee` with `PremiumAccount.withdrawal_fee`. Record which values come from base state and which come from premium state.

### Test before and after the change

Predict premium withdrawals just below, exactly at, and just above a threshold. Use separate runs first so an earlier withdrawal cannot hide a boundary error. Test exact funds for amount plus fee, funds sufficient only when the fee is waived, and a rejected withdrawal followed by a smaller successful one. Repeat a boundary input with `kind = standard` to check the unchanged base rule. Include fee zero and threshold zero.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “Even though `withdraw` is defined in `Account`, its call through `self` can use `PremiumAccount.withdrawal_fee`.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`. Trace one call from `solve` through the inherited `Account.withdraw` method to the fee method selected for a premium instance. Cite file lines and explain the receiver at each call. Do not change a comparison or implement an override. I will derive the threshold tests.

### Technical completion checks

- Trace the selected fee method for both account kinds.
- Run threshold and exact-funds cases with hand-written expected balances.
- Review the diff for one policy change. Judge success does not prove that shared withdrawal logic remains in the base class.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 06](/problems/cb-06-composed-fee-protocol).

Official documentation: [1](https://docs.python.org/3.11/tutorial/classes.html#inheritance), [2](https://docs.python.org/3.11/library/functions.html#super)
