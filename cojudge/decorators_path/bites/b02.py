"""HTML decorator factory: recreated from the public description."""

SPEC = {
    "title": "Write a decorator with argument",
    "module": "html_tags",
    "original": False,
    "contract": (
        "make_html(tag) returns a decorator for string-returning functions. tag "
        "is a nonempty valid HTML tag name supplied without brackets. Wrap the "
        "result as <tag>result</tag>, including empty results. Do not escape the "
        "result. Forward args and kwargs once. Preserve function name, docstring "
        "and annotations. Propagate wrapped exceptions. Invalid tags and "
        "non-string results are outside the contract."
    ),
    "statement": '''Implement `make_html(tag)`.

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
''',
    "template": '''def make_html(tag):
    """Create a decorator that encloses returned text in an HTML tag."""
    # TODO: return a decorator.
    pass
''',
    "tests": '''import pytest

from html_tags import make_html


def test_wraps_a_string_in_matching_tags():
    @make_html("span")
    def text():
        return "Hello"
    assert text() == "<span>Hello</span>"


def test_stacked_decorators_keep_the_declared_order():
    @make_html("p")
    @make_html("strong")
    def text():
        return "Hello"
    assert text() == "<p><strong>Hello</strong></p>"


def test_empty_text_and_html_are_not_escaped():
    @make_html("div")
    def text(value):
        return value
    assert text("") == "<div></div>"
    assert text("<b>A & B</b>") == "<div><b>A & B</b></div>"


def test_forwards_positional_and_keyword_arguments_once():
    calls = []
    @make_html("h2")
    def text(first, *rest, suffix):
        calls.append((first, rest, suffix))
        return first + " ".join(rest) + suffix
    assert text("A", "B", "C", suffix="!") == "<h2>AB C!</h2>"
    assert calls == [("A", ("B", "C"), "!")]


def test_preserves_function_metadata():
    def heading(value: str) -> str:
        """Return a heading."""
        return value
    wrapped = make_html("h1")(heading)
    assert wrapped.__name__ == "heading"
    assert wrapped.__doc__ == "Return a heading."
    assert wrapped.__annotations__ == {"value": str, "return": str}


def test_decoration_is_lazy_and_the_decorator_is_reusable():
    calls = []
    decorate = make_html("em")
    def first():
        calls.append("first")
        return "one"
    def second():
        calls.append("second")
        return "two"
    one, two = decorate(first), decorate(second)
    assert calls == []
    assert one() == "<em>one</em>"
    assert two() == "<em>two</em>"
    assert one() == "<em>one</em>"
    assert calls == ["first", "second", "first"]


def test_separate_factories_do_not_share_tags():
    @make_html("i")
    def first(value):
        return value
    @make_html("b")
    def second(value):
        return value
    assert first("one") == "<i>one</i>"
    assert second("two") == "<b>two</b>"
    assert first("three") == "<i>three</i>"


def test_propagates_the_original_exception():
    error = LookupError("missing text")
    @make_html("p")
    def reject():
        raise error
    with pytest.raises(LookupError) as caught:
        reject()
    assert caught.value is error
''',
    "examples": [{
        "input": "@make_html('p')\n@make_html('strong')\ndef greeting():\n    return 'Hello'\ngreeting()",
        "output": "<p><strong>Hello</strong></p>",
        "explanation": "The outer decorator adds the outer tag.",
    }],
    "notes": "The template and tests are recreated from the public description. Argument forwarding, metadata preservation and exception propagation are explicit course guarantees. Invalid tags are outside the contract.",
}

SPEC["reference"] = '''from functools import wraps


def make_html(tag):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            return f"<{tag}>{text}</{tag}>"
        return wrapper
    return decorate
'''
SPEC["mutations"] = [
    {"name": "omit closing slash", "old": "</{tag}>", "new": "<{tag}>"},
    {"name": "hard-code the tag", "old": 'return f"<{tag}>{text}</{tag}>"', "new": 'return f"<p>{text}</p>"'},
    {"name": "drop keyword arguments", "old": "func(*args, **kwargs)", "new": "func(*args)"},
    {"name": "call the wrapped function twice", "old": "text = func(*args, **kwargs)", "new": "text = func(*args, **kwargs)\n            func(*args, **kwargs)"},
    {"name": "lose function metadata", "old": "        @wraps(func)\n", "new": ""},
]
