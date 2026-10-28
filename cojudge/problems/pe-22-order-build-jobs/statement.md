The build runner needs a stable execution order that respects every job prerequisite.

Implement `build_order(dependencies)`. Return a complete list of job names in execution order.

A job is ready after all its prerequisites enter the result. Repeatedly choose the ASCII lexicographically smallest currently ready job. Treat duplicate prerequisites as one dependency. Compare names exactly.

If a cycle prevents completion, return `None` instead of a partial list. An empty map returns an empty list.

**Constraints:**

- There are 0 through 100 jobs.
- Job names are nonempty ASCII strings of at most 30 characters.
- Prerequisite lists can be empty and can contain duplicate names.
- All prerequisite names are keys in dependencies; self dependencies are allowed.
- Do not change input objects or their nested values. Each call starts with fresh state.
