"""Learner-facing text for the Software Engineering Tickets course.

Each guide explains one ticket in plain, short sentences: the ticket, why it
matters in production, numbered rules, a step-by-step starter, three hints
(concept -> mechanics -> detail), and an explained solution. Test cases,
references, Java markers, and faults stay in tickets/pNN.py.
"""

# Course order: (ticket file number, category). Display numbers are 01-15.
ORDER = [
    (1, '01-clean-input'), (2, '01-clean-input'), (3, '01-clean-input'),
    (5, '02-data-and-apis'), (6, '02-data-and-apis'), (18, '02-data-and-apis'), (7, '02-data-and-apis'),
    (8, '03-reliability'), (10, '03-reliability'), (11, '03-reliability'), (13, '03-reliability'),
    (19, '04-security-and-money'), (24, '04-security-and-money'), (20, '04-security-and-money'),
    (16, '04-security-and-money'),
]
CATEGORIES = ['01-clean-input', '02-data-and-apis', '03-reliability', '04-security-and-money']
# Tickets that repeat another ticket or Pybites, or are too specialized.
RETIRED = [4, 9, 12, 14, 15, 17, 21, 22, 23]

GUIDES = {
    1: {
        'ticket': 'An import gives the notification service a list of email addresses. Some addresses are duplicates with different spaces or letter case.',
        'why': 'If you do not clean the list, one person gets the same email two or three times.',
        'task': '''Write `clean_emails(emails)`. Return a list of clean addresses.

1. Remove whitespace at the start and the end of each address.
2. Change the letters to lowercase.
3. Skip the address if it is now empty.
4. Skip the address if you already have it.
5. Keep the order in which the addresses first appear. Do not sort.

Do not check if an address is valid. Keep the characters inside an address unchanged: `a.b@c` stays `a.b@c`.''',
        'constraints': ['`emails` has 0–1000 strings. Each string has at most 200 ASCII characters.'],
        'starter': '''def clean_emails(emails):
    """Return clean addresses, without duplicates, in first-seen order.

    clean_emails([' ADA@EXAMPLE.COM ', 'ada@example.com', 'bob@example.com'])
    -> ['ada@example.com', 'bob@example.com']
    """
    result = []    # the clean addresses, in order
    seen = set()   # the addresses that are already in result (fast lookup)

    for email in emails:
        # Step 1: clean the address.
        #         Remove whitespace at both ends, then make it lowercase.
        cleaned = email  # TODO

        # Step 2: skip it when it is empty or already in `seen`.
        #         `continue` goes to the next email.
        # TODO

        # Step 3: keep it.
        # TODO: add `cleaned` to `seen` and append it to `result`.

    return result
''',
        'hints': [
            'Use two containers: a list keeps the order, and a set answers "do I already have it?" quickly.',
            '`email.strip()` removes whitespace at both ends. `.lower()` changes the case. You can chain them: `email.strip().lower()`.',
            'An empty string is falsy, so one check covers both skips: `if not cleaned or cleaned in seen: continue`.',
        ],
        'explanation': '''Loop over the addresses once. Clean each address, then use a set to see if you already have it. The list keeps the first-seen order.''',
        'mistakes': [
            'Sorting the result. The order must stay as in the input.',
            'Checking for duplicates before you lowercase. Then `ADA@X` and `ada@x` both stay.',
            'Keeping empty entries such as `" "`.',
        ],
    },
    2: {
        'ticket': 'A service reads feature flags from environment variables, for example `NEW_CHECKOUT=yes`.',
        'why': 'Environment variables are always text. `bool("false")` is `True`, because every nonempty string is truthy. A service that uses `bool(value)` turns on a feature by mistake.',
        'task': '''Write `parse_flag(value, default)`. Return `True`, `False`, or `None`.

1. If `value` is `None` (the variable is not set), return `default`.
2. Otherwise, remove whitespace at both ends and change the text to lowercase.
3. `true`, `1`, `yes`, and `on` return `True`.
4. `false`, `0`, `no`, and `off` return `False`.
5. Every other text, also an empty string, returns `None` (invalid).''',
        'constraints': ['`value` is `None` or a string with at most 100 ASCII characters.', '`default` is `True` or `False`.'],
        'starter': '''TRUE_WORDS = {"true", "1", "yes", "on"}
FALSE_WORDS = {"false", "0", "no", "off"}


def parse_flag(value, default):
    """Turn environment-variable text into True, False, or None.

    parse_flag(' true ', False) -> True
    parse_flag('OFF', True)     -> False
    parse_flag(None, True)      -> True      (not set: use the default)
    parse_flag('enabled', True) -> None      (invalid)
    """
    # Step 1: the variable is not set.
    # TODO: if value is None, return default.

    # Step 2: clean the text: whitespace at both ends, then lowercase.
    text = value  # TODO

    # Step 3: look up the clean text.
    # TODO: return True if text is in TRUE_WORDS.
    # TODO: return False if text is in FALSE_WORDS.

    # Step 4: every other text is invalid.
    return None
''',
        'hints': [
            'Never use `bool(value)` on text. Compare the text with known words.',
            'Check `value is None` first. Call string methods only after that check, because `None` has no `.strip()`.',
            '`text = value.strip().lower()`, then `if text in TRUE_WORDS: return True`.',
        ],
        'explanation': '''Handle the missing value first. Then clean the text and look it up in two sets of known words. Anything else is invalid, so the caller can report a configuration error.''',
        'mistakes': [
            'Returning `default` for invalid text. Invalid text must return `None`.',
            'Forgetting to lowercase, so `OFF` is invalid.',
            'Forgetting the words `1` and `0`.',
        ],
    },
    3: {
        'ticket': 'The create-user endpoint must reject bad input before it saves a user.',
        'why': 'Bad data in a database causes errors later, far from the cause. Report all bad fields at once, so the client can fix them in one try.',
        'task': '''Write `validate_user(payload)`. Return a list with the names of the invalid fields, in the order `name`, `email`, `age`. Return `[]` when all fields are valid.

1. `name` is required. It must be a string. After `.strip()`, it must not be empty.
2. `email` is required. It must be a string with exactly one `@`, text before and after the `@`, and no whitespace (space, tab, `\\r`, `\\n`). Do not strip the email.
3. `age` is optional. If the key is there, the value must be an `int` that is `0` or more. `True`, `1.0`, `"4"`, and `None` are not valid ages.
4. Ignore all other fields. Do not convert types.''',
        'constraints': ['`payload` is a dictionary with at most 20 fields. Values can be any JSON value.'],
        'starter': '''def validate_user(payload):
    """Return the invalid field names, in the order name, email, age.

    validate_user({'name': 'Ada', 'email': 'a@b', 'age': 0}) -> []
    validate_user({})                                         -> ['name', 'email']
    validate_user({'name': 'A', 'email': 'a@b', 'age': True}) -> ['age']
    """
    errors = []

    # Step 1: name. payload.get returns None when the key is missing.
    name = payload.get("name")
    # TODO: append "name" if name is not a str, or name.strip() is empty.

    # Step 2: email.
    email = payload.get("email")
    # TODO: the email is valid only if ALL of these are true:
    #       - it is a str
    #       - email.count("@") == 1
    #       - both parts of email.split("@") are nonempty
    #       - no character of email is in " \\t\\r\\n"
    #       If it is not valid, append "email".

    # Step 3: age (optional). Check it only if "age" in payload.
    # TODO: append "age" if the value is not an int, or it is below 0.
    #       Booleans must fail. See hint 2.

    return errors
''',
        'hints': [
            '`payload.get("name")` returns `None` for a missing key. So one type check covers "missing" and "wrong type".',
            'In Python, `bool` is a kind of `int`: `isinstance(True, int)` is `True`. Use `type(age) is int` to reject `True` and `False`.',
            'For the email: check `isinstance(email, str) and email.count("@") == 1` first. Then `local, domain = email.split("@")` and require `local and domain and not any(c in " \\t\\r\\n" for c in email)`.',
        ],
        'explanation': '''Check each field on its own and append its name when it fails. Because you check the fields in a fixed order, the list is always in the order `name`, `email`, `age`.''',
        'mistakes': [
            'Using `isinstance(age, int)`, which accepts `True`.',
            'Rejecting a valid age of `0` with `if not age`.',
            'Stopping after the first error. The client needs all errors.',
        ],
    },
    5: {
        'ticket': 'The records endpoint returns records in pages. The client sends the last ID it saw, and the endpoint returns the next page.',
        'why': 'If the order is not stable, or the cursor is wrong, clients skip or repeat records. The bug is hard to see because each page looks correct.',
        'task': '''Write `paginate_records(records, after_id, limit)`. Return `{'items': [...], 'next_cursor': ...}`.

1. If `after_id` is not `None`, keep only the records with `id > after_id`. The cursor does not need to be an existing ID.
2. Sort the records by `id`, smallest first.
3. Take at most `limit` records. Keep all their fields.
4. If more records remain after this page, `next_cursor` is the `id` of the last record on the page. Otherwise it is `None`.''',
        'constraints': ['0–200 records. `id` values are unique positive integers. Records can have other fields.', '`after_id` is `None` or an integer of 0 or more. `limit` is 1–50.'],
        'starter': '''def paginate_records(records, after_id, limit):
    """Return one page of records, sorted by id, and the cursor for the next page.

    records = [{'id': 3}, {'id': 1}, {'id': 2}]
    paginate_records(records, None, 2) -> {'items': [{'id': 1}, {'id': 2}], 'next_cursor': 2}
    paginate_records(records, 1, 2)    -> {'items': [{'id': 2}, {'id': 3}], 'next_cursor': None}
    """
    # Step 1: keep only the records after the cursor.
    #         When after_id is None, keep all records.
    eligible = list(records)  # TODO: keep only rows with row["id"] > after_id

    # Step 2: sort by id, smallest first.
    # TODO

    # Step 3: take one page.
    items = eligible  # TODO: only the first `limit` records

    # Step 4: is there another page?
    # TODO: if eligible has more records than items, use the last id on the page.
    next_cursor = None

    return {"items": items, "next_cursor": next_cursor}
''',
        'hints': [
            'Filter first, then sort, then slice. A slice such as `eligible[:limit]` is safe when the list is shorter than `limit`.',
            'Sort with `eligible.sort(key=lambda row: row["id"])`. The IDs are numbers, so `10` comes after `2`.',
            'More records remain when `len(eligible) > len(items)`. Then `next_cursor = items[-1]["id"]`. A full page that is also the last page has no cursor.',
        ],
        'explanation': '''Filter by the cursor, sort, and slice. The cursor is the last ID on the page, but only when more records exist. So the client knows when to stop.''',
        'mistakes': [
            'Including the record whose ID equals the cursor. The cursor means "after this ID".',
            'Returning a cursor after the final page. The client then asks for an empty page.',
            'Sorting IDs as text, so `10` comes before `2`.',
        ],
    },
    6: {
        'ticket': 'A PATCH request changes only some user settings. A value of `null` (`None`) means "delete this setting".',
        'why': '`False`, `0`, and `""` are real values. A common bug uses `if value:` and deletes them by mistake. Then a user cannot turn a setting off.',
        'task': '''Write `apply_settings_patch(settings, patch)`. Return a new settings dictionary. Do not change the inputs.

1. Start with a copy of `settings`.
2. For each key in `patch`:
   - If the value is `None`, remove the key. If the key is not there, do nothing.
   - Otherwise, set the key to the value. This replaces an old value or adds a new key.
3. Change only the top level. A dictionary in the patch replaces the whole old value. Do not merge it.
4. Keep all other settings unchanged, also settings whose value is `None`.''',
        'constraints': ['Both arguments are dictionaries with 0–200 string keys. Values can be any JSON value.'],
        'starter': '''def apply_settings_patch(settings, patch):
    """Return new settings with the patch applied. None in the patch deletes a key.

    apply_settings_patch({'theme': 'dark', 'lang': 'en'}, {'theme': 'light'})
    -> {'theme': 'light', 'lang': 'en'}
    apply_settings_patch({'enabled': True}, {'enabled': False})
    -> {'enabled': False}        (False is a real value, not a delete)
    """
    # Step 1: copy, so the input does not change.
    result = settings  # TODO: make a copy

    for key, value in patch.items():
        # Step 2: None means "delete this key".
        #         Use `value is None`, not `not value`.
        # TODO: remove the key. result.pop(key, None) does not fail for a missing key.

        # Step 3: every other value replaces or adds the setting.
        # TODO
        pass

    return result
''',
        'hints': [
            '`dict(settings)` or `settings.copy()` makes a new dictionary. A shallow copy is enough here, because you replace values and do not change them.',
            'Use `if value is None:` and `else:`. Only `None` deletes.',
            '`result.pop(key, None)` removes a key and does nothing when the key is missing. `result[key] = value` replaces or adds.',
        ],
        'explanation': '''Copy the settings, then apply each patch entry. Only `None` deletes. Every other value, also `False`, `0`, and empty values, is stored.''',
        'mistakes': [
            'Using `if not value:`, which deletes `False`, `0`, and `""`.',
            'Storing `None` instead of deleting the key.',
            'Changing the input `settings` instead of a copy.',
        ],
    },
    18: {
        'ticket': 'Servers in different time zones send event times with an offset, for example `2026-10-28T00:30:00+02:00`. The daily report must count events per UTC day.',
        'why': 'If you take the date from the text, an event at 00:30 in Berlin counts for the wrong day. Daily totals then do not match other reports.',
        'task': '''Write `count_utc_days(timestamps)`. Return a dictionary from dates (`YYYY-MM-DD`) to counts.

1. Read each timestamp. `Z` means UTC. `+02:00` means two hours ahead of UTC.
2. Convert the time to UTC. Then take its date.
3. Count the events for each UTC date. Count duplicates separately.

Example: `2026-10-28T00:30:00+02:00` is `2026-10-27T22:30:00` in UTC, so it counts for `2026-10-27`.''',
        'constraints': ['0–200 timestamps in the form `YYYY-MM-DDTHH:MM:SS` followed by `Z`, `+HH:MM`, or `-HH:MM`.', 'Input years are 2000–2099. The UTC date can be in 1999 or 2100.'],
        'starter': '''from datetime import datetime, timezone


def count_utc_days(timestamps):
    """Count events per UTC date.

    count_utc_days(['2026-10-28T00:30:00+02:00', '2026-10-27T23:30:00Z'])
    -> {'2026-10-27': 2}
    """
    counts = {}
    for timestamp in timestamps:
        # Step 1: read the text. Python 3.11 understands the offset and "Z".
        moment = datetime.fromisoformat(timestamp)

        # Step 2: the UTC date as "YYYY-MM-DD".
        day = timestamp[:10]  # TODO: this is the LOCAL date. Convert `moment` to UTC first.

        # Step 3: add one to the count for that day.
        counts[day] = counts.get(day, 0) + 1

    return counts
''',
        'hints': [
            '`datetime.fromisoformat(text)` returns a time that knows its offset (an "aware" datetime).',
            '`moment.astimezone(timezone.utc)` converts the time to UTC. Do not use `.replace(tzinfo=...)`: it changes the label, not the time.',
            '`.date().isoformat()` gives the text `"YYYY-MM-DD"`.',
        ],
        'explanation': '''Parse each timestamp into an aware datetime, convert it to UTC, and take the date. Then count with a dictionary.''',
        'mistakes': [
            'Taking the date from the text (`timestamp[:10]`). That is the local date.',
            'Replacing the offset instead of converting the time.',
            'Overwriting a count instead of adding one.',
        ],
    },
    7: {
        'ticket': 'The request logger writes request data to the logs. It must remove passwords, tokens, and secrets first, at every level of the data.',
        'why': 'Many people can read logs, and logs are kept for a long time. A password in a log is a security incident. Request data is often nested, so a secret can be at any depth.',
        'task': '''Write `redact_secrets(value)`. The input is any JSON value: a dictionary, a list, a string, a number, a boolean, or `None`. Return a new value.

1. In a dictionary, compare each key in lowercase. If it is exactly `password`, `token`, or `secret`, replace the whole value with `'[REDACTED]'`. Keep the key as it is written.
2. Process all other dictionary values and all list items in the same way, at every depth.
3. Return strings, numbers, booleans, and `None` unchanged. Only keys are checked: a string value `'password'` stays.
4. Match whole keys only. `password_hint`, `access_token`, and `' token'` are not secret keys.''',
        'constraints': ['The data is at most 10 levels deep and has at most 1000 values. Keys are ASCII strings.'],
        'starter': '''SECRET_KEYS = {"password", "token", "secret"}


def redact_secrets(value):
    """Return a copy of value with every secret value replaced by '[REDACTED]'.

    redact_secrets({'user': 'sam', 'password': 'abc'})
    -> {'user': 'sam', 'password': '[REDACTED]'}
    redact_secrets({'events': [{'Token': 42}, 'ok']})
    -> {'events': [{'Token': '[REDACTED]'}, 'ok']}
    """
    # Step 1: a dictionary. Build a new dictionary.
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            # TODO: if key.lower() is in SECRET_KEYS, store "[REDACTED]".
            #       Otherwise store redact_secrets(item). The function calls itself.
            result[key] = item
        return result

    # Step 2: a list. Process every item in the same way.
    if isinstance(value, list):
        return value  # TODO: a new list with redact_secrets(item) for each item

    # Step 3: anything else (str, int, float, bool, None) stays unchanged.
    return value
''',
        'hints': [
            'This is recursion: the function calls itself for each nested value. The stop case is a value that is not a dictionary or a list.',
            'Compare `key.lower() in SECRET_KEYS`. Do not search inside the key: `"token" in "access_token"` is `True`.',
            'Do not process the value of a secret key. Replace the whole value, also when it is a dictionary or a list.',
        ],
        'explanation': '''The function has three cases: a dictionary, a list, and a plain value. Dictionaries and lists build new containers and call the function again for each item. Secret keys get `'[REDACTED]'` instead.''',
        'mistakes': [
            'Comparing keys with their original case, so `Token` is missed.',
            'Not looking inside lists, so `[{"token": 1}]` leaks.',
            'Stripping keys or matching parts of keys.',
        ],
    },
    8: {
        'ticket': 'The service client tries a request again when the server fails for a short time. It must wait longer before each new try, and it must stop at a limit.',
        'why': 'Without a limit, a client can try forever. Without a growing wait (backoff), many clients hit a server that is already overloaded. Both make an outage worse.',
        'task': '''Write `retry_policy(statuses, base_delay, max_delay, max_attempts)`. Return `{'attempts': N, 'delays': [...], 'status': last_status}`. Do not sleep and do not send requests.

`statuses` are the HTTP statuses that the server gives, one for each attempt, in order.

1. Make attempts one at a time. Each attempt reads the next status.
2. Stop when the status is not retryable. Retryable means `429` or `500` and higher.
3. Also stop after `max_attempts` attempts, or when no statuses remain.
4. Before each real retry, add a wait to `delays`: `min(max_delay, base_delay * 2 ** (attempts - 1))`, where `attempts` is the number of attempts so far. So the waits are `base`, `2 × base`, `4 × base`, …, never more than `max_delay`.
5. Add no wait when no other attempt will run.
6. `status` is the last status that you read. With no statuses, return 0 attempts, no delays, and `None`.''',
        'constraints': ['`statuses` has 0–100 integers from 100 to 599.', '`max_attempts` is 1–10. `1 <= base_delay <= max_delay`.'],
        'starter': '''def retry_policy(statuses, base_delay, max_delay, max_attempts):
    """Plan the attempts and the waits between them.

    retry_policy([503, 503, 200], base_delay=2, max_delay=3, max_attempts=3)
    -> {'attempts': 3, 'delays': [2, 3], 'status': 200}
    """
    attempts = 0
    delays = []
    status = None

    while attempts < max_attempts and attempts < len(statuses):
        # Step 1: make one attempt. Read the next status.
        status = statuses[attempts]
        attempts += 1

        # Step 2: stop if this status is not retryable (retryable: 429, or 500 and higher).
        # TODO

        # Step 3: stop if no other attempt will run
        #         (attempts reached max_attempts, or no statuses remain).
        # TODO

        # Step 4: a retry will happen. Add its wait:
        #         min(max_delay, base_delay * 2 ** (attempts - 1))
        # TODO

    return {"attempts": attempts, "delays": delays, "status": status}
''',
        'hints': [
            'Check "not retryable" first: `if not (status == 429 or status >= 500): break`.',
            'Add a wait only before a real retry. If `attempts == max_attempts` or `attempts == len(statuses)`, stop without a wait.',
            'You already increased `attempts`, so the first wait is `base_delay * 2 ** 0`, which is `base_delay`.',
        ],
        'explanation': '''Each loop pass is one attempt. Stop at a final status, or when the limit or the statuses run out. Otherwise add the next wait. It doubles each time and is capped at `max_delay`.''',
        'mistakes': [
            'Not retrying `429`. It means "too many requests, try later".',
            'Adding a wait after the last attempt.',
            'Starting the doubling one step too high, so the first wait is `2 × base`.',
        ],
    },
    10: {
        'ticket': 'Clients send a job request again when they do not get an answer. Each request has an idempotency key. The same key means "this is the same request".',
        'why': 'Without the key, a repeated request runs the job twice. For a payment, that charges the customer twice. With the key, the server returns the first result again.',
        'task': '''Write `enqueue_jobs(requests)`. Process the requests in order. Return one response for each request. Each request has a `key` and a `task`.

1. New key: save the key with its task and give it the next ID (1, 2, 3, …). Return `{'status': 'created', 'id': ID}`.
2. Known key with the same task: return `{'status': 'replayed', 'id': ORIGINAL_ID}`.
3. Known key with a different task: return `{'status': 'conflict', 'id': None}`. Keep the saved task unchanged.
4. Only `created` uses a new ID.
5. Compare keys and tasks exactly. Letter case and spaces count.''',
        'constraints': ['0–300 requests. Keys are nonempty strings. Tasks are strings and can be empty.'],
        'starter': '''def enqueue_jobs(requests):
    """Create each job once. A repeated key replays the first result.

    enqueue_jobs([{'key': 'a', 'task': 'send'}, {'key': 'a', 'task': 'send'}])
    -> [{'status': 'created', 'id': 1}, {'status': 'replayed', 'id': 1}]
    """
    jobs = {}      # key -> (task, id)
    next_id = 1
    responses = []

    for request in requests:
        key, task = request["key"], request["task"]

        if key not in jobs:
            # Step 1: a new key.
            # TODO: save jobs[key] = (task, next_id), answer "created" with
            #       next_id, then increase next_id by 1.
            responses.append({"status": "created", "id": None})
        else:
            saved_task, saved_id = jobs[key]
            # Step 2: same task      -> "replayed" with saved_id.
            # Step 3: different task -> "conflict" with id None. Do not change jobs.
            # TODO
            responses.append({"status": "TODO", "id": None})

    return responses
''',
        'hints': [
            'Save two values for each key: the task (to compare later) and the ID (to return later).',
            'Increase `next_id` only in the `created` branch. Replays and conflicts do not use an ID.',
            'Use `if task == saved_task:` for a replay and `else:` for a conflict. Do not overwrite `jobs[key]` on a conflict.',
        ],
        'explanation': '''A dictionary maps each key to its first task and ID. A new key creates a job. A known key returns the saved ID when the task matches, or a conflict when it does not.''',
        'mistakes': [
            'Giving an ID to replays or conflicts, so the IDs have gaps.',
            'Returning a new ID for a replay instead of the original ID.',
            'Accepting a changed task as a replay.',
        ],
    },
    11: {
        'ticket': 'The cache keeps each value for a fixed time (TTL, "time to live"). After that time, the value is old and must not be used.',
        'why': 'Old cache values show wrong prices or permissions. The tests give the time as a number. So the result does not depend on the real clock, and the tests are repeatable.',
        'task': '''Write `run_cache(operations)`. Start with an empty cache. Process the operations in order. Return one result for each operation.

1. `put` has `key`, `value`, `now`, and `ttl`. Save the value with the deadline `now + ttl`. Replace an old entry. The result is `None`.
2. `get` has `key` and `now`. If the key is saved and `now < deadline`, return `{'hit': True, 'value': VALUE}`. Otherwise return `{'hit': False, 'value': None}`.
3. A saved `None`, `False`, `0`, or `""` is still a hit.
4. At `now == deadline`, the entry is expired. A `ttl` of `0` expires at once.
5. A `get` does not change the deadline.''',
        'constraints': ['Times and TTLs are integers of 0 or more. Times do not go backwards.', 'Keys are strings and can be empty. Values can be any JSON value.'],
        'starter': '''def run_cache(operations):
    """Run put/get operations on a cache with expiry times.

    run_cache([{'op': 'put', 'key': 'a', 'value': 'ready', 'now': 5, 'ttl': 3},
               {'op': 'get', 'key': 'a', 'now': 7}])
    -> [None, {'hit': True, 'value': 'ready'}]      (7 < 5 + 3)
    """
    entries = {}   # key -> (value, deadline)
    results = []

    for operation in operations:
        key, now = operation["key"], operation["now"]

        if operation["op"] == "put":
            # Step 1: save the value with its deadline (now + ttl).
            # TODO
            results.append(None)
        else:
            # Step 2: a get. It is a hit only if the key is in entries AND now < deadline.
            #         Check `key in entries`, not the value: a saved None is still a hit.
            # TODO
            results.append({"hit": False, "value": None})

    return results
''',
        'hints': [
            'Save a pair for each key: `entries[key] = (operation["value"], now + operation["ttl"])`.',
            'Use `if key in entries:`, then `value, deadline = entries[key]`, then compare `now < deadline`.',
            'Use `<`, not `<=`. Do not test the value itself with `if value:`, because `None`, `False`, and `0` are valid cached values.',
        ],
        'explanation': '''Save each value with its deadline. A get is a hit only before the deadline. The check uses the key, not the value, so falsy values are cached correctly.''',
        'mistakes': [
            'Keeping a value at the exact deadline (`<=`).',
            'Treating a cached `None`, `False`, or `0` as a miss.',
            'Using `ttl` as the deadline instead of `now + ttl`.',
        ],
    },
    13: {
        'ticket': 'A consumer reads update events from a queue. Events can arrive late or out of order. Each event has a version number.',
        'why': 'If you keep the last event that arrives, a late old event overwrites new data. The version number tells you which data is newer.',
        'task': '''Write `latest_events(events)`. Each event has `entity`, `version`, and `value`. Return a dictionary from each entity to its latest value.

1. Process the events in order.
2. Save the first event for each entity.
3. Replace the saved value only when the new version is strictly greater. On an equal or smaller version, ignore the event.
4. Return the values, not the versions. A value can be any JSON value, also `None` or `False`.''',
        'constraints': ['0–300 events. Entity names are nonempty strings. Versions are integers from 1 to 1000000000.'],
        'starter': '''def latest_events(events):
    """Keep the value with the highest version for each entity.

    latest_events([{'entity': 'a', 'version': 2, 'value': 'new'},
                   {'entity': 'a', 'version': 1, 'value': 'old'}])
    -> {'a': 'new'}     (the late old event is ignored)
    """
    latest = {}   # entity -> (version, value)

    for event in events:
        entity, version, value = event["entity"], event["version"], event["value"]

        # Step 1: new entity -> save (version, value).
        # Step 2: known entity -> replace only if version > saved version.
        # TODO: put a condition around this line.
        latest[entity] = (version, value)

    # Step 3: return only the values.
    return {entity: saved[1] for entity, saved in latest.items()}
''',
        'hints': [
            'Save the version with the value. You need the version to compare later events.',
            '`if entity not in latest or version > latest[entity][0]:` covers both steps.',
            'Use `>`, not `>=`. On a tie, the first event stays.',
        ],
        'explanation': '''Save the version and the value for each entity. A new event wins only with a higher version. So late and repeated events do not overwrite newer data.''',
        'mistakes': [
            'Letting an equal version overwrite the first event.',
            'Letting a stale event overwrite a newer one.',
            'Returning the version instead of the value.',
        ],
    },
    19: {
        'ticket': 'The resource endpoint decides if a user can `read`, `write`, or `delete` a resource.',
        'why': 'Authorization bugs let users see or change data that is not theirs. Rules are safest when you check them in a fixed order and deny when no rule allows.',
        'task': '''Write `can_access(user, resource, action)`. Return `True` or `False`. Check these rules in order. The first rule that applies decides.

1. If `action` is not exactly `read`, `write`, or `delete`, deny.
2. If the user is suspended, deny. This is also true for admins.
3. If the user is an `admin`, allow.
4. If the action is `read` and the resource is public, allow.
5. If the user is a `member` and their `id` equals the resource `owner_id`, allow.
6. Otherwise, deny.

`user` has `id`, `role` (`admin`, `member`, or `guest`), and `suspended`. `resource` has `owner_id` and `public`. Compare text exactly.''',
        'constraints': ['`suspended` and `public` are booleans. A guest `id` is `None`.', '`action` is any string with at most 100 characters.'],
        'starter': '''KNOWN_ACTIONS = {"read", "write", "delete"}


def can_access(user, resource, action):
    """Apply the access rules in order. The first rule that applies decides.

    user = {'id': 'a', 'role': 'member', 'suspended': False}
    can_access(user, {'owner_id': 'a', 'public': False}, 'write') -> True   (owner)
    can_access(user, {'owner_id': 'b', 'public': False}, 'read')  -> False
    """
    # Each rule returns at once. The order is important.

    # Rule 1: unknown action -> deny.
    # TODO

    # Rule 2: suspended user -> deny. This is also true for admins.
    # TODO

    # Rule 3: admin -> allow.
    # TODO

    # Rule 4: anyone can read a public resource.
    # TODO

    # Rule 5: a member can do any known action on their own resource.
    # TODO

    # Rule 6: no rule allowed it -> deny.
    return False
''',
        'hints': [
            'Write each rule as `if ...: return ...`. The first rule that matches decides.',
            'Put the deny rules (unknown action, suspended) before the allow rules. Then no allow rule can skip them.',
            'Rule 5 is `user["role"] == "member" and user["id"] == resource["owner_id"]`. Rule 4 needs both `action == "read"` and `resource["public"]`.',
        ],
        'explanation': '''The function is a list of rules in a fixed order. Deny rules come first, then allow rules, and the default is deny. This "deny by default" design is the safe way to write permissions.''',
        'mistakes': [
            'Ignoring `suspended` for admins.',
            'Letting a public resource allow `write` or `delete`.',
            'Allowing any member instead of only the owner.',
        ],
    },
    24: {
        'ticket': 'The page renderer puts user values into a trusted HTML template with placeholders like `{{name}}`.',
        'why': 'If a value contains `<script>` and you insert it without escaping, the script runs in another user\'s browser. This attack is called cross-site scripting (XSS). Escape every inserted value.',
        'task': '''Write `render_html(template, values)`. Return the rendered text.

1. A placeholder is `{{name}}`. The name starts with a letter or `_`, then has letters, digits, or `_`. There are no spaces.
2. If the name is in `values`, replace the placeholder with the escaped value. Escape `&`, `<`, `>`, `"`, and `'` as `&amp;`, `&lt;`, `&gt;`, `&quot;`, and `&#x27;`. `html.escape(text)` does exactly this.
3. If the name is not in `values`, keep the placeholder unchanged.
4. Do not change any other template text, also `&` or `<b>`.
5. Replace in one pass. Do not process text that you inserted.''',
        'constraints': ['The template has at most 10000 characters. `values` has at most 100 string values.'],
        'starter': '''import html
import re

PLACEHOLDER = re.compile(r"\\{\\{([A-Za-z_][A-Za-z0-9_]*)\\}\\}")


def render_html(template, values):
    """Replace each {{name}} with the escaped value.

    render_html('<p>{{name}}</p>', {'name': '<b>'})  -> '<p>&lt;b&gt;</p>'
    render_html('Hi {{missing}}', {})                -> 'Hi {{missing}}'
    """
    def substitute(match):
        name = match.group(1)   # the text between {{ and }}
        # Step 1: unknown name -> return the placeholder unchanged: match.group(0)
        # TODO
        # Step 2: known name -> return the ESCAPED value.
        return values[name]  # TODO: escape it

    # Step 3: re.sub calls substitute once for each placeholder, in one pass.
    return PLACEHOLDER.sub(substitute, template)
''',
        'hints': [
            '`html.escape(value)` escapes all five characters. It escapes quotes by default.',
            '`match.group(0)` is the full placeholder text, such as `{{name}}`. `match.group(1)` is only the name.',
            'Do not call `template.replace()` once for each name. A value that contains `{{b}}` would then be processed again. `re.sub` with a function makes one pass.',
        ],
        'explanation': '''A regular expression finds each placeholder. A small function decides the replacement: the escaped value, or the unchanged placeholder when the name is unknown. Only inserted values are escaped. The trusted template stays the same.''',
        'mistakes': [
            'Not escaping quotes. A value can then break out of an HTML attribute.',
            'Removing unknown placeholders.',
            'Replacing names one after another, so inserted text is processed again.',
        ],
    },
    20: {
        'ticket': 'The upload endpoint gets a file path from the user and saves the file below the upload folder.',
        'why': 'If a user sends `../../etc/passwd`, the server can write outside the upload folder. This attack is called path traversal. Clean the path as text, and reject any path that leaves the folder.',
        'task': '''Write `resolve_upload_path(path)`. Return a clean relative path, or `None` when you reject the path.

1. Reject the path if it starts with `/`, or if it contains a backslash (`\\`) or the NUL character (`\\x00`).
2. Split the path on `/`. Process the parts in order:
   - Skip empty parts and `.` parts.
   - For `..`, remove the last kept part. If no part is kept, reject the path at once. Later parts cannot repair it.
   - Keep every other part exactly as it is.
3. Join the kept parts with `/`. If no part is kept, return `None`.

Only exact `.` and `..` are special. `...` and `..hidden` are normal names. Do not use the file system.''',
        'constraints': ['`path` has 0–500 ASCII characters.'],
        'starter': r'''def resolve_upload_path(path):
    """Return a clean relative path, or None when the path is unsafe or empty.

    resolve_upload_path('photos/./2026//image.png') -> 'photos/2026/image.png'
    resolve_upload_path('a/b/../file.txt')          -> 'a/file.txt'
    resolve_upload_path('../safe/file.txt')         -> None   (leaves the folder)
    """
    # Step 1: reject absolute paths, backslashes, and NUL characters.
    # TODO: return None if path starts with "/", or "\\" in path, or "\x00" in path.

    parts = []   # the kept parts, used like a stack
    for component in path.split("/"):
        # Step 2: skip empty and "." parts.
        # TODO
        # Step 3: ".." removes the last kept part. With nothing to remove, return None.
        # TODO
        # Step 4: keep every other part.
        parts.append(component)

    # Step 5: join the parts, or return None when no part is kept.
    return "/".join(parts)  # TODO: None when parts is empty
''',
        'hints': [
            'Use `parts` as a stack: `append` keeps a part, and `pop` removes the last part for `..`.',
            'Check the stack before you `pop()`: `if not parts: return None`. A path that leaves the folder is always rejected.',
            'Compare parts with `==`. Only exactly `"."` and `".."` are special. Use `continue` to skip a part.',
        ],
        'explanation': '''First reject the characters that are never allowed. Then walk through the parts with a stack. `..` removes the last part, and a `..` with nothing to remove means the path leaves the folder.''',
        'mistakes': [
            'Accepting a path that starts with `/`.',
            'Ignoring a `..` that goes above the folder instead of rejecting the path.',
            'Treating every name that starts with `.` as special.',
        ],
    },
    16: {
        'ticket': 'The balance service moves money between accounts. Each transfer changes two balances.',
        'why': 'Money must never be lost or created. Either both changes happen, or neither happens. This is called an atomic change. Check everything first, then change.',
        'task': '''Write `apply_transfers(balances, transfers)`. `balances` maps account names to integer cents. Each transfer has `from`, `to`, and `amount`. Process the transfers in order.

1. Accept a transfer only if both accounts exist and the source has at least `amount` cents.
2. If you accept it, subtract the amount from the source and add it to the target.
3. If you reject it, change nothing and do not create accounts.
4. A transfer to the same account needs enough money. It does not change the balance.

Return `{'accepted': [...], 'balances': {...}}`, with one boolean for each transfer and the final balance of every account. Do not change the input.''',
        'constraints': ['0–300 accounts and 0–300 transfers. Balances and amounts are integers. Amounts are 1 or more.'],
        'starter': '''def apply_transfers(balances, transfers):
    """Apply each transfer completely or not at all.

    apply_transfers({'a': 50, 'b': 10}, [{'from': 'a', 'to': 'b', 'amount': 20}])
    -> {'accepted': [True], 'balances': {'a': 30, 'b': 30}}
    """
    accounts = dict(balances)   # a copy: do not change the input
    accepted = []

    for transfer in transfers:
        source, target, amount = transfer["from"], transfer["to"], transfer["amount"]

        # Step 1: check everything BEFORE you change anything.
        #         ok = both accounts exist and the source has at least `amount`.
        ok = False  # TODO

        # Step 2: only when ok, subtract from the source and add to the target.
        # TODO

        accepted.append(ok)

    return {"accepted": accepted, "balances": accounts}
''',
        'hints': [
            'Check first, then change. If you subtract before you know that the target exists, a failed transfer loses money.',
            '`ok = source in accounts and target in accounts and accounts[source] >= amount`.',
            'Use `>=`, because an exact balance is enough. For a transfer to the same account, subtract then add gives the same balance.',
        ],
        'explanation': '''Check all conditions before you change a balance. Then make both changes together. In a real database you get the same guarantee from a transaction: both updates are saved, or neither is.''',
        'mistakes': [
            'Rejecting a transfer of the exact balance.',
            'Subtracting from the source when the target does not exist.',
            'Adding to the target without subtracting from the source.',
        ],
        'difficulty': 'Medium',
        'simple_solution': '''def apply_transfers(balances, transfers):
    accounts = dict(balances)
    accepted = []
    for transfer in transfers:
        source, target, amount = transfer["from"], transfer["to"], transfer["amount"]
        ok = source in accounts and target in accounts and accounts[source] >= amount
        if ok:
            accounts[source] -= amount
            accounts[target] += amount
        accepted.append(ok)
    return {"accepted": accepted, "balances": accounts}
''',
        'simple_solution_note': 'The judge also accepts this version with a real SQLite transaction. `with db:` commits both updates together, or rolls both back on an error:',
    },
}
