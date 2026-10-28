# 24. Render HTML placeholders safely

The page renderer must escape inserted values while preserving the trusted HTML template.

Implement `render_html(template, values)`. The template is trusted HTML text. Match each substring `{{name}}` whose name follows `[A-Za-z_][A-Za-z0-9_]*`, with no spaces. If name is a key in values, replace that occurrence with its escaped string value. Escape `&` as `&amp;`, `<` as `&lt;`, `>` as `&gt;`, double quotes as `&quot;`, and single quotes as `&#x27;`. Leave missing placeholders and all other template text unchanged. Perform one pass over the original template: inserted placeholders must not be processed again. Compare names exactly. Empty strings are valid. Return the rendered string. Do not change the input.

**Constraints:**

- The template is a Unicode string of at most 10000 characters.
- values has at most 100 keys, each matching the stated identifier rule.
- All values are Unicode strings, including empty strings; their combined length is at most 10000 characters.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `render_html`. **Run** checks the examples. **Submit** checks all 17 cases.
