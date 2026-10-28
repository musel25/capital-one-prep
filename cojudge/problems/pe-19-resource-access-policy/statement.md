# 19. Apply a resource access policy

The resource endpoint must apply suspension and action checks before it grants access by role or ownership.

Implement can_access(user, resource, action) using this fixed policy. Return a bool. user has id, role and suspended fields; resource has owner_id and public fields. The only known actions are the exact strings read, write and delete. Deny every unknown action. Deny suspended users for every action, including admins. Otherwise admins may perform every known action. Any unsuspended user may read a public resource. A member whose id equals owner_id may read, write or delete that resource, including a private one. Deny every remaining request. Guest IDs are null; member and admin IDs are nonempty strings. Owner IDs are nonempty strings. Compare IDs and action names exactly, without case conversion or whitespace changes. Do not change either input object. All required fields and valid field types are supplied.

**Constraints:**

- role is exactly admin, member or guest; suspended and public are bool values.
- IDs contain 1–100 ASCII characters, except guest IDs, which are null.
- action is an ASCII string of 0–100 characters; unknown strings are valid inputs and are denied.
- Apply only the stated policy. No authentication, storage or network access is required.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `can_access`. **Run** checks the examples. **Submit** checks all 21 cases.
