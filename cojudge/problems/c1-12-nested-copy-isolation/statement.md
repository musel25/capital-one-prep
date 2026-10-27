# 12. Fix nested configuration copies

[Course list](/?course=capital-one-engineering-50) · Level 2 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Nested dictionaries, lists, and object references.

Assignment gives another name to the same object. A shallow copy creates a new outer container but keeps references to its nested containers. If you copy a dictionary and then change a nested list, both dictionaries can show that change. deepcopy recursively copies nested values so that each configuration can change independently. Copy only what the model requires; a deliberate copy of known nested fields can also work. This task uses small JSON-like dictionaries and lists, so deep copying has clear meaning. The starter copies only the outer dictionary. Repair it so each result starts from the original template, not from a previous result.

</details>

**Bug fix.** The starter makes a shallow copy. Repair it.

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

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/copy.html)
