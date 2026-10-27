# 08. Locate a batch commit boundary

[Course list](/?course=capital-one-codebase-practice) · Level 2 · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 07. Trace accepted and rejected state transitions.

A batch can contain valid transfers followed by one that fails. The starter lets earlier writes escape from a rejected batch. Your objective is to distinguish tentative balances from published balances and find the single commit boundary.

Atomic means that an operation has one complete result: all intended changes happen, or none happen. A loop that updates live balances can leave a partial result when a later transfer fails. For a small in-memory model, start with a working copy. Apply each transfer to that copy in order. Earlier transfers in the same batch can fund later transfers. Publish the working copy only after every transfer succeeds. On failure, discard it. This method is a simulation of atomic behavior within one call. It does not create a database transaction or protect the state from concurrent callers.

</details>

**Scenario:** A payroll system sends transfers in batches. A batch is all-or-nothing: if one transfer in it fails, none of the batch happens. Operations report that after a failed batch, some money moved anyway.

> **Bug report:** "A payroll batch was rejected because one account had too little money. But the first transfer of that batch still moved money."

**Input:** `data` has:
- `accounts`: maps account IDs to nonnegative integer cents.
- `batches`: a list of batches. Each batch is a list of transfers `{"from": string, "to": string, "cents": int}`, with nonnegative `cents`. Both accounts always exist.

**Rules**
- Process batches in order. Inside a batch, process transfers in order. Each transfer uses the balances after the earlier transfers in the same batch.
- If any source has less than `cents`, reject the whole batch and restore the balances from the start of that batch.
- Otherwise accept the batch and keep all its transfers.
- A self-transfer needs enough funds but does not change the balance.
- An empty batch is accepted.

**Return** `{"accepted": [bool], "balances": {...}}`: one boolean per batch, and the final account map.

**What to fix:** The starter runs, but it has one intentional bug. The starter keeps part of a rejected batch (a partial write). Repair it.

- Repair the ownership of tentative batch state.
- Preserve transfer order inside a batch and commit only after all transfers succeed.
- Keep empty batches successful.
- Keep the self-transfer funds check.
- Do not add a rollback log, database, or concurrent execution.
- A shallow dictionary copy is sufficient here because balances are integer values.

**Constraints:**

- At most 30 accounts, 30 batches, and 100 transfers per batch. Input cents and initial balances are at most 1,000,000,000,000.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Start with `A = 5`, `B = 0`, and `C = 0`. In one batch, transfer `4` from A to B, then `6` from B to C. After the first tentative transfer, balances are `(1, 4, 0)`. The second fails. The batch result must be false, and published balances must remain `(5, 0, 0)`. A later batch transferring `5` from A to C must therefore succeed.

### Read the existing code

Inspect `Ledger.__init__` to see how input balances enter the object. In `Ledger.apply_batch`, locate `trial`, the funds check, both balance writes, and the final assignment to `self.balances`. Mark which paths reach that final assignment. Follow repeated calls from `solve` to see when a successful batch becomes the next batch's starting state.

### Test before and after the change

Write a late-failure regression with at least one earlier transfer that changes balances. Predict a subsequent batch that distinguishes restored state from partial state. Also test failure on the first transfer, an empty batch, a zero transfer, a funded and an unfunded self-transfer, and a transfer funded by an earlier transfer in the same batch. Check total funds as an additional invariant, but do not use conservation alone: partial writes can conserve money and still violate atomicity.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “A batch can validate each transfer against its starting balances before applying any transfer.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`. Trace ownership of balances through `Ledger.__init__` and `Ledger.apply_batch`. Cite file lines for tentative writes, rejection, and publication. Explain whether a later transfer reads starting or tentative funds. Do not propose a copy expression, rollback implementation, or tests. I will write the regression.

### Technical completion checks

- Identify the tentative state and the commit boundary.
- Run both a late-failure regression and a within-batch funding case.
- Review rejected-operation behavior. This in-memory result does not prove database transaction or concurrency safety.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Next, complete lab03 and lab04 from the guide.

Official documentation: [1](https://docs.python.org/3.11/library/stdtypes.html#dict.copy)
