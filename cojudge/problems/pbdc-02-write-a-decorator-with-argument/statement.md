# 02. Write a decorator with argument

Implement `make_html(tag)`.

This function creates a decorator. The decorated function returns its text
between an opening HTML tag and the matching closing tag. The supplied `tag`
is a valid, nonempty tag name without brackets. Do not escape the text.
Forward positional and keyword arguments. Preserve the function name,
docstring and annotations. Propagate exceptions from the wrapped function.

Decorators can be stacked:

```python
@make_html('p')
@make_html('strong')
def greeting():
    return 'Hello'

greeting()  # '<p><strong>Hello</strong></p>'
```
