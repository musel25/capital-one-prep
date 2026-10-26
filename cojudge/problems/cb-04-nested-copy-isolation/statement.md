# 04. Follow ownership through a nested copy

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 1 · Easy · About 30 minutes**

**Before this problem:** Exercise 03. Follow references to dictionaries and nested lists.

## Learn first

Each change must produce a fresh configuration based on the original template. The starter lets one change affect other results. Your objective is to identify which nested objects must be independent before you repair the copy boundary.

Assignment gives another name to the same object. A shallow copy creates a new outer container but keeps references to its nested containers. If you copy a dictionary and then change a nested list, both dictionaries can show that change. deepcopy recursively copies nested values so that each configuration can change independently. Copy only what the model requires; a deliberate copy of known nested fields can also work. This task uses small JSON-like dictionaries and lists, so deep copying has clear meaning. The starter copies only the outer dictionary. Repair it so each result starts from the original template, not from a previous result.

### Worked trace

Start with limits `daily = 5`, `monthly = 30`, and tags `["base"]`. Apply changes `{"daily": 0}`, `{"tag": ""}`, and `{}`. The copies must be `(0, 30, ["base"])`, `(5, 30, ["base", ""])`, and `(5, 30, ["base"])`. The template remains `(5, 30, ["base"])`. The second copy starts from the template, not the first copy.

### Read the existing code

In `solve`, inspect `template`, the creation of `config`, the writes to `config['limits']`, and the append to `config['tags']`. Draw the outer dictionary, nested limits dictionary, and tags list separately. Mark which arrows a copy must replace. The scalar limit values and string tags do not need independent mutable storage.

## Your task

### Scoped repair

Repair the configuration copy step. Keep every change independent and leave the input template unchanged. Preserve missing fields, numeric zero, empty tags, and duplicate tags. Keep the same return structure and change order. Do not reuse the preceding copy as the next starting point. Do not alter the template to undo changes after the loop.

### Required behavior

Bug-fix task. `data.template` is `{"limits":{"daily":nonnegative_integer,"monthly":nonnegative_integer},"tags":[strings]}`. `data.changes` is a list of objects. A change may contain `daily`, `monthly`, and `tag`; no other keys occur. Numeric values replace that limit. A tag is appended even if it is an empty string or already exists. For each change, create an independent copy of the original template and apply only that change. Return `{"template": unchanged_original, "copies": [updated_configurations]}` in change order. Repair the shallow-copy starter.

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

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Next, complete lab01 and lab02 from the guide.

## Examples

### Example 1: copies and template stay independent

Input to `solve`:
```json
{
  "template": {
    "limits": {
      "daily": 1,
      "monthly": 10
    },
    "tags": [
      "base"
    ]
  },
  "changes": [
    {
      "daily": 2
    },
    {
      "tag": "new"
    }
  ]
}
```
Return:
```json
{
  "template": {
    "limits": {
      "daily": 1,
      "monthly": 10
    },
    "tags": [
      "base"
    ]
  },
  "copies": [
    {
      "limits": {
        "daily": 2,
        "monthly": 10
      },
      "tags": [
        "base"
      ]
    },
    {
      "limits": {
        "daily": 1,
        "monthly": 10
      },
      "tags": [
        "base",
        "new"
      ]
    }
  ]
}
```

### Example 2: one change can update all fields

Input to `solve`:
```json
{
  "template": {
    "limits": {
      "daily": 5,
      "monthly": 50
    },
    "tags": []
  },
  "changes": [
    {
      "daily": 0,
      "monthly": 0,
      "tag": "x"
    }
  ]
}
```
Return:
```json
{
  "template": {
    "limits": {
      "daily": 5,
      "monthly": 50
    },
    "tags": []
  },
  "copies": [
    {
      "limits": {
        "daily": 0,
        "monthly": 0
      },
      "tags": [
        "x"
      ]
    }
  ]
}
```

### Example 3: no requested copies

Input to `solve`:
```json
{
  "template": {
    "limits": {
      "daily": 0,
      "monthly": 0
    },
    "tags": []
  },
  "changes": []
}
```
Return:
```json
{
  "template": {
    "limits": {
      "daily": 0,
      "monthly": 0
    },
    "tags": []
  },
  "copies": []
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

- [Official documentation 1](https://docs.python.org/3.11/library/copy.html)
