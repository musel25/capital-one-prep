"""Normalize a relative upload path without accessing the filesystem."""

CASES = [
    {"input": {"path": "photos/./2026//image.png"}, "expected": "photos/2026/image.png", "label": "remove dot and empty components"},
    {"input": {"path": "a/b/../file.txt"}, "expected": "a/file.txt", "label": "parent component removes one prior component"},
    {"input": {"path": "../safe/file.txt"}, "expected": None, "label": "reject an initial parent escape"},
    {"input": {"path": ""}, "expected": None, "label": "empty input has no file components"},
    {"input": {"path": "."}, "expected": None, "label": "single dot normalizes to empty"},
    {"input": {"path": "././"}, "expected": None, "label": "only dot and empty components"},
    {"input": {"path": "/etc/passwd"}, "expected": None, "label": "reject an absolute path"},
    {"input": {"path": "///file"}, "expected": None, "label": "reject repeated leading slashes"},
    {"input": {"path": "a\\b"}, "expected": None, "label": "reject a backslash"},
    {"input": {"path": "a\x00b"}, "expected": None, "label": "reject a NUL character"},
    {"input": {"path": "a/.."}, "expected": None, "label": "parent traversal consumes all components"},
    {"input": {"path": "a/../b"}, "expected": "b", "label": "return to root and then add a component"},
    {"input": {"path": "a/../../b"}, "expected": None, "label": "reject escape immediately even with later components"},
    {"input": {"path": "a/b/../../c/d"}, "expected": "c/d", "label": "multiple balanced parent components"},
    {"input": {"path": "report.txt/"}, "expected": "report.txt", "label": "ignore a trailing separator"},
    {"input": {"path": ".../..hidden/file..txt"}, "expected": ".../..hidden/file..txt", "label": "only exact dot names have special meaning"},
    {"input": {"path": "A_b-1/File.TXT"}, "expected": "A_b-1/File.TXT", "label": "preserve normal segment spelling"},
    {"input": {"path": ".."}, "expected": None, "label": "standalone parent escapes root"},
    {"input": {"path": "a//b///.././c//"}, "expected": "a/c", "label": "combined redundant separators and parent traversal"},
    {"input": {"path": "a/../..//later"}, "expected": None, "label": "later segments cannot repair an escape"},
]

SPEC = {
    "number": 20,
    "slug": "relative-upload-path",
    "title": "Resolve a relative upload path",
    "difficulty": "Medium",
    "category": "05-files-time-and-boundaries",
    "ticket": "The upload endpoint must reject paths that escape the upload root before it constructs a relative destination.",
    "task": "Implement resolve_upload_path(path). Return a normalized relative POSIX path or null if it is rejected or has no remaining components. Reject a leading slash, any backslash or any NUL character. Split the string on '/'. Ignore empty components and exact '.' components. For an exact '..' component, remove the prior normal component. If none exists, reject immediately; later components cannot repair that escape. Keep all other components exactly as supplied. Join the remaining components with '/'. Return null when none remain. Empty input is valid and returns null. This is a string operation only. Do not access the filesystem, resolve symlinks, expand variables or interpret URL encoding. Inputs contain only ASCII letters, digits, '.', '_', '-', '/', backslash or NUL.",
    "constraints": ["path is an ASCII string with 0–500 characters from the stated character set.", "Only exact '.' and '..' components have special meaning.", "Use no filesystem, environment, network or current-directory state. Each call is independent."],
    "function": "resolve_upload_path",
    "starter": "def resolve_upload_path(path):\n    raise NotImplementedError\n",
    "cases": CASES,
}

SPEC["reference"] = r'''def resolve_upload_path(path):
    if path.startswith("/") or "\\" in path or "\x00" in path:
        return None
    parts = []
    for component in path.split("/"):
        if component in ("", "."):
            continue
        if component == "..":
            if not parts:
                return None
            parts.pop()
        else:
            parts.append(component)
    return "/".join(parts) if parts else None
'''

SPEC["java"] = r'''public Object solve(Map<String,Object> d) {
    String path = s(d.get("path"));
    if (path.startsWith("/") || path.indexOf('\\') >= 0 || path.indexOf((char) 0) >= 0) return null;
    List<String> parts = new ArrayList<>();
    for (String component : path.split("/", -1)) {
        if (component.isEmpty() || component.equals(".")) continue;
        if (component.equals("..")) {
            if (parts.isEmpty()) return null;
            parts.remove(parts.size() - 1);
        } else parts.add(component);
    }
    return parts.isEmpty() ? null : String.join("/", parts);
}
'''

SPEC["mutations"] = [
    {"name": "accept leading slash", "old": 'path.startswith("/")', "new": 'False'},
    {"name": "accept backslashes", "old": r'or "\\" in path', "new": ''},
    {"name": "accept NUL characters", "old": r'or "\x00" in path', "new": ''},
    {"name": "ignore root escapes", "old": 'if not parts:\n                return None', "new": 'if not parts:\n                continue'},
    {"name": "keep prior component on parent traversal", "old": 'parts.pop()', "new": 'pass'},
    {"name": "interpret all dot-prefixed names as parents", "old": 'if component == "..":', "new": 'if component.startswith(".."):'},
]
