## Reference solution

Paste this code above the supplied tests and runner.

```python
import re
def get_srt_section_ids(text):
    def milliseconds(value):
        match = re.fullmatch(r'(\d{2,}):([0-5]\d):([0-5]\d),(\d{3})', value.strip())
        if not match:
            raise ValueError('Invalid SRT time')
        h, m, s, ms = map(int, match.groups())
        return ((h * 60 + m) * 60 + s) * 1000 + ms
    if not text.strip():
        return []
    result, seen = [], set()
    for block in re.split(r'\n\s*\n', text.replace('\r\n', '\n').strip()):
        lines = block.splitlines()
        if len(lines) < 3:
            raise ValueError('Missing caption')
        section = int(lines[0].strip())
        if section in seen:
            raise ValueError('Duplicate section')
        seen.add(section)
        start, end = lines[1].split('-->')
        duration = milliseconds(end) - milliseconds(start)
        if duration <= 0:
            raise ValueError('Nonpositive duration')
        caption = ' '.join(line.strip() for line in lines[2:])
        result.append((section, len(caption) / duration))
    return [section for section, rate in sorted(result, key=lambda row: -row[1])]
```
