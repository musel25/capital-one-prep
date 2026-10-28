"""A create-user endpoint validates three fields in a fixed order."""
CASES = [
    {'input': {'payload': {'name': 'Ada', 'email': 'a@b', 'age': 0}}, 'expected': [], 'label': 'valid age zero'},
    {'input': {'payload': {}}, 'expected': ['name', 'email'], 'label': 'missing required fields'},
    {'input': {'payload': {'name': '', 'email': ''}}, 'expected': ['name', 'email'], 'label': 'empty strings'},
    {'input': {'payload': {'name': ' \t', 'email': 'a@b'}}, 'expected': ['name'], 'label': 'blank name'},
    {'input': {'payload': {'name': 'A', 'email': '@b'}}, 'expected': ['email'], 'label': 'missing local part'},
    {'input': {'payload': {'name': 'A', 'email': 'a@'}}, 'expected': ['email'], 'label': 'missing domain'},
    {'input': {'payload': {'name': 'A', 'email': 'a@@b'}}, 'expected': ['email'], 'label': 'multiple separators'},
    {'input': {'payload': {'name': 'A', 'email': ' a@b'}}, 'expected': ['email'], 'label': 'do not trim email'},
    {'input': {'payload': {'name': 'A', 'email': 'a@b', 'age': True}}, 'expected': ['age'], 'label': 'bool is not an age'},
    {'input': {'payload': {'name': 'A', 'email': 'a@b', 'age': 1.0}}, 'expected': ['age'], 'label': 'float is not integer'},
    {'input': {'payload': {'name': 'A', 'email': 'a@b', 'age': -1}}, 'expected': ['age'], 'label': 'negative age'},
    {'input': {'payload': {'name': None, 'email': 1, 'age': None}}, 'expected': ['name', 'email', 'age'], 'label': 'all invalid in fixed order'},
    {'input': {'payload': {'name': ' A ', 'email': 'a@b', 'extra': False}}, 'expected': [], 'label': 'ignore unknown fields'},
    {'input': {'payload': {'name': 1, 'email': True, 'age': '4'}}, 'expected': ['name', 'email', 'age'], 'label': 'no type coercion'},
    {'input': {'payload': {'name': 'A', 'email': 'a@b\nc'}}, 'expected': ['email'], 'label': 'reject embedded whitespace'},
]

SPEC = {
    'number': 3, 'slug': 'validate-create-user', 'title': 'Validate a create-user request',
    'difficulty': 'Easy', 'category': '01-data-and-api', 'function': 'validate_user',
    'ticket': 'The create-user endpoint must report invalid fields before it writes a record.',
    'task': 'Given a dictionary `payload`, return a list of invalid field names in this order: `name`, `email`, `age`.\n\n- `name` is required. It must be a string that is nonempty after removal of surrounding spaces, tabs, carriage returns, and newlines.\n- `email` is required. It must be a string with exactly one `@`, nonempty parts on both sides, and no spaces, tabs, carriage returns, or newlines. Do not apply other email rules.\n- `age` is optional. If present, it must be an integer of zero or more. Booleans and floats are invalid.\n\nIgnore other fields. Return an empty list for a valid request. Do not convert field types.',
    'constraints': ['`payload` is a JSON object with at most 20 fields.', 'String values and keys contain ASCII characters. String values have at most 200 characters.', 'Numeric values are between -1000000 and 1000000. Missing fields and `None` are allowed.'],
    'starter': 'def validate_user(payload):\n    raise NotImplementedError\n',
    'reference': '''def validate_user(payload):
    errors = []
    name = payload.get("name")
    if not isinstance(name, str) or not name.strip(" \\t\\r\\n"):
        errors.append("name")
    email = payload.get("email")
    valid_email = isinstance(email, str) and email.count("@") == 1
    if valid_email:
        local, domain = email.split("@")
        valid_email = bool(local and domain) and not any(c in " \\t\\r\\n" for c in email)
    if not valid_email:
        errors.append("email")
    if "age" in payload and (type(payload["age"]) is not int or payload["age"] < 0):
        errors.append("age")
    return errors
''',
    'java': '''public Object solve(Map<String,Object> d) {
        Map<String,Object> p=obj(d.get("payload")); List<Object> out=new ArrayList<>();
        Object name=p.get("name"), email=p.get("email"), age=p.get("age");
        if(!(name instanceof String) || s(name).replaceAll("^[ \\t\\r\\n]+|[ \\t\\r\\n]+$", "").isEmpty()) out.add("name");
        if(!(email instanceof String) || !s(email).matches("[^@ \\t\\r\\n]+@[^@ \\t\\r\\n]+")) out.add("email");
        if(p.containsKey("age") && (!isInteger(age) || lng(age)<0)) out.add("age");
        return out;
    }''',
    'cases': CASES,
    'mutations': [
        {'name': 'accepts boolean age', 'old': 'type(payload["age"]) is not int', 'new': 'not isinstance(payload["age"], int)'},
        {'name': 'accepts empty name', 'old': 'or not name.strip(" \\t\\r\\n")', 'new': ''},
        {'name': 'rejects valid zero age', 'old': 'payload["age"] < 0', 'new': 'payload["age"] <= 0'},
        {'name': 'misses missing email', 'old': 'if not valid_email:', 'new': 'if "email" in payload and not valid_email:'},
    ],
}
