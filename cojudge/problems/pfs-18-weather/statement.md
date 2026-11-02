## Learn

`elif` means "else if". Python checks from top to bottom and runs only the **first** true part.

```python
speed = int(input())
if speed < 10:
    print("slow")
elif speed < 50:
    print("medium")
else:
    print("fast")
```

For `30`, the first check is false and the second is true, so it shows `medium`.

## Your task

Read a temperature in °C. Show what to wear:

| Temperature | Your program shows |
| --- | --- |
| below 10 | `Cold. Wear a jacket.` |
| 10 to 24 | `Nice. Wear a sweater.` |
| 25 or more | `Hot. Wear a T-shirt.` |
