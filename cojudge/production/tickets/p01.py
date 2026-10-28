"""Notification email cleanup: explicit expectations precede the implementation."""
CASES = [
    {'input': {'emails': [' ADA@EXAMPLE.COM ', 'ada@example.com', 'bob@example.com']}, 'expected': ['ada@example.com', 'bob@example.com'], 'label': 'normalize then deduplicate'},
    {'input': {'emails': []}, 'expected': [], 'label': 'empty batch'},
    {'input': {'emails': ['', ' ', '\t\r\n']}, 'expected': [], 'label': 'blank entries'},
    {'input': {'emails': ['A@B']}, 'expected': ['a@b'], 'label': 'one address'},
    {'input': {'emails': ['z@b', 'a@b']}, 'expected': ['z@b', 'a@b'], 'label': 'retain input order'},
    {'input': {'emails': ['a@b', 'a@b', 'a@b']}, 'expected': ['a@b'], 'label': 'repeated address'},
    {'input': {'emails': ['\ta@b\n', ' a@b\r']}, 'expected': ['a@b'], 'label': 'trim permitted whitespace'},
    {'input': {'emails': ['', 'X+tag@B', '']}, 'expected': ['x+tag@b'], 'label': 'keep plus tag'},
    {'input': {'emails': ['A.B@C', 'ab@c']}, 'expected': ['a.b@c', 'ab@c'], 'label': 'do not remove dots'},
    {'input': {'emails': ['first', 'SECOND']}, 'expected': ['first', 'second'], 'label': 'no syntax validation'},
    {'input': {'emails': ['a @b']}, 'expected': ['a @b'], 'label': 'preserve internal whitespace'},
    {'input': {'emails': ['B', 'a', 'B', 'C', 'A']}, 'expected': ['b', 'a', 'c'], 'label': 'nonadjacent duplicates'},
]

SPEC = {
    'number': 1, 'slug': 'clean-notification-emails', 'title': 'Clean notification emails',
    'difficulty': 'Easy', 'category': '01-data-and-api', 'function': 'clean_emails',
    'ticket': 'The notification service receives duplicate email addresses from an import.',
    'task': 'Given a list of strings `emails`, return the cleaned addresses. Remove leading and trailing spaces, tabs, carriage returns, and newlines. Convert letters to lowercase. Skip empty results. Keep each cleaned address once, in its first input position. Do not validate email syntax or remove internal characters.',
    'constraints': ['`0 <= len(emails) <= 1000`.', 'Each item is an ASCII string with at most 200 characters. Empty strings are allowed.'],
    'starter': 'def clean_emails(emails):\n    raise NotImplementedError\n',
    'reference': '''def clean_emails(emails):
    out, seen = [], set()
    for email in emails:
        email = email.strip(" \\t\\r\\n").lower()
        if email and email not in seen:
            seen.add(email)
            out.append(email)
    return out
''',
    'java': '''public Object solve(Map<String,Object> d) {
        List<Object> out = new ArrayList<>(); Set<String> seen = new HashSet<>();
        for(Object v: arr(d.get("emails"))) {
            String e=s(v).replaceAll("^[ \\t\\r\\n]+|[ \\t\\r\\n]+$", "").toLowerCase(Locale.ROOT);
            if(!e.isEmpty() && seen.add(e)) out.add(e);
        } return out;
    }''',
    'cases': CASES,
    'mutations': [
        {'name': 'does not normalize case', 'old': '.lower()', 'new': ''},
        {'name': 'keeps duplicate emails', 'old': 'email not in seen', 'new': 'True'},
        {'name': 'sorts addresses', 'old': 'return out', 'new': 'return sorted(out)'},
        {'name': 'keeps blank entries', 'old': 'if email and email not in seen:', 'new': 'if email not in seen:'},
    ],
}
