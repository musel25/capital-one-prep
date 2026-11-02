"""Build and verify the Python First Steps course as CoJudge script problems.

Script problems (`"scriptMode": true`, CoJudge commit 5bc43f0 or later) run the
learner's whole file. Each test gives the program its input on stdin. The
judge compares the printed text with Marker.java's independent Java version.
"""
from __future__ import annotations

import base64
import subprocess
import sys
import tempfile
from pathlib import Path

from cojudge.authoring.support import ROOT, write_json
from cojudge.first_steps.exercises import EXERCISES

COURSE_ID = 'python-first-steps'
PREFIX = 'pfs'
PYTHON = subprocess.run(['uv', 'python', 'find', '3.11'], capture_output=True, text=True).stdout.strip() or sys.executable
# Same start code as the judge: run Solution.py, and do not print input() questions.
START = ("import builtins, runpy, sys\n_read = builtins.input\n"
         "builtins.input = lambda prompt='': _read()\nsys.argv = ['Solution.py']\n"
         "runpy.run_path('Solution.py', run_name='__main__')\n")
CATEGORIES = ['01-print', '02-variables', '03-input', '04-if-else', '05-elif', '06-and-or', '07-projects']

MARKER = '''import java.util.*;

// Independent Java version of the exercise. It returns the text the program must print.
class Marker {
    private String[] lines;
    private StringBuilder out;

    private int num(int i) { return Integer.parseInt(lines[i].trim()); }
    private String line(int i) { return lines[i]; }

    // Like Python print(): one space between the parts, then a new line.
    private void say(Object... parts) {
        StringBuilder text = new StringBuilder();
        for (int i = 0; i < parts.length; i++) {
            if (i > 0) text.append(' ');
            text.append(parts[i]);
        }
        out.append(text).append('\\n');
    }

    private void run() {
        %BODY%
    }

    public String program(String input) {
        lines = (input == null ? "" : input).replace("\\r\\n", "\\n").split("\\n", -1);
        out = new StringBuilder();
        try {
            run();
        } catch (RuntimeException e) {
            return "(This test input does not fit this exercise.)";
        }
        return clean(out.toString());
    }

    // Spaces at the end of a line and empty lines at the end do not count.
    static String clean(String text) {
        if (text == null) return "";
        String[] rows = text.replace("\\r\\n", "\\n").split("\\n", -1);
        List<String> kept = new ArrayList<>();
        for (String row : rows) kept.add(row.replaceAll("[ \\t]+$", ""));
        while (!kept.isEmpty() && kept.get(kept.size() - 1).isEmpty()) kept.remove(kept.size() - 1);
        return String.join("\\n", kept);
    }

    public boolean isCorrect(String input, String output) {
        return program(input).equals(clean(output));
    }
}
'''

CHECK_MAIN = '''import java.nio.file.*;
import java.util.*;

public class CheckMain {
    static String dec(String s) { return new String(Base64.getDecoder().decode(s), java.nio.charset.StandardCharsets.UTF_8); }
    static String enc(String s) { return Base64.getEncoder().encodeToString(s.getBytes(java.nio.charset.StandardCharsets.UTF_8)); }
    public static void main(String[] args) throws Exception {
        Marker marker = new Marker();
        for (String row : Files.readAllLines(Path.of("cases.txt"))) {
            String[] part = row.split("\\t", -1);
            String input = dec(part[0]);
            System.out.println(marker.isCorrect(input, dec(part[1])) + "\\t" + enc(marker.program(input)));
        }
    }
}
'''

COURSE_HELP = {
    'title': 'How this course works',
    'body': (
        'Write your program in the editor. Press **Run** to try the sample tests. '
        'Press **Submit** to check all tests. A green check means your program printed the right text.\n\n'
        'Each test can type an **input** for your program. `input()` reads one line of it. '
        'Big and small letters, spaces between words, and punctuation must match. '
        'Spaces at the end of a line do not matter.\n\n'
        'If you see `Error on line 3`, look at line 3 of your code. Check quotes, `:`, '
        'and the 4 spaces in front of lines inside an `if`.\n\n'
        'Stuck? Open a hint. The solution tab shows one correct answer. Try first!'
    ),
}


def problem_id(number, spec):
    return f"{PREFIX}-{number:02d}-{spec['slug']}"


def numbered():
    return list(enumerate(EXERCISES, start=1))


def clean(text):
    rows = [row.rstrip(' \t') for row in text.replace('\r\n', '\n').split('\n')]
    while rows and not rows[-1]:
        rows.pop()
    return '\n'.join(rows)


def run_program(code, stdin):
    """Run a program like the judge does. Returns printed text, or an error marker."""
    with tempfile.TemporaryDirectory(prefix='pfs-') as work:
        (Path(work) / 'Solution.py').write_text(code)
        text = stdin + '\n' if stdin and not stdin.endswith('\n') else stdin
        done = subprocess.run([PYTHON, '-B', '-c', START], cwd=work, input=text,
                              capture_output=True, text=True, timeout=10)
        if done.returncode:
            return done.stdout.rstrip('\n') + '\n<error> ' + done.stderr.strip().splitlines()[-1]
        return done.stdout.replace('\r\n', '\n').rstrip('\n')


def java_marker(spec):
    body = spec['java'].strip()
    return MARKER.replace('%BODY%', body)


def java_check(spec, pairs):
    """Run Marker.isCorrect and Marker.program for (input, candidate output) pairs."""
    with tempfile.TemporaryDirectory(prefix='pfs-java-') as work:
        folder = Path(work)
        (folder / 'Marker.java').write_text(java_marker(spec))
        (folder / 'CheckMain.java').write_text(CHECK_MAIN)
        b64 = lambda s: base64.b64encode(s.encode()).decode()
        (folder / 'cases.txt').write_text(''.join(f'{b64(i)}\t{b64(o)}\n' for i, o in pairs))
        subprocess.run(['javac', 'Marker.java', 'CheckMain.java'], cwd=folder, check=True,
                       capture_output=True, text=True)
        done = subprocess.run(['java', 'CheckMain'], cwd=folder, check=True, capture_output=True, text=True)
        rows = [row.split('\t') for row in done.stdout.splitlines()]
        return [(verdict == 'true', base64.b64decode(answer).decode()) for verdict, answer in rows]


def verify(number, spec):
    pid = problem_id(number, spec)
    assert spec['category'] in CATEGORIES, pid
    assert '---' not in spec['reference'], f'{pid}: output must not contain the judge separator'
    tests = spec['tests']
    reference = [run_program(spec['reference'], stdin) for stdin in tests]
    for stdin, output in zip(tests, reference):
        assert '<error>' not in output, f'{pid}: reference failed for {stdin!r}: {output}'
        assert '---' not in output, pid
    starter = [run_program(spec['starter'], stdin) for stdin in tests]
    faults = {name: [run_program(spec['reference'].replace(old, new, 1), stdin) for stdin in tests]
              for name, old, new in spec['faults']}
    for name, old, _ in spec['faults']:
        assert old in spec['reference'], f'{pid}: fault target missing: {name}'
    # One Java run checks every candidate: reference, starter and faults.
    candidates = [reference, starter, *faults.values()]
    pairs = [(stdin, outputs[i]) for outputs in candidates for i, stdin in enumerate(tests)]
    verdicts = java_check(spec, pairs)
    size = len(tests)
    groups = [verdicts[k * size:(k + 1) * size] for k in range(len(candidates))]
    for (ok, expected), stdin, output in zip(groups[0], tests, reference):
        assert ok and expected == clean(output), (
            f'{pid}: Java and Python disagree for {stdin!r}\nPython: {output!r}\nJava:   {expected!r}')
    assert not all(ok for ok, _ in groups[1]), f'{pid}: the starter passes every test'
    for (name, _, _), group in zip(spec['faults'], groups[2:]):
        assert not all(ok for ok, _ in group), f'{pid}: fault not detected: {name}'
    return {'id': pid, 'cases': size, 'outputs': reference,
            'starter_failures': sum(not ok for ok, _ in groups[1]), 'faults': len(spec['faults'])}


def example_input(stdin):
    return stdin if stdin else '(no input)'


def build_problem(number, spec, destination=ROOT / 'cojudge'):
    result = verify(number, spec)
    pid = result['id']
    folder = Path(destination) / 'problems' / pid
    folder.mkdir(parents=True, exist_ok=True)
    samples = spec.get('samples', 1)
    tests = [{'input': stdin} for stdin in spec['tests']]
    metadata = {
        'id': pid, 'title': f"{number:02d}. {spec['title']}",
        'difficulty': spec.get('difficulty', 'Easy'), 'link': '', 'category': spec['category'],
        'examples': [{'input': example_input(stdin), 'output': output}
                     for stdin, output in list(zip(spec['tests'], result['outputs']))[:samples]],
        'starterCode': {'python': spec['starter']},
        'testCases': tests[:samples],
        'functionName': 'program', 'params': [{'name': 'input', 'type': 'string'}], 'outputType': 'string',
        'scriptMode': True,
        'courseHelp': COURSE_HELP,
        'hints': spec.get('hints', []),
    }
    write_json(folder / 'metadata.json', metadata)
    write_json(folder / 'official-tests.json', tests)
    (folder / 'statement.md').write_text(
        f"## Learn\n\n{spec['lesson'].strip()}\n\n"
        f"## Your task\n\n{spec['task'].strip()}\n")
    (folder / 'Marker.java').write_text(java_marker(spec))
    (folder / 'solution.md').write_text(
        '## One correct answer\n\nTry the exercise first. There are many correct answers.\n\n'
        f"```python\n{spec['reference'].strip()}\n```\n")
    return result


def course_info():
    return {
        'title': 'Python First Steps',
        'description': ('25 tiny Python exercises for a complete beginner. Start with print(), '
                        'then variables, input(), if/else, elif, and/or, and two small games. '
                        'Each exercise teaches one new idea. Select Python.'),
        'category-order': CATEGORIES,
        'problems-of-category': {
            category: [problem_id(n, spec) for n, spec in numbered() if spec['category'] == category]
            for category in CATEGORIES
        },
    }
