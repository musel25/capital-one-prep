"""Readable ticket text and calls, separate from execution and grading."""
from pprint import pformat
from textwrap import indent



from cojudge.production.guide import GUIDES


def _example_call(function, data):
    arguments = []
    for name, value in data.items():
        argument = f'{name}={pformat(value, width=68, sort_dicts=False)}'
        arguments.append(indent(argument, '    '))
    return function + '(\n' + ',\n'.join(arguments) + '\n)'


def statement(spec):
    guide = GUIDES[spec['number']]
    text = (f"**The ticket.** {guide['ticket']}\n\n"
            f"**Why it matters.** {guide['why']}\n\n"
            f"### Your task\n\n{guide['task']}\n\n**Constraints:**\n\n")
    return text + '\n'.join('- ' + item for item in guide['constraints']) + '\n'


def solution(spec):
    guide = GUIDES[spec['number']]
    text = f"## How it works\n\n{guide['explanation']}\n\n## Common mistakes\n\n"
    text += '\n'.join('- ' + item for item in guide['mistakes']) + '\n\n## Solution\n\n'
    if 'simple_solution' in guide:
        text += f"```python\n{guide['simple_solution'].strip()}\n```\n\n{guide['simple_solution_note']}\n\n"
    return text + f"```python\n{spec['reference'].strip()}\n```\n"


def present(spec):
    return {
        'statement': statement(spec),
        'examples': [{'input': _example_call(spec['function'], case['input']),
                      'output': repr(case['expected']), 'explanation': case['label']}
                     for case in spec['cases'][:3]],
        'testCaseDescriptions': {},
        'courseHelp': {
            'title': 'Course help',
            'body': ('Write your code in the function at the top of the editor. Follow the numbered steps '
                     'and replace each TODO. Run checks the three examples. Submit checks all cases, '
                     'including edge cases. Open the hints one at a time if you are stuck.\n\n'
                     'Keep the adapter class at the bottom unchanged. It reads the input, calls your '
                     'function, and rejects changes to the input. Python 3.11 and the standard library.'),
        },
    }
