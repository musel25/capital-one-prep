"""Replace HTML placeholders once and escape inserted text."""

CASES = [
    {"label": "escape all five HTML special characters", "input": {"template": "<p>{{name}}</p>", "values": {"name": "<&>\"'"}}, "expected": "<p>&lt;&amp;&gt;&quot;&#x27;</p>"},
    {"label": "missing placeholder remains unchanged", "input": {"template": "Hello {{missing}}.", "values": {"name": "Ada"}}, "expected": "Hello {{missing}}."},
    {"label": "inserted placeholders are not processed again", "input": {"template": "{{a}} {{b}}", "values": {"a": "{{b}}", "b": "resolved"}}, "expected": "{{b}} resolved"},
    {"label": "empty template and values", "input": {"template": "", "values": {}}, "expected": ""},
    {"label": "plain template HTML remains unchanged", "input": {"template": "<b>& raw</b>", "values": {"a": "<"}}, "expected": "<b>& raw</b>"},
    {"label": "empty value removes placeholder", "input": {"template": "A{{name}}B", "values": {"name": ""}}, "expected": "AB"},
    {"label": "every repeated occurrence is replaced", "input": {"template": "{{x}}/{{x}}/{{x}}", "values": {"x": "<"}}, "expected": "&lt;/&lt;/&lt;"},
    {"label": "underscore and digits are valid identifier characters", "input": {"template": "{{_a1}} {{Z9}}", "values": {"_a1": "one", "Z9": "two"}}, "expected": "one two"},
    {"label": "spaces hyphens leading digits and empty names do not match", "input": {"template": "{{ a }}|{{a b}}|{{a-b}}|{{1a}}|{{}}", "values": {"a": "x", "b": "y"}}, "expected": "{{ a }}|{{a b}}|{{a-b}}|{{1a}}|{{}}"},
    {"label": "Unicode text is preserved", "input": {"template": "¡Hola {{name}}! 🌍", "values": {"name": "李 & Zoë"}}, "expected": "¡Hola 李 &amp; Zoë! 🌍"},
    {"label": "existing value entities are escaped again", "input": {"template": "{{x}}", "values": {"x": "&amp;"}}, "expected": "&amp;amp;"},
    {"label": "template entities remain while value entities escape", "input": {"template": "&copy; {{x}}", "values": {"x": "&copy;"}}, "expected": "&copy; &amp;copy;"},
    {"label": "replacement dollar and backslash are literal", "input": {"template": "{{path}}", "values": {"path": "$1\\path"}}, "expected": "$1\\path"},
    {"label": "names are case sensitive", "input": {"template": "{{A}} {{a}} {{B}}", "values": {"A": "upper", "a": "lower"}}, "expected": "upper lower {{B}}"},
    {"label": "surrounding unmatched braces remain template text", "input": {"template": "{{{a}}}", "values": {"a": "X"}}, "expected": "{X}"},
    {"label": "one-pass replacement still escapes inserted markup", "input": {"template": "{{a}}", "values": {"a": "{{b}}<", "b": "done"}}, "expected": "{{b}}&lt;"},
    {"label": "line breaks in values remain line breaks", "input": {"template": "<pre>{{text}}</pre>", "values": {"text": "one\ntwo"}}, "expected": "<pre>one\ntwo</pre>"},
]

SPEC = {
    "number": 24,
    "slug": "render-escaped-html-values",
    "title": "Render HTML placeholders safely",
    "difficulty": "Medium",
    "category": "06-application-logic",
    "ticket": "The page renderer must escape inserted values while preserving the trusted HTML template.",
    "task": "Implement `render_html(template, values)`. The template is trusted HTML text. Match each substring `{{name}}` whose name follows `[A-Za-z_][A-Za-z0-9_]*`, with no spaces. If name is a key in values, replace that occurrence with its escaped string value. Escape `&` as `&amp;`, `<` as `&lt;`, `>` as `&gt;`, double quotes as `&quot;`, and single quotes as `&#x27;`. Leave missing placeholders and all other template text unchanged. Perform one pass over the original template: inserted placeholders must not be processed again. Compare names exactly. Empty strings are valid. Return the rendered string. Do not change the input.",
    "constraints": ["The template is a Unicode string of at most 10000 characters.", "values has at most 100 keys, each matching the stated identifier rule.", "All values are Unicode strings, including empty strings; their combined length is at most 10000 characters."],
    "function": "render_html",
    "starter": "def render_html(template, values):\n    raise NotImplementedError\n",
    "reference": r'''import html
import re


def render_html(template, values):
    pattern = r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}"

    def substitute(match):
        name = match.group(1)
        if name not in values:
            return match.group(0)
        return html.escape(values[name], quote=True)

    return re.sub(pattern, substitute, template)
''',
    "java": r'''private String escapeValue(String value) {
    StringBuilder escaped = new StringBuilder();
    for (int i = 0; i < value.length(); i++) {
        char ch = value.charAt(i);
        if (ch == '&') escaped.append("&amp;");
        else if (ch == '<') escaped.append("&lt;");
        else if (ch == '>') escaped.append("&gt;");
        else if (ch == '"') escaped.append("&quot;");
        else if (ch == 39) escaped.append("&#x27;");
        else escaped.append(ch);
    }
    return escaped.toString();
}

public Object solve(Map<String,Object> d) {
    String template = s(d.get("template"));
    Map<String,Object> values = obj(d.get("values"));
    Matcher matcher = Pattern.compile("\\{\\{([A-Za-z_][A-Za-z0-9_]*)\\}\\}").matcher(template);
    StringBuffer rendered = new StringBuffer();
    while (matcher.find()) {
        String name = matcher.group(1);
        String replacement = values.containsKey(name) ? escapeValue(s(values.get(name))) : matcher.group();
        matcher.appendReplacement(rendered, Matcher.quoteReplacement(replacement));
    }
    matcher.appendTail(rendered);
    return rendered.toString();
}''',
    "cases": CASES,
    "mutations": [
        {"name": "leave quotes unescaped", "old": "quote=True", "new": "quote=False"},
        {"name": "erase missing placeholders", "old": "return match.group(0)", "new": "return ''"},
        {"name": "skip empty replacement values", "old": "if name not in values:", "new": "if name not in values or not values[name]:"},
        {"name": "process inserted placeholders a second time", "old": "return re.sub(pattern, substitute, template)", "new": "return re.sub(pattern, substitute, re.sub(pattern, substitute, template))"},
        {"name": "accept spaces around placeholder names", "old": r'pattern = r"\{\{([A-Za-z_][A-Za-z0-9_]*)\}\}"', "new": r'pattern = r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}"'},
    ],
}
