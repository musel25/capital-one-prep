"""Environment flag parsing."""
CASES = [
    {'input': {'value': ' true ', 'default': False}, 'expected': True, 'label': 'trim truthy value'},
    {'input': {'value': 'OFF', 'default': True}, 'expected': False, 'label': 'case insensitive false'},
    {'input': {'value': None, 'default': True}, 'expected': True, 'label': 'missing uses true default'},
    {'input': {'value': None, 'default': False}, 'expected': False, 'label': 'missing uses false default'},
    {'input': {'value': '', 'default': True}, 'expected': None, 'label': 'empty is invalid'},
    {'input': {'value': '  ', 'default': False}, 'expected': None, 'label': 'blank is invalid'},
    {'input': {'value': '1', 'default': False}, 'expected': True, 'label': 'numeric true token'},
    {'input': {'value': '0', 'default': True}, 'expected': False, 'label': 'numeric false token'},
    {'input': {'value': 'YeS', 'default': False}, 'expected': True, 'label': 'yes token'},
    {'input': {'value': 'no', 'default': True}, 'expected': False, 'label': 'no token'},
    {'input': {'value': '\ton\n', 'default': False}, 'expected': True, 'label': 'on token'},
    {'input': {'value': 'False', 'default': True}, 'expected': False, 'label': 'false token'},
    {'input': {'value': 'enabled', 'default': True}, 'expected': None, 'label': 'unknown token rejects'},
    {'input': {'value': 'true false', 'default': False}, 'expected': None, 'label': 'do not parse prefixes'},
]

SPEC = {
    'number': 2, 'slug': 'parse-environment-flag', 'title': 'Parse an environment flag',
    'difficulty': 'Easy', 'category': '01-data-and-api', 'function': 'parse_flag',
    'ticket': 'A service must parse feature flags from environment variables.',
    'task': 'Given `value` and a boolean `default`, return the parsed flag. If `value` is `None`, return `default`. Otherwise, remove surrounding spaces, tabs, carriage returns, and newlines. Compare without letter case. `true`, `1`, `yes`, and `on` mean `True`. `false`, `0`, `no`, and `off` mean `False`. Return `None` for every other string, including an empty string.',
    'constraints': ['`value` is `None` or an ASCII string with at most 100 characters.', '`default` is a boolean.'],
    'starter': 'def parse_flag(value, default):\n    raise NotImplementedError\n',
    'reference': '''def parse_flag(value, default):
    if value is None:
        return default
    value = value.strip(" \\t\\r\\n").lower()
    if value in {"true", "1", "yes", "on"}:
        return True
    if value in {"false", "0", "no", "off"}:
        return False
    return None
''',
    'java': '''public Object solve(Map<String,Object> d) {
        Object v=d.get("value"); if(v==null) return d.get("default");
        String token=s(v).replaceAll("^[ \\t\\r\\n]+|[ \\t\\r\\n]+$", "").toLowerCase(Locale.ROOT);
        if(Arrays.asList("true","1","yes","on").contains(token)) return true;
        if(Arrays.asList("false","0","no","off").contains(token)) return false;
        return null;
    }''',
    'cases': CASES,
    'mutations': [
        {'name': 'always uses false default', 'old': 'return default', 'new': 'return False'},
        {'name': 'does not normalize case', 'old': '.lower()', 'new': ''},
        {'name': 'accepts invalid values as default', 'old': 'return None', 'new': 'return default'},
        {'name': 'omits numeric truth token', 'old': '"true", "1", "yes", "on"', 'new': '"true", "yes", "on"'},
    ],
}
