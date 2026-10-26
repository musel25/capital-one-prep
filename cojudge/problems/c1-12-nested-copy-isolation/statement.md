# 12. Fix nested configuration copies

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Easy · About 20 minutes**

**Before this problem:** Nested dictionaries, lists, and object references.

## Learn first

Assignment gives another name to the same object. A shallow copy creates a new outer container but keeps references to its nested containers. If you copy a dictionary and then change a nested list, both dictionaries can show that change. deepcopy recursively copies nested values so that each configuration can change independently. Copy only what the model requires; a deliberate copy of known nested fields can also work. This task uses small JSON-like dictionaries and lists, so deep copying has clear meaning. The starter copies only the outer dictionary. Repair it so each result starts from the original template, not from a previous result.

## Your task

Bug-fix task. `data.template` is `{"limits":{"daily":nonnegative_integer,"monthly":nonnegative_integer},"tags":[strings]}`. `data.changes` is a list of objects. A change may contain `daily`, `monthly`, and `tag`; no other keys occur. Numeric values replace that limit. A tag is appended even if it is an empty string or already exists. For each change, create an independent copy of the original template and apply only that change. Return `{"template": unchanged_original, "copies": [updated_configurations]}` in change order. Repair the shallow-copy starter.

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
