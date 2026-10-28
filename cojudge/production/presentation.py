"""Readable ticket text and calls, separate from execution and grading."""
from pprint import pformat
from textwrap import indent


TASKS = {
    1: '''Implement `clean_emails(emails)`. Return cleaned addresses in first-seen order.

Remove surrounding spaces, tabs, carriage returns, and newlines. Convert letters to lowercase. Skip empty results and duplicates. Keep internal characters unchanged. Do not validate email syntax.''',
    2: '''Implement `parse_flag(value, default)`. Return `default` when `value` is `None`.

Otherwise, remove surrounding spaces, tabs, carriage returns, and newlines. Compare without letter case:

- `true`, `1`, `yes`, and `on` return `True`.
- `false`, `0`, `no`, and `off` return `False`.
- Every other string, including an empty string, returns `None`.''',
    3: '''Implement `validate_user(payload)`. Return invalid field names in the order `name`, `email`, `age`.

- `name` is required. It must be a string that remains nonempty after removal of surrounding spaces, tabs, carriage returns, and newlines.
- `email` is required. It must be a string with exactly one `@`, nonempty parts on both sides, and no spaces, tabs, carriage returns, or newlines. Apply no other email rules.
- `age` is optional. If present, it must be a nonnegative integer. Booleans and floats are invalid.

Ignore other fields. Keep field types unchanged. Return an empty list for a valid request.''',
    4: '''Implement `summarize_logs(logs)`. Return a dictionary keyed by service name. Each value contains:

- `requests`: the number of rows for that service.
- `errors`: the number of those rows with status 500 or more.

Count duplicate rows. Compare service names exactly. Empty logs return an empty dictionary.''',
    5: '''Implement `paginate_records(records, after_id, limit)`. Return `{'items': [...], 'next_cursor': ...}`.

Sort records by numeric `id` in ascending order. If `after_id` is not `None`, keep only IDs strictly greater than it. The cursor need not match a record. Return at most `limit` eligible records and retain every field.

Set `next_cursor` to the last returned ID only if more eligible records remain. Otherwise use `None`, including for empty results and exactly full final pages.''',
    6: '''Implement `apply_settings_patch(settings, patch)`. Return a new settings object, even when the patch is empty.

Start with the existing entries. For each patch key:

- A `None` value removes the key. Removing an absent key does nothing.
- Any other value replaces the existing value or adds a new entry. Keep `False`, zero, and empty values.

Apply the patch only at the top level. Nested objects and lists replace entire values; keep `None` inside them. Keep unpatched entries, including existing `None` values. Compare keys exactly; empty keys are valid.''',
    7: '''Implement `redact_secrets(value)` for any JSON value.

For each object key, compare ASCII letters without regard to case. If the whole key is `password`, `token`, or `secret`, replace its entire value with `'[REDACTED]'`. Keep the original key spelling and do not inspect the replaced subtree. Do not trim keys or match substrings.

Recursively process other object values and list elements. Keep scalars unchanged, including strings that contain secret words. Keep empty objects and lists empty. Redacting an already redacted result must leave its JSON value unchanged.''',
    8: '''Implement `retry_policy(statuses, base_delay, max_delay, max_attempts)`. Return `{'attempts': N, 'delays': [...], 'status': last_status}`.

Read one status per attempt, in input order. Retry only status 429 or statuses at least 500. Stop on any other status, at `max_attempts`, or when statuses run out. Ignore unconsumed statuses.

Before an actual retry after attempt `i`, append `min(max_delay, base_delay * 2**(i-1))` to `delays`. Attempt numbers start at 1. Add no delay after the final attempt.

Empty input returns zero attempts, no delays, and `None` status. Produce a plan; do not sleep or make requests.''',
    9: '''Implement `collect_pages(pages, start)`. Follow `next` tokens from `start` until `None`. Return `{'items': [...], 'error': None}` on success.

Keep each ID once, in first-seen order. Compare tokens exactly. Stop before reading a missing or previously visited token:

- A missing token returns error `'missing_page'`.
- A repeated token returns error `'cycle'`.

Keep all IDs collected before an error. A `None` start returns empty items and no error. Ignore pages outside the followed chain.''',
    10: '''Implement `enqueue_jobs(requests)`. Process requests in order and return one response per request.

- New key: store its task and allocate the next ID, starting at 1. Return `{'status': 'created', 'id': ID}`.
- Existing key, same task: return `{'status': 'replayed', 'id': ORIGINAL_ID}`.
- Existing key, different task: return `{'status': 'conflict', 'id': None}`.

Replays and conflicts consume no ID. Conflicts change no stored data. Compare strings exactly. Each call starts with an empty queue and ID 1. Empty input returns an empty list.''',
    11: '''Implement `run_cache(operations)`. Process operations in order, starting with an empty cache. Return one result per operation.

- `put` has `key`, `value`, `now`, and `ttl`. Store the value with expiry `now + ttl`, replacing the prior value and deadline. Return `None`.
- `get` has `key` and `now`. Before expiry (`now < expiry`), return `{'hit': True, 'value': STORED_VALUE}`. Otherwise return `{'hit': False, 'value': None}`.

A stored `None` is a hit before expiry. Zero TTL expires immediately. Gets do not change expiry. Compare keys exactly. Use the supplied times; do not use the wall clock or impose a capacity.''',
    12: '''Implement `limit_requests(requests, limit, window)`. Return one boolean per request, in input order.

Each request belongs to bucket `at // window`. Allow at most `limit` requests per user in each bucket. Deny the first request beyond the quota. Denied requests use no quota slot.

Buckets start at multiples of `window`, not at a user's first request. Each new bucket has a full quota. Users have independent quotas; compare names exactly. Empty input returns an empty list.''',
    13: '''Implement `latest_events(events)`. Each event has `entity`, `version`, and `value`. Return a dictionary that maps each entity to its latest value.

Process events in order. Store the first event for each entity. Replace its value only for a strictly greater version. The first event wins a version tie.

Keep any JSON value, including `None`, `False`, and empty collections. Empty input returns an empty dictionary.''',
    14: '''Implement `reserve_stock(stock, requests)`. `stock` maps SKUs to available quantities. Each request has `sku` and `quantity`. Process reservations in request order.

Accept only when the SKU exists and the requested quantity is no greater than its remaining stock. Subtract stock only on success. Reject unknown SKUs without adding them.

Return `{'accepted': [...], 'stock': {...}}` with one boolean per request. Include every original SKU in the final stock, including zero balances. Empty inputs are valid.''',
    15: '''Implement `process_queue(operations, visibility)`. Return one result per operation, in input order.

- `enqueue` has `id` and `at`. Append the job and return `None`.
- `poll` has `at`. Return the earliest unacknowledged job in enqueue order that was never polled or whose deadline is at or before `at`. Set its deadline to `at + visibility`. Return `None` if no job is available.
- `ack` has `id` and `at`. Remove the job and return `True` only when it is in flight and `at` is strictly before its deadline. Otherwise return `False` without a state change.

At exact expiry, acknowledgment fails and polling can redeliver the job. Empty input returns an empty list.''',
    16: '''Implement `apply_transfers(balances, transfers)`. `balances` maps account names to integer cents. Each transfer has `from`, `to`, and `amount`. Process transfers in input order.

Accept only when both accounts exist and the source has at least `amount` cents. Debit the source and credit the target together. A self-transfer requires sufficient funds and leaves the balance unchanged. Reject other transfers without changing balances or creating accounts.

Return `{'accepted': [...], 'balances': {...}}` with one boolean per transfer and every final account balance. Empty inputs are valid.''',
    17: '''Implement `parse_inventory(csv_text)` with `csv.reader`. Return `{'sku': STRING, 'quantity': INTEGER}` records in CSV order. Keep duplicate SKUs separate.

The first CSV record contains exactly `sku` and `quantity`, in that order. Preserve each SKU exactly, including spaces, quoted commas, escaped double quotes, and quoted newlines. Convert each quantity to an integer.

Skip fully blank records, which `csv.reader` returns as empty lists. A blank physical line inside a quoted field belongs to that field. A header-only file returns an empty list. A final record ending is optional.''',
    18: '''Implement `count_utc_days(timestamps)`. Convert each timestamp to UTC before taking its calendar date. Return a dictionary from `YYYY-MM-DD` dates to counts.

Count duplicate timestamps separately. Input order and dictionary key order do not matter. Empty input returns an empty dictionary. UTC conversion may produce dates in 1999 or 2100.''',
    19: '''Implement `can_access(user, resource, action)`. Return a boolean using these checks in order:

1. Deny unknown actions. Only the exact strings `read`, `write`, and `delete` are known.
2. Deny suspended users, including admins.
3. Allow admins to perform every known action.
4. Allow any unsuspended user to read a public resource.
5. Allow a member whose `id` equals `owner_id` to read, write, or delete that resource, including a private one.
6. Deny every remaining request.

Compare IDs and actions exactly. Do not change letter case or whitespace.''',
    20: '''Implement `resolve_upload_path(path)`. Return a normalized relative POSIX path, or `None` when rejected or no components remain.

Reject a leading slash, any backslash, or any NUL character. Split on `/` and process components in order:

- Ignore empty components and exact `.` components.
- For exact `..`, remove the previous normal component. Reject immediately if none exists; later components cannot repair the escape.
- Keep every other component exactly as supplied.

Join remaining components with `/`. Empty input returns `None`. Operate on the string only. Do not access the filesystem, resolve symlinks, expand variables, or interpret URL encoding.''',
    21: '''Implement `compare_versions(left, right)` for valid SemVer 2.0.0 strings. Return `-1`, `1`, or `0` when the left version has lower, higher, or equal precedence.

Compare major, minor, and patch numerically. A release follows every prerelease with the same core. Compare prerelease identifiers from left to right:

- Numeric identifiers compare numerically and precede nonnumeric identifiers.
- Other identifiers use ASCII lexical order.
- If shared identifiers are equal, the shorter prerelease comes first.

Ignore build metadata after `+`.''',
    22: '''Implement `build_order(dependencies)`. Return a complete list of job names in execution order.

A job is ready after all its prerequisites enter the result. Repeatedly choose the ASCII lexicographically smallest currently ready job. Treat duplicate prerequisites as one dependency. Compare names exactly.

If a cycle prevents completion, return `None` instead of a partial list. An empty map returns an empty list.''',
    23: '''Implement `reconcile_records(local, remote)`. Each list contains records with `id`, `version`, and `checksum`. Return `{'upload': [...], 'download': [...], 'conflicts': [...]}`.

- An ID found only locally needs an upload. An ID found only remotely needs a download.
- For an ID on both sides, upload if its local version is higher; download if its remote version is higher.
- Equal versions with equal checksums need no action. Equal versions with different checksums produce a conflict.

Compare versions before checksums. Compare IDs and checksums exactly. Sort each output list by ASCII lexical order. Do not infer deletions.''',
    24: '''Implement `render_html(template, values)`. Keep the trusted HTML template unchanged except for matching placeholders.

A placeholder is `{{name}}`, where `name` matches `[A-Za-z_][A-Za-z0-9_]*` with no spaces. If the name exists in `values`, insert its escaped string value. Escape `&`, `<`, `>`, double quotes, and single quotes as `&amp;`, `&lt;`, `&gt;`, `&quot;`, and `&#x27;`, respectively.

Leave missing placeholders and other template text unchanged. Process the original template once; do not process inserted placeholders again. Compare names exactly. Empty strings are valid. Return the rendered string.''',
}

# These guarantees were formerly embedded in long task paragraphs.
EXTRA_CONSTRAINTS = {
    5: ['Records are unsorted JSON objects. Fields other than `id` can contain any JSON value.'],
    6: ['Both arguments are JSON objects with string keys and arbitrary JSON values.'],
    9: ['`pages` maps tokens to objects with an `items` list and a `next` token or `None`; `start` is a token or `None`.'],
    10: ['Tasks are ASCII strings and can be empty.'],
    11: ['Keys are ASCII strings, including empty strings. Times arrive in nondecreasing order.'],
    12: ['Each request has a nonempty ASCII `user` string and a nonnegative integer `at`. Requests arrive in nondecreasing timestamp order.'],
    17: ['CSV syntax is valid, with LF or CRLF record endings. Every nonblank data record has two fields. Quantities use canonical nonnegative decimal notation: `0`, or digits without a leading zero.'],
    18: ['Timestamps use exactly `YYYY-MM-DDTHH:MM:SSZ`, `YYYY-MM-DDTHH:MM:SS+HH:MM`, or `YYYY-MM-DDTHH:MM:SS-HH:MM`. Fractional seconds are excluded.'],
    19: ['`user` has `id`, `role`, and `suspended`; `resource` has `owner_id` and `public`.'],
    20: ['Characters are ASCII letters, digits, `.`, `_`, `-`, `/`, backslash, or NUL.'],
}


def _constraints(spec):
    constraints = []
    for item in spec['constraints']:
        if item.startswith(('Inputs satisfy the contract', 'The header and all records satisfy',
                            'No local timezone', 'Use no filesystem', 'Apply only the stated policy')):
            continue
        item = item.replace(' Inputs satisfy the contract; no validation is required.', '')
        constraints.append(item)
    constraints.extend(EXTRA_CONSTRAINTS.get(spec['number'], ()))
    constraints.append('Do not change input objects or their nested values. Each call starts with fresh state.')
    return constraints


def _example_call(function, data):
    arguments = []
    for name, value in data.items():
        argument = f'{name}={pformat(value, width=68, sort_dicts=False)}'
        arguments.append(indent(argument, '    '))
    return function + '(\n' + ',\n'.join(arguments) + '\n)'


def present(spec):
    task = TASKS[spec['number']]
    statement = spec['ticket'].strip() + '\n\n' + task + '\n\n**Constraints:**\n\n'
    statement += '\n'.join('- ' + item for item in _constraints(spec)) + '\n'
    return {
        'statement': statement,
        'examples': [{'input': _example_call(spec['function'], case['input']),
                      'output': repr(case['expected']), 'explanation': case['label']}
                     for case in spec['cases'][:3]],
        'testCaseDescriptions': {},
        'courseHelp': {
            'title': 'Course help',
            'body': ('Implement the named function above the supplied adapter. Run checks the example inputs. '
                     'Submit checks all supplied cases. You can edit each sample input as a JSON object. '
                     'The adapter passes its fields as named arguments and rejects input changes. '
                     'Keep the adapter unchanged.\n\nPython 3.11. Use the standard library.'),
        },
    }
