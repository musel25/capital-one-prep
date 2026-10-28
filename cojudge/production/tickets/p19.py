"""Apply a fixed access policy with explicit deny precedence."""

def case(user, resource, action, expected, label):
    return {"input": {"user": user, "resource": resource, "action": action}, "expected": expected, "label": label}


CASES = [
    case({"id": "root", "role": "admin", "suspended": True}, {"owner_id": "x", "public": True}, "read", False, "suspension overrides admin and public access"),
    case({"id": None, "role": "guest", "suspended": False}, {"owner_id": "x", "public": True}, "read", True, "guest can read a public resource"),
    case({"id": "a", "role": "member", "suspended": False}, {"owner_id": "a", "public": False}, "write", True, "member can write an owned private resource"),
    case({"id": "root", "role": "admin", "suspended": False}, {"owner_id": "x", "public": False}, "delete", True, "admin can delete another owner's resource"),
    case({"id": "root", "role": "admin", "suspended": False}, {"owner_id": "x", "public": False}, "read", True, "admin can read a private resource"),
    case({"id": "root", "role": "admin", "suspended": False}, {"owner_id": "x", "public": False}, "write", True, "admin can write another owner's resource"),
    case({"id": "root", "role": "admin", "suspended": False}, {"owner_id": "x", "public": True}, "share", False, "admin cannot use an unknown action"),
    case({"id": None, "role": "guest", "suspended": False}, {"owner_id": "x", "public": False}, "read", False, "guest cannot read a private resource"),
    case({"id": None, "role": "guest", "suspended": False}, {"owner_id": "x", "public": True}, "write", False, "public visibility does not allow guest writes"),
    case({"id": None, "role": "guest", "suspended": False}, {"owner_id": "x", "public": True}, "delete", False, "public visibility does not allow guest deletion"),
    case({"id": None, "role": "guest", "suspended": True}, {"owner_id": "x", "public": True}, "read", False, "suspended guest cannot read public data"),
    case({"id": "a", "role": "member", "suspended": False}, {"owner_id": "a", "public": False}, "read", True, "owner can read a private resource"),
    case({"id": "a", "role": "member", "suspended": False}, {"owner_id": "a", "public": False}, "delete", True, "owner can delete a private resource"),
    case({"id": "a", "role": "member", "suspended": True}, {"owner_id": "a", "public": False}, "delete", False, "suspension overrides ownership"),
    case({"id": "a", "role": "member", "suspended": False}, {"owner_id": "b", "public": True}, "read", True, "non-owner member can read public data"),
    case({"id": "a", "role": "member", "suspended": False}, {"owner_id": "b", "public": False}, "read", False, "non-owner member cannot read private data"),
    case({"id": "a", "role": "member", "suspended": False}, {"owner_id": "b", "public": True}, "write", False, "non-owner member cannot write public data"),
    case({"id": "a", "role": "member", "suspended": False}, {"owner_id": "b", "public": True}, "delete", False, "non-owner member cannot delete public data"),
    case({"id": "a", "role": "member", "suspended": False}, {"owner_id": "a", "public": True}, "READ", False, "action matching is case-sensitive"),
    case({"id": "a", "role": "member", "suspended": False}, {"owner_id": "a", "public": True}, "", False, "empty action is unknown"),
    case({"id": "A", "role": "member", "suspended": False}, {"owner_id": "a", "public": False}, "read", False, "owner IDs are case-sensitive"),
]

SPEC = {
    "number": 19,
    "slug": "resource-access-policy",
    "title": "Apply a resource access policy",
    "difficulty": "Easy",
    "category": "05-files-time-and-boundaries",
    "ticket": "The resource endpoint must apply suspension and action checks before it grants access by role or ownership.",
    "task": "Implement can_access(user, resource, action) using this fixed policy. Return a bool. user has id, role and suspended fields; resource has owner_id and public fields. The only known actions are the exact strings read, write and delete. Deny every unknown action. Deny suspended users for every action, including admins. Otherwise admins may perform every known action. Any unsuspended user may read a public resource. A member whose id equals owner_id may read, write or delete that resource, including a private one. Deny every remaining request. Guest IDs are null; member and admin IDs are nonempty strings. Owner IDs are nonempty strings. Compare IDs and action names exactly, without case conversion or whitespace changes. Do not change either input object. All required fields and valid field types are supplied.",
    "constraints": ["role is exactly admin, member or guest; suspended and public are bool values.", "IDs contain 1–100 ASCII characters, except guest IDs, which are null.", "action is an ASCII string of 0–100 characters; unknown strings are valid inputs and are denied.", "Apply only the stated policy. No authentication, storage or network access is required."],
    "function": "can_access",
    "starter": "def can_access(user, resource, action):\n    raise NotImplementedError\n",
    "cases": CASES,
}

SPEC["reference"] = '''def can_access(user, resource, action):
    if action not in ("read", "write", "delete"):
        return False
    if user["suspended"]:
        return False
    if user["role"] == "admin":
        return True
    if action == "read" and resource["public"]:
        return True
    return user["role"] == "member" and user["id"] == resource["owner_id"]
'''

SPEC["java"] = '''public Object solve(Map<String,Object> d) {
    Map<String,Object> user = obj(d.get("user")), resource = obj(d.get("resource"));
    String action = s(d.get("action"));
    if (!Set.of("read", "write", "delete").contains(action) || Boolean.TRUE.equals(user.get("suspended"))) return false;
    if (s(user.get("role")).equals("admin")) return true;
    if (action.equals("read") && Boolean.TRUE.equals(resource.get("public"))) return true;
    return s(user.get("role")).equals("member") && Objects.equals(user.get("id"), resource.get("owner_id"));
}
'''

SPEC["mutations"] = [
    {"name": "ignore suspension", "old": 'if user["suspended"]:', "new": 'if False:'},
    {"name": "allow unknown actions for authorized users", "old": 'if action not in ("read", "write", "delete"):', "new": 'if False:'},
    {"name": "public resources allow every action", "old": 'action == "read" and resource["public"]', "new": 'resource["public"]'},
    {"name": "members need not own the resource", "old": 'user["role"] == "member" and user["id"] == resource["owner_id"]', "new": 'user["role"] == "member"'},
    {"name": "admins cannot access other owners' resources", "old": 'if user["role"] == "admin":', "new": 'if user["role"] == "admin" and user["id"] == resource["owner_id"]:'},
]
