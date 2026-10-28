"""Choose a deterministic dependency build order."""

CASES = [
    {"label": "independent jobs and dependent job", "input": {"dependencies": {"app": ["lib"], "lib": [], "docs": []}}, "expected": ["docs", "lib", "app"]},
    {"label": "newly ready job can precede an earlier ready job", "input": {"dependencies": {"a": [], "b": ["a"], "z": []}}, "expected": ["a", "b", "z"]},
    {"label": "cycle returns no partial build list", "input": {"dependencies": {"a": [], "b": ["c"], "c": ["b"]}}, "expected": None},
    {"label": "empty dependency map", "input": {"dependencies": {}}, "expected": []},
    {"label": "one independent job", "input": {"dependencies": {"build": []}}, "expected": ["build"]},
    {"label": "independent jobs use ASCII order", "input": {"dependencies": {"a": [], "Z": [], "A": [], "0": [], "-": []}}, "expected": ["-", "0", "A", "Z", "a"]},
    {"label": "chain ignores mapping insertion order", "input": {"dependencies": {"c": ["b"], "b": ["a"], "a": []}}, "expected": ["a", "b", "c"]},
    {"label": "diamond requires both prerequisites", "input": {"dependencies": {"d": ["b", "c"], "c": ["a"], "b": ["a"], "a": []}}, "expected": ["a", "b", "c", "d"]},
    {"label": "duplicate prerequisites count once", "input": {"dependencies": {"b": ["a", "a", "a"], "a": []}}, "expected": ["a", "b"]},
    {"label": "self dependency is a cycle", "input": {"dependencies": {"a": ["a"]}}, "expected": None},
    {"label": "duplicate self dependencies remain a cycle", "input": {"dependencies": {"a": ["a", "a"]}}, "expected": None},
    {"label": "three-job cycle", "input": {"dependencies": {"a": ["b"], "b": ["c"], "c": ["a"]}}, "expected": None},
    {"label": "multiple roots become ready in lexical order", "input": {"dependencies": {"z": [], "a": ["z"], "b": []}}, "expected": ["b", "z", "a"]},
    {"label": "job names are not stripped", "input": {"dependencies": {"A": [" A "], " A ": [], "a": []}}, "expected": [" A ", "A", "a"]},
    {"label": "duplicate edges across a diamond", "input": {"dependencies": {"a": [], "b": ["a", "a"], "c": ["a"], "d": ["b", "c", "c"]}}, "expected": ["a", "b", "c", "d"]},
    {"label": "job becomes ready only after last prerequisite", "input": {"dependencies": {"a": ["b", "z"], "b": [], "c": ["b"], "z": []}}, "expected": ["b", "c", "z", "a"]},
]

SPEC = {
    "number": 22,
    "slug": "order-build-jobs",
    "title": "Produce a deterministic build order",
    "difficulty": "Medium",
    "category": "06-application-logic",
    "ticket": "The build runner needs a stable execution order that respects every job prerequisite.",
    "task": "Implement `build_order(dependencies)`. The input maps each job name to a list of prerequisite job names. Every prerequisite exists in the map. Treat duplicate prerequisites as one dependency. A job is ready when all its prerequisites have already been added to the result. Repeatedly select the ASCII lexicographically smallest currently ready job. Return the complete list of job names. If a cycle prevents completion, return null instead of a partial list. An empty map returns an empty list. Compare names exactly. Do not change the input.",
    "constraints": ["There are 0 through 100 jobs.", "Job names are nonempty ASCII strings of at most 30 characters.", "Prerequisite lists can be empty and can contain duplicate names.", "All prerequisite names are keys in dependencies; self dependencies are allowed."],
    "function": "build_order",
    "starter": "def build_order(dependencies):\n    raise NotImplementedError\n",
    "reference": '''def build_order(dependencies):
    remaining = {job: set(prerequisites) for job, prerequisites in dependencies.items()}
    ordered = []
    while remaining:
        ready = sorted(job for job, needed in remaining.items() if not needed)
        if not ready:
            return None
        job = ready[0]
        ordered.append(job)
        del remaining[job]
        for needed in remaining.values():
            needed.discard(job)
    return ordered
''',
    "java": '''public Object solve(Map<String,Object> d) {
    Map<String,Object> dependencies = obj(d.get("dependencies"));
    Map<String,Integer> indegree = new HashMap<>();
    Map<String,List<String>> dependents = new HashMap<>();
    for (String job : dependencies.keySet()) {
        Set<String> unique = new HashSet<>();
        for (Object prerequisite : arr(dependencies.get(job))) unique.add(s(prerequisite));
        indegree.put(job, unique.size());
        for (String prerequisite : unique) {
            dependents.computeIfAbsent(prerequisite, k -> new ArrayList<>()).add(job);
        }
    }
    PriorityQueue<String> ready = new PriorityQueue<>();
    for (String job : indegree.keySet()) if (indegree.get(job) == 0) ready.add(job);
    List<Object> ordered = new ArrayList<>();
    while (!ready.isEmpty()) {
        String job = ready.remove();
        ordered.add(job);
        for (String dependent : dependents.getOrDefault(job, Collections.emptyList())) {
            int count = indegree.get(dependent) - 1;
            indegree.put(dependent, count);
            if (count == 0) ready.add(dependent);
        }
    }
    return ordered.size() == dependencies.size() ? ordered : null;
}''',
    "cases": CASES,
    "mutations": [
        {"name": "choose largest ready job", "old": "job = ready[0]", "new": "job = ready[-1]"},
        {"name": "ignore unmet prerequisites", "old": "if not needed)", "new": "if True)"},
        {"name": "return partial output on a cycle", "old": "if not ready:\n            return None", "new": "if not ready:\n            return ordered"},
        {"name": "sort job names without case", "old": "ready = sorted(job for job, needed in remaining.items() if not needed)", "new": "ready = sorted((job for job, needed in remaining.items() if not needed), key=str.lower)"},
    ],
}
