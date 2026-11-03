**The ticket.** The resource endpoint decides if a user can `read`, `write`, or `delete` a resource.

**Why it matters.** Authorization bugs let users see or change data that is not theirs. Rules are safest when you check them in a fixed order and deny when no rule allows.

### Your task

Write `can_access(user, resource, action)`. Return `True` or `False`. Check these rules in order. The first rule that applies decides.

1. If `action` is not exactly `read`, `write`, or `delete`, deny.
2. If the user is suspended, deny. This is also true for admins.
3. If the user is an `admin`, allow.
4. If the action is `read` and the resource is public, allow.
5. If the user is a `member` and their `id` equals the resource `owner_id`, allow.
6. Otherwise, deny.

`user` has `id`, `role` (`admin`, `member`, or `guest`), and `suspended`. `resource` has `owner_id` and `public`. Compare text exactly.

**Constraints:**

- `suspended` and `public` are booleans. A guest `id` is `None`.
- `action` is any string with at most 100 characters.
