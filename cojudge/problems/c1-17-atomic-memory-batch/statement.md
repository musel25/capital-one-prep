# 17. Fix an in-memory transfer batch

[Course list](/?course=capital-one-engineering-50) · Level 2 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Dictionary copies, account invariants, and ordered operations.

Atomic means that an operation has one complete result: all intended changes happen, or none happen. A loop that updates live balances can leave a partial result when a later transfer fails. For a small in-memory model, start with a working copy. Apply each transfer to that copy in order. Earlier transfers in the same batch can fund later transfers. Publish the working copy only after every transfer succeeds. On failure, discard it. This method is a simulation of atomic behavior within one call. It does not create a database transaction or protect the state from concurrent callers.

</details>

**Scenario:** A payroll system sends transfers in batches. A batch is all-or-nothing: if one transfer in it fails, none of the batch happens. Operations report that after a failed batch, some money moved anyway.

**Bug fix.** The starter keeps part of a rejected batch (a partial write). Repair it.

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

**Constraints:**

- At most 30 accounts, 30 batches, and 100 transfers per batch. Input cents and initial balances are at most 1,000,000,000,000.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/stdtypes.html#dict.copy)
