## Reference solution

```python
import html
import re


def render_html(template, values):
    pattern = r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}"

    def substitute(match):
        name = match.group(1)
        if name not in values:
            return match.group(0)
        return html.escape(values[name], quote=True)

    return re.sub(pattern, substitute, template)
```
