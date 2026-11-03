## How it works

A regular expression finds each placeholder. A small function decides the replacement: the escaped value, or the unchanged placeholder when the name is unknown. Only inserted values are escaped. The trusted template stays the same.

## Common mistakes

- Not escaping quotes. A value can then break out of an HTML attribute.
- Removing unknown placeholders.
- Replacing names one after another, so inserted text is processed again.

## Solution

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
