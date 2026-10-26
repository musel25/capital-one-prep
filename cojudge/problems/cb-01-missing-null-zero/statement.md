# 01. Trace a configuration default

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 1 · Easy · About 30 minutes**

**Before this problem:** Lists, dictionaries, loops, and functions. This is the first exercise in this course.

## Learn first

Start with one function and two result fields. `solve` reads each record and builds `limits` and `configured`. The runnable starter changes a valid explicit value. Your objective is to separate a field's presence from its value before you repair that behavior.

A field can be absent, present with null, or present with zero. These states often have different meanings. Dictionary membership tells you whether a key exists. A value of None represents JSON null after decoding. Zero is a configured numeric value, even though it is false in a boolean condition. An expression such as value or default merges these states and can replace a valid zero. Write the decision in the same order as the contract: first check membership, then inspect the stored value. This makes defaults explicit and avoids an accidental change to a caller’s configuration.

### Worked trace

Use `default = 12` and records `[{}, {"limit": 0}, {"limit": null}]`. After the first record, `limits` is `[12]` and `configured` is `0`. After the second, they are `[12, 0]` and `1`. After the third, they are `[12, 0, null]` and `1`. The count records an explicit, non-null setting. It cannot be derived from the resolved numbers alone.

### Read the existing code

Read `solve` from its input loop to its return. Mark the branch that detects an absent `limit`. Then find where `value` enters `limits` and where `configured` changes. For each branch, write which input state reaches it. Read the stored value and the output decision as separate steps.

## Your task

### Scoped repair

Repair only the per-record value handling in `solve`. Keep the input keys, output keys, record order, and count rule. Preserve explicit null and zero. Ignore unrelated fields. Do not add validation for inputs that the contract excludes. Keep the loop so its behavior remains easy to compare with your trace.

### Required behavior

`data` has nonnegative integer `default` and a list `records`. Each record is an object. It may contain `limit`, whose value is a nonnegative integer or null. Ignore other keys. An absent `limit` resolves to `default`. An explicit null resolves to null. Zero stays zero. Return `{"limits": [resolved_values], "configured": count}`. Count only records that contain a non-null `limit`, including zero.

### Test before and after the change

Before Run, predict the full result for `default = 0` and records `[{}, {"limit": 0}]`. Both outputs are zero, but only one record is configured. Write that expected result yourself. Then check an empty list, explicit null with a nonzero default, a positive value, and two identical explicit values. Check both output fields in each test. A test of `configured` alone will miss a wrong resolved value.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “When the default is zero, every zero in the resolved limits list counts as a configured record.”

Optional AI prompt. Write your own implementation and tests:

> I will paste this task's starter as `solution.py`. Trace `solve` for an absent limit, a null limit, and a zero limit. Cite line numbers and short code excerpts from that file. State which input distinction each branch preserves. Do not propose a replacement expression or write an implementation. I will predict and test the outputs.

### Technical completion checks

- Predict a case where equal output values have different input meanings.
- Run your cases and the judge. Record what their results establish.
- Review the diff. Confirm that the count rule and unrelated fields still follow the contract.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 02](/problems/cb-02-typed-json-boundary).

## Examples

### Example 1: three distinct field states

Input to `solve`:
```json
{
  "default": 10,
  "records": [
    {},
    {
      "limit": null
    },
    {
      "limit": 0
    },
    {
      "limit": 4
    }
  ]
}
```
Return:
```json
{
  "limits": [
    10,
    null,
    0,
    4
  ],
  "configured": 2
}
```

### Example 2: count records, not distinct values

Input to `solve`:
```json
{
  "default": 5,
  "records": [
    {
      "limit": 2
    },
    {
      "limit": 2
    }
  ]
}
```
Return:
```json
{
  "limits": [
    2,
    2
  ],
  "configured": 2
}
```

### Example 3: empty records

Input to `solve`:
```json
{
  "default": 9,
  "records": []
}
```
Return:
```json
{
  "limits": [],
  "configured": 0
}
```

## Constraints

- At most 100 input items. All input values follow the stated contract.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 24 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
