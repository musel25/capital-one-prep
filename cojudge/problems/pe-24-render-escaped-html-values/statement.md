The page renderer must escape inserted values while preserving the trusted HTML template.

Implement `render_html(template, values)`. Keep the trusted HTML template unchanged except for matching placeholders.

A placeholder is `{{name}}`, where `name` matches `[A-Za-z_][A-Za-z0-9_]*` with no spaces. If the name exists in `values`, insert its escaped string value. Escape `&`, `<`, `>`, double quotes, and single quotes as `&amp;`, `&lt;`, `&gt;`, `&quot;`, and `&#x27;`, respectively.

Leave missing placeholders and other template text unchanged. Process the original template once; do not process inserted placeholders again. Compare names exactly. Empty strings are valid. Return the rendered string.

**Constraints:**

- The template is a Unicode string of at most 10000 characters.
- values has at most 100 keys, each matching the stated identifier rule.
- All values are Unicode strings, including empty strings; their combined length is at most 10000 characters.
- Do not change input objects or their nested values. Each call starts with fresh state.
