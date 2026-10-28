"""Learner-facing descriptions and sample checks, separate from judge inputs."""
from __future__ import annotations

import ast
import re


def statement_text(original: str, assumptions=()) -> str:
    """Keep the source task visible and add only the missing input guarantees."""
    text = original.strip()
    if assumptions:
        text += '\n\n**Constraints:**\n\n' + '\n'.join(f'- {item}' for item in assumptions)
    return text + '\n'


def test_case_details(tests: str, test_ids) -> dict:
    """Expose the actual supplied test instead of its internal JSON selector."""
    lines = tests.splitlines()
    functions = {}
    for node in ast.parse(tests).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith('test'):
            start = min([node.lineno, *(item.lineno for item in node.decorator_list)]) - 1
            functions[node.name] = '\n'.join(lines[start:node.end_lineno])
    details = {}
    for test_id in test_ids:
        name = test_id.rsplit('::', 1)[-1].split('[', 1)[0]
        if name in functions:
            details[test_id] = {'title': test_id, 'code': functions[name]}
    return details


def course_help(source_url: str = '', note: str = '', *, testing=False) -> dict:
    if testing:
        body = ('Write tests below the marked line in the editor. Run checks the correct '
                'implementation and a sample of the faulty versions. Submit checks every version. '
                'Keep the supplied code and runner unchanged.')
    else:
        body = ('Write your implementation above the supplied tests. Run checks the sample tests. '
                'Submit checks all supplied tests. Keep the tests and runner unchanged.')
    body += ('\n\nFor an older saved solution, use **+** beside the editor tabs to open the current '
             'template. Copy your implementation into the new tab. Your old tab stays in place.')
    if note:
        body += '\n\n' + note.strip()
    if source_url:
        body += f'\n\n[Original Pybites exercise]({source_url})'
    return {'title': 'Course help', 'body': body}
