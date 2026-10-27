# 01. Trace a configuration default

[Course list](/?course=capital-one-codebase-practice) · Level 1 · Easy · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Lists, dictionaries, loops, and functions. This is the first exercise in this course.

Start with one function and two result fields. `solve` reads each record and builds `limits` and `configured`. The runnable starter changes a valid explicit value. Your objective is to separate a field's presence from its value before you repair that behavior.

A field can be absent, present with null, or present with zero. These states often have different meanings. Dictionary membership tells you whether a key exists. A value of None represents JSON null after decoding. Zero is a configured numeric value, even though it is false in a boolean condition. An expression such as value or default merges these states and can replace a valid zero. Write the decision in the same order as the contract: first check membership, then inspect the stored value. This makes defaults explicit and avoids an accidental change to a caller’s configuration.

</details>

**Scenario:** You work on the alert service of a banking app. Each customer can set a daily limit for push alerts. The app stores one settings record per customer. Before the service sends alerts, it calls `solve` to get the real limit of each customer.

A record can be in three states:
- The customer never opened the setting: there is no `limit` key, so use the company default.
- The customer chose "no limit": `limit` is `null`. Keep `null`, so the service does not cap their alerts.
- The customer chose a number: keep it. `0` means "send me no alerts".

The product team also counts how many customers set their own limit (a number, including 0).

> **Bug report:** "I set my alert limit to 0 because I want no alerts. I still get 10 alerts every day."

**Input:** `data` has:
- `default`: a nonnegative integer.
- `records`: a list of objects. A record can have a `limit` key whose value is a nonnegative integer or `null`. Ignore all other keys.

**Rules:** resolve the limit of each record.
- No `limit` key → `default`.
- `limit` is `null` → `null`.
- `limit` is a number, including `0` → that number.

**Return** `{"limits": [...], "configured": int}`
- `limits`: the resolved limit of each record, in input order.
- `configured`: the number of records that have a `limit` key with a non-null value. A `0` counts.

**What to fix:** The starter runs, but it has one intentional bug.

- Repair only the per-record value handling in `solve`.
- Keep the input keys, output keys, record order, and count rule.
- Preserve explicit null and zero.
- Ignore unrelated fields.
- Do not add validation for inputs that the contract excludes.
- Keep the loop so its behavior remains easy to compare with your trace.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Use `default = 12` and records `[{}, {"limit": 0}, {"limit": null}]`. After the first record, `limits` is `[12]` and `configured` is `0`. After the second, they are `[12, 0]` and `1`. After the third, they are `[12, 0, null]` and `1`. The count records an explicit, non-null setting. It cannot be derived from the resolved numbers alone.

### Read the existing code

Read `solve` from its input loop to its return. Mark the branch that detects an absent `limit`. Then find where `value` enters `limits` and where `configured` changes. For each branch, write which input state reaches it. Read the stored value and the output decision as separate steps.

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

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 02](/problems/cb-02-typed-json-boundary).

Official documentation: [1](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
