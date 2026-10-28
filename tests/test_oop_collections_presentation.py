"""Run learner examples against the same reference code used by the judge."""
import ast
from contextlib import redirect_stdout
from io import StringIO
import sys
from types import ModuleType

import pytest

from cojudge.pybites import support as oop
from cojudge.collections_path import support as collections


@pytest.mark.parametrize('course', [oop, collections], ids=['oop', 'collections'])
def test_presented_examples_match_reference_results(course, tmp_path, monkeypatch):
    monkeypatch.setenv('TMP', str(tmp_path))
    for spec in course.load_specs():
        for example in course.present_problem(spec, [])['examples']:
            module = ModuleType(f"example_{course.COURSE_ID}_{spec['number']}")
            monkeypatch.setitem(sys.modules, module.__name__, module)
            with redirect_stdout(StringIO()):
                exec(spec['reference'], module.__dict__)
            tree = ast.parse(example['input'])
            output = StringIO()
            with redirect_stdout(output):
                if isinstance(tree.body[-1], ast.Expr):
                    last = tree.body.pop()
                    exec(compile(tree, '<example>', 'exec'), module.__dict__)
                    value = eval(compile(ast.Expression(last.value), '<example>', 'eval'), module.__dict__)
                    if value is not None:
                        print(repr(value))
                else:
                    exec(compile(tree, '<example>', 'exec'), module.__dict__)
            assert output.getvalue().rstrip() == example['output'], (spec['number'], example['input'])


def test_html_converter_keeps_literal_placeholder_tags_in_inline_code():
    spec = {'page': {'desc_html': '<p>Return <code>"<brand> <model> with <wheels> wheels"</code>.</p>'}}
    assert oop.description(spec) == 'Return `"<brand> <model> with <wheels> wheels"`.'


def test_html_converter_normalizes_code_block_line_endings():
    spec = {'page': {'desc_html': '<pre><code>x = 1\r\nprint(x)\r\n</code></pre>'}}
    assert oop.description(spec) == '```python\nx = 1\nprint(x)\n\n```'
