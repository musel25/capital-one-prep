# 08. Locate a batch commit boundary

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 2 · Medium · About 35 minutes**

**Before this problem:** Exercise 07. Trace accepted and rejected state transitions.

## Learn first

A batch can contain valid transfers followed by one that fails. The starter lets earlier writes escape from a rejected batch. Your objective is to distinguish tentative balances from published balances and find the single commit boundary.

Atomic means that an operation has one complete result: all intended changes happen, or none happen. A loop that updates live balances can leave a partial result when a later transfer fails. For a small in-memory model, start with a working copy. Apply each transfer to that copy in order. Earlier transfers in the same batch can fund later transfers. Publish the working copy only after every transfer succeeds. On failure, discard it. This method is a simulation of atomic behavior within one call. It does not create a database transaction or protect the state from concurrent callers.

### Worked trace

Start with `A = 5`, `B = 0`, and `C = 0`. In one batch, transfer `4` from A to B, then `6` from B to C. After the first tentative transfer, balances are `(1, 4, 0)`. The second fails. The batch result must be false, and published balances must remain `(5, 0, 0)`. A later batch transferring `5` from A to C must therefore succeed.

### Read the existing code

Inspect `Ledger.__init__` to see how input balances enter the object. In `Ledger.apply_batch`, locate `trial`, the funds check, both balance writes, and the final assignment to `self.balances`. Mark which paths reach that final assignment. Follow repeated calls from `solve` to see when a successful batch becomes the next batch's starting state.

## Your task

### Scoped repair

Repair the ownership of tentative batch state. Preserve transfer order inside a batch and commit only after all transfers succeed. Keep empty batches successful. Keep the self-transfer funds check. Do not add a rollback log, database, or concurrent execution. A shallow dictionary copy is sufficient here because balances are integer values.

### Required behavior

Bug-fix task. `data.accounts` maps account IDs to nonnegative integer cents. `data.batches` is a list of transfer lists. Each transfer has string `from`, string `to`, and nonnegative integer `cents`. Both accounts always exist. Process batches in order. Within a batch, process transfers in order using the tentative updated balances. If any source has less than cents, reject the entire batch and restore its starting balances. Otherwise accept all transfers. A self-transfer needs enough funds but leaves its balance unchanged. An empty batch succeeds. Return `{"accepted": [booleans_per_batch], "balances": final_account_map}`. Repair the starter’s partial-write defect.

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

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Next, complete lab03 and lab04 from the guide.

## Examples

### Example 1: late failure rolls back earlier transfer

Input to `solve`:
```json
{
  "accounts": {
    "A": 10,
    "B": 0
  },
  "batches": [
    [
      {
        "from": "A",
        "to": "B",
        "cents": 6
      },
      {
        "from": "A",
        "to": "B",
        "cents": 5
      }
    ]
  ]
}
```
Return:
```json
{
  "accepted": [
    false
  ],
  "balances": {
    "A": 10,
    "B": 0
  }
}
```

### Example 2: earlier transfer funds later transfer

Input to `solve`:
```json
{
  "accounts": {
    "A": 10,
    "B": 0,
    "C": 0
  },
  "batches": [
    [
      {
        "from": "A",
        "to": "B",
        "cents": 7
      },
      {
        "from": "B",
        "to": "C",
        "cents": 7
      }
    ]
  ]
}
```
Return:
```json
{
  "accepted": [
    true
  ],
  "balances": {
    "A": 3,
    "B": 0,
    "C": 7
  }
}
```

### Example 3: no accounts or batches

Input to `solve`:
```json
{
  "accounts": {},
  "batches": []
}
```
Return:
```json
{
  "accepted": [],
  "balances": {}
}
```

## Constraints

- At most 30 accounts, 30 batches, and 100 transfers per batch. Input cents and initial balances are at most 1,000,000,000,000.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 25 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3.11/library/stdtypes.html#dict.copy)
