**The ticket.** The page renderer puts user values into a trusted HTML template with placeholders like `{{name}}`.

**Why it matters.** If a value contains `<script>` and you insert it without escaping, the script runs in another user's browser. This attack is called cross-site scripting (XSS). Escape every inserted value.

### Your task

Write `render_html(template, values)`. Return the rendered text.

1. A placeholder is `{{name}}`. The name starts with a letter or `_`, then has letters, digits, or `_`. There are no spaces.
2. If the name is in `values`, replace the placeholder with the escaped value. Escape `&`, `<`, `>`, `"`, and `'` as `&amp;`, `&lt;`, `&gt;`, `&quot;`, and `&#x27;`. `html.escape(text)` does exactly this.
3. If the name is not in `values`, keep the placeholder unchanged.
4. Do not change any other template text, also `&` or `<b>`.
5. Replace in one pass. Do not process text that you inserted.

**Constraints:**

- The template has at most 10000 characters. `values` has at most 100 string values.
