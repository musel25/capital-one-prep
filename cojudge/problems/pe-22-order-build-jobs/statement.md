The build runner needs a stable execution order that respects every job prerequisite.

Implement `build_order(dependencies)`. The input maps each job name to a list of prerequisite job names. Every prerequisite exists in the map. Treat duplicate prerequisites as one dependency. A job is ready when all its prerequisites have already been added to the result. Repeatedly select the ASCII lexicographically smallest currently ready job. Return the complete list of job names. If a cycle prevents completion, return null instead of a partial list. An empty map returns an empty list. Compare names exactly. Do not change the input.

**Constraints:**

- There are 0 through 100 jobs.
- Job names are nonempty ASCII strings of at most 30 characters.
- Prerequisite lists can be empty and can contain duplicate names.
- All prerequisite names are keys in dependencies; self dependencies are allowed.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `build_order`. **Run** checks the examples. **Submit** checks all 16 cases.
