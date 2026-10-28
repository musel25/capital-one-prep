"""Summarize service failures without treating client errors as server errors."""
CASES = [
    {'input': {'logs': [{'service': 'api', 'status': 200}, {'service': 'api', 'status': 503}]}, 'expected': {'api': {'requests': 2, 'errors': 1}}, 'label': 'mixed outcomes'},
    {'input': {'logs': []}, 'expected': {}, 'label': 'empty logs'},
    {'input': {'logs': [{'service': 'api', 'status': 499}]}, 'expected': {'api': {'requests': 1, 'errors': 0}}, 'label': 'last client status'},
    {'input': {'logs': [{'service': 'api', 'status': 500}]}, 'expected': {'api': {'requests': 1, 'errors': 1}}, 'label': 'first server status'},
    {'input': {'logs': [{'service': 'api', 'status': 599}]}, 'expected': {'api': {'requests': 1, 'errors': 1}}, 'label': 'last server status'},
    {'input': {'logs': [{'service': 'api', 'status': 100}]}, 'expected': {'api': {'requests': 1, 'errors': 0}}, 'label': 'first status'},
    {'input': {'logs': [{'service': 'a', 'status': 500}, {'service': 'b', 'status': 200}]}, 'expected': {'a': {'requests': 1, 'errors': 1}, 'b': {'requests': 1, 'errors': 0}}, 'label': 'separate services'},
    {'input': {'logs': [{'service': 'A', 'status': 200}, {'service': 'a', 'status': 500}]}, 'expected': {'A': {'requests': 1, 'errors': 0}, 'a': {'requests': 1, 'errors': 1}}, 'label': 'case sensitive service'},
    {'input': {'logs': [{'service': 'a', 'status': 500}, {'service': 'a', 'status': 500}]}, 'expected': {'a': {'requests': 2, 'errors': 2}}, 'label': 'duplicate rows count'},
    {'input': {'logs': [{'service': 'api', 'status': 301}, {'service': 'api', 'status': 404}]}, 'expected': {'api': {'requests': 2, 'errors': 0}}, 'label': 'redirect and client error'},
    {'input': {'logs': [{'service': 'x-y', 'status': 503}, {'service': 'x-y', 'status': 201}, {'service': 'x-y', 'status': 501}]}, 'expected': {'x-y': {'requests': 3, 'errors': 2}}, 'label': 'repeated service totals'},
    {'input': {'logs': [{'service': 'a', 'status': 200}, {'service': 'b', 'status': 500}, {'service': 'a', 'status': 500}]}, 'expected': {'a': {'requests': 2, 'errors': 1}, 'b': {'requests': 1, 'errors': 1}}, 'label': 'interleaved services'},
]

SPEC = {
    'number': 4, 'slug': 'summarize-service-errors', 'title': 'Summarize service errors',
    'difficulty': 'Easy', 'category': '01-data-and-api', 'function': 'summarize_logs',
    'ticket': 'The operations dashboard needs request and server-error counts for each service.',
    'task': 'Given a list `logs`, return a dictionary keyed by service name. Each input row has `service` and `status`. Each output value has `requests`, the number of rows for that service, and `errors`, the number with status 500 or more. Count duplicate rows. Service names are case-sensitive. Return an empty dictionary for empty logs.',
    'constraints': ['`0 <= len(logs) <= 10000`.', '`service` is a nonempty ASCII string with at most 100 characters.', '`status` is an integer from 100 through 599. Every row has both fields.'],
    'starter': 'def summarize_logs(logs):\n    raise NotImplementedError\n',
    'reference': '''def summarize_logs(logs):
    out = {}
    for row in logs:
        counts = out.setdefault(row["service"], {"requests": 0, "errors": 0})
        counts["requests"] += 1
        if row["status"] >= 500:
            counts["errors"] += 1
    return out
''',
    'java': '''public Object solve(Map<String,Object> d) {
        Map<String,Object> out=new LinkedHashMap<>();
        for(Object v:arr(d.get("logs"))) {
            Map<String,Object> r=obj(v); String service=s(r.get("service"));
            Map<String,Object> c=obj(out.computeIfAbsent(service,k->map("requests",0,"errors",0)));
            c.put("requests",n(c.get("requests"))+1);
            if(n(r.get("status"))>=500) c.put("errors",n(c.get("errors"))+1);
        } return out;
    }''',
    'cases': CASES,
    'mutations': [
        {'name': 'misses status 500', 'old': '>= 500', 'new': '> 500'},
        {'name': 'counts client errors', 'old': '>= 500', 'new': '>= 400'},
        {'name': 'resets request count', 'old': 'counts["requests"] += 1', 'new': 'counts["requests"] = 1'},
        {'name': 'folds service case', 'old': 'row["service"]', 'new': 'row["service"].lower()'},
    ],
}
