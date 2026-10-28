"""Compare semantic version precedence."""

CASES = [
    {"label": "equal release versions", "input": {"left": "1.2.3", "right": "1.2.3"}, "expected": 0},
    {"label": "core numbers use numeric comparison", "input": {"left": "1.10.0", "right": "1.9.9"}, "expected": 1},
    {"label": "prerelease precedes its release", "input": {"left": "1.0.0-alpha", "right": "1.0.0"}, "expected": -1},
    {"label": "core takes precedence over prerelease", "input": {"left": "2.0.0-alpha", "right": "1.999.999"}, "expected": 1},
    {"label": "zero core and patch difference", "input": {"left": "0.0.0", "right": "0.0.1"}, "expected": -1},
    {"label": "maximum core number", "input": {"left": "1000000000.0.0", "right": "999999999.1000000000.1000000000"}, "expected": 1},
    {"label": "build metadata is ignored on releases", "input": {"left": "1.2.3+001", "right": "1.2.3+build-002"}, "expected": 0},
    {"label": "build metadata is ignored on prereleases", "input": {"left": "1.2.3-alpha.1+001", "right": "1.2.3-alpha.1+other"}, "expected": 0},
    {"label": "numeric prerelease identifiers compare numerically", "input": {"left": "1.0.0-2", "right": "1.0.0-11"}, "expected": -1},
    {"label": "numeric prerelease identifiers reverse comparison", "input": {"left": "1.0.0-11", "right": "1.0.0-2"}, "expected": 1},
    {"label": "numeric identifier precedes text", "input": {"left": "1.0.0-9", "right": "1.0.0-alpha"}, "expected": -1},
    {"label": "text identifier follows numeric", "input": {"left": "1.0.0-alpha", "right": "1.0.0-9"}, "expected": 1},
    {"label": "shorter equal prerelease prefix precedes", "input": {"left": "1.0.0-alpha", "right": "1.0.0-alpha.1"}, "expected": -1},
    {"label": "longer equal prerelease prefix follows", "input": {"left": "1.0.0-alpha.1", "right": "1.0.0-alpha"}, "expected": 1},
    {"label": "first differing text identifier decides", "input": {"left": "1.0.0-alpha.beta", "right": "1.0.0-beta"}, "expected": -1},
    {"label": "later numeric identifier decides", "input": {"left": "1.0.0-beta.2", "right": "1.0.0-beta.11"}, "expected": -1},
    {"label": "ASCII uppercase precedes lowercase", "input": {"left": "1.0.0-A", "right": "1.0.0-a"}, "expected": -1},
    {"label": "hyphen identifier is not numeric", "input": {"left": "1.0.0--", "right": "1.0.0-0"}, "expected": 1},
    {"label": "hyphen follows ASCII lexical ordering", "input": {"left": "1.0.0-alpha-2", "right": "1.0.0-alpha2"}, "expected": -1},
    {"label": "numeric prerelease can exceed machine integers", "input": {"left": "1.0.0-999999999999999999999999", "right": "1.0.0-1000000000000000000000000"}, "expected": -1},
    {"label": "equal multi-part prereleases", "input": {"left": "0.0.0-x.7.z.92", "right": "0.0.0-x.7.z.92"}, "expected": 0},
    {"label": "release follows its prerelease", "input": {"left": "1.0.0", "right": "1.0.0-rc.1"}, "expected": 1},
]

SPEC = {
    "number": 21,
    "slug": "compare-semantic-versions",
    "title": "Compare release versions correctly",
    "difficulty": "Medium",
    "category": "06-application-logic",
    "ticket": "The update service must compare semantic versions without treating numeric components as plain text.",
    "task": "Implement `compare_versions(left, right)` for valid SemVer 2.0.0 strings. Return -1 if left precedes right, 1 if it follows, or 0 for equal precedence. Compare major, minor, then patch numerically. A release follows every prerelease with the same core. Compare prerelease identifiers from left to right: numeric identifiers compare numerically and precede nonnumeric identifiers; other identifiers use ASCII lexical order. If all shared identifiers are equal, the shorter prerelease precedes the longer one. Ignore build metadata after `+`. Inputs are guaranteed valid; do not add validation.",
    "constraints": ["Each input is an ASCII SemVer 2.0.0 string of at most 100 characters.", "Core numbers are canonical nonnegative integers through 1000000000.", "Prerelease identifiers contain ASCII letters, digits, or hyphens; numeric identifiers have no leading zeros.", "Build identifiers can have leading zeros."],
    "function": "compare_versions",
    "starter": "def compare_versions(left, right):\n    raise NotImplementedError\n",
    "reference": '''def compare_versions(left, right):
    def parse(value):
        core, separator, prerelease = value.split("+", 1)[0].partition("-")
        return tuple(map(int, core.split("."))), prerelease.split(".") if separator else None

    left_core, left_pre = parse(left)
    right_core, right_pre = parse(right)
    if left_core != right_core:
        return (left_core > right_core) - (left_core < right_core)
    if left_pre is None:
        return 0 if right_pre is None else 1
    if right_pre is None:
        return -1
    for a, b in zip(left_pre, right_pre):
        if a == b:
            continue
        if a.isdigit() and b.isdigit():
            return (int(a) > int(b)) - (int(a) < int(b))
        if a.isdigit() != b.isdigit():
            return -1 if a.isdigit() else 1
        return (a > b) - (a < b)
    return (len(left_pre) > len(right_pre)) - (len(left_pre) < len(right_pre))
''',
    "java": r'''public Object solve(Map<String,Object> d) {
    String[] versions = {s(d.get("left")), s(d.get("right"))};
    String[][] core = new String[2][];
    String[][] pre = new String[2][];
    for (int i = 0; i < 2; i++) {
        String value = versions[i];
        int plus = value.indexOf('+');
        if (plus >= 0) value = value.substring(0, plus);
        int dash = value.indexOf('-');
        if (dash >= 0) {
            pre[i] = value.substring(dash + 1).split("\\.");
            value = value.substring(0, dash);
        }
        core[i] = value.split("\\.");
    }
    for (int i = 0; i < 3; i++) {
        int comparison = Integer.compare(Integer.parseInt(core[0][i]), Integer.parseInt(core[1][i]));
        if (comparison != 0) return comparison;
    }
    if (pre[0] == null) return pre[1] == null ? 0 : 1;
    if (pre[1] == null) return -1;
    for (int i = 0; i < Math.min(pre[0].length, pre[1].length); i++) {
        String a = pre[0][i], b = pre[1][i];
        if (a.equals(b)) continue;
        boolean numericA = a.matches("[0-9]+"), numericB = b.matches("[0-9]+");
        if (numericA && numericB) return new BigInteger(a).compareTo(new BigInteger(b));
        if (numericA != numericB) return numericA ? -1 : 1;
        return Integer.signum(a.compareTo(b));
    }
    return Integer.compare(pre[0].length, pre[1].length);
}''',
    "cases": CASES,
    "mutations": [
        {"name": "compare core components as text", "old": 'tuple(map(int, core.split(".")))', "new": 'tuple(core.split("."))'},
        {"name": "put a release before its prerelease", "old": "return 0 if right_pre is None else 1", "new": "return 0 if right_pre is None else -1"},
        {"name": "compare numeric prerelease identifiers as text", "old": "return (int(a) > int(b)) - (int(a) < int(b))", "new": "return (a > b) - (a < b)"},
        {"name": "include build metadata in precedence", "old": 'value.split("+", 1)[0].partition("-")', "new": 'value.partition("-")'},
        {"name": "reverse equal-prefix length ordering", "old": "return (len(left_pre) > len(right_pre)) - (len(left_pre) < len(right_pre))", "new": "return (len(left_pre) < len(right_pre)) - (len(left_pre) > len(right_pre))"},
    ],
}
