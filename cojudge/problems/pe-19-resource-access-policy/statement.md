The resource endpoint must apply suspension and action checks before it grants access by role or ownership.

Implement `can_access(user, resource, action)`. Return a boolean using these checks in order:

1. Deny unknown actions. Only the exact strings `read`, `write`, and `delete` are known.
2. Deny suspended users, including admins.
3. Allow admins to perform every known action.
4. Allow any unsuspended user to read a public resource.
5. Allow a member whose `id` equals `owner_id` to read, write, or delete that resource, including a private one.
6. Deny every remaining request.

Compare IDs and actions exactly. Do not change letter case or whitespace.

**Constraints:**

- role is exactly admin, member or guest; suspended and public are bool values.
- IDs contain 1–100 ASCII characters, except guest IDs, which are null.
- action is an ASCII string of 0–100 characters; unknown strings are valid inputs and are denied.
- `user` has `id`, `role`, and `suspended`; `resource` has `owner_id` and `public`.
- Do not change input objects or their nested values. Each call starts with fresh state.
