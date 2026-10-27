# 04. Follow ownership through a nested copy

[Course list](/?course=capital-one-codebase-practice) · Level 1 · Easy · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 03. Follow references to dictionaries and nested lists.

Each change must produce a fresh configuration based on the original template. The starter lets one change affect other results. Your objective is to identify which nested objects must be independent before you repair the copy boundary.

Assignment gives another name to the same object. A shallow copy creates a new outer container but keeps references to its nested containers. If you copy a dictionary and then change a nested list, both dictionaries can show that change. deepcopy recursively copies nested values so that each configuration can change independently. Copy only what the model requires; a deliberate copy of known nested fields can also work. This task uses small JSON-like dictionaries and lists, so deep copying has clear meaning. The starter copies only the outer dictionary. Repair it so each result starts from the original template, not from a previous result.

</details>

**Input:** `data` has:
- `template`: `{"limits": {"daily": int, "monthly": int}, "tags": [string]}`. The limits are nonnegative integers.
- `changes`: a list of objects. A change can contain `daily`, `monthly`, and `tag`. No other keys occur.

**Rules:** for each change:
1. Make an independent copy of the original template, not of an earlier copy.
2. `daily` or `monthly`: replace that limit with the value.
3. `tag`: append it to `tags`, even if it is an empty string or is already in the list.

**Return** `{"template": ..., "copies": [...]}`
- `template`: the original template, unchanged.
- `copies`: the updated configurations, in change order.

**What to fix:** The starter runs, but it has one intentional bug. The starter makes a shallow copy. Repair it.

- Repair the configuration copy step.
- Keep every change independent and leave the input template unchanged.
- Preserve missing fields, numeric zero, empty tags, and duplicate tags.
- Keep the same return structure and change order.
- Do not reuse the preceding copy as the next starting point.
- Do not alter the template to undo changes after the loop.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Start with limits `daily = 5`, `monthly = 30`, and tags `["base"]`. Apply changes `{"daily": 0}`, `{"tag": ""}`, and `{}`. The copies must be `(0, 30, ["base"])`, `(5, 30, ["base", ""])`, and `(5, 30, ["base"])`. The template remains `(5, 30, ["base"])`. The second copy starts from the template, not the first copy.

### Read the existing code

In `solve`, inspect `template`, the creation of `config`, the writes to `config['limits']`, and the append to `config['tags']`. Draw the outer dictionary, nested limits dictionary, and tags list separately. Mark which arrows a copy must replace. The scalar limit values and string tags do not need independent mutable storage.

### Test before and after the change

Predict the result for a daily change followed by an empty change. Then test a tag append followed by an empty change. The two pairs exercise different nested containers. Check the returned template as well as every copy. Include monthly-only changes, daily zero, empty tags, and duplicate tags. In a local test, save the input before `solve` and compare it afterward. Equality of the final copy alone cannot prove input preservation.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “Copying the outer dictionary and the limits dictionary is sufficient, because tags contain immutable strings.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`. Draw the object references used by `template`, `config`, `limits`, and `tags`. Cite file lines for each nested write. Identify which objects need independent ownership under the stated contract. Do not choose a copy implementation or write code. I will test the ownership requirements.

### Technical completion checks

- Draw ownership for both nested containers before editing.
- Run independent regressions for limits and tags.
- Review template preservation and independence between copies. Judge equality checks do not inspect every possible object alias.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Next, complete lab01 and lab02 from the guide.

Official documentation: [1](https://docs.python.org/3.11/library/copy.html)
