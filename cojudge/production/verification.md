# Publication checks — October 28, 2026

The live course is [Software Engineering Tickets](https://cojudge.musel.dev/?course=software-engineering).

- 24 tickets have 380 manually expected cases. Python and independent Java implementations agree with those expectations.
- All 380 cases also pass through the supplied adapter in Python 3.11.
- The live Submit API accepts every reference and rejects all 103 prepared faulty implementations.
- The live Run API accepts the three examples of ticket 01. The CoJudge CLI initializes its Python template, accepts its reference on Run, and reports a failed case for an incorrect implementation.
- All 22 updated Pybites references pass their 390 live cases. Each unfinished template is rejected. Local checks also reject 83 prepared Pybites faults.
- An isolated copy of this task's committed files passes 86 repository tests. The shared checkout contains concurrent work; its unrelated, initially failing Pytest Path tests are recorded in the implementation plan.
- Independent review checked the contracts and marker behavior. The added eight topics passed 279 further probes against both implementations. No blocking findings remained.
- Browser checks confirmed that a ticket renders its contract, examples, Python template, and one title. Progress writes were blocked in the isolated browser checks.
- The live catalog contains 24 new tickets and 22 Pybites bites. The three retired course indexes are absent. Other course indexes remain in place.

The User bite guarantees nonempty ASCII names. The statement now gives that rule before the original description. The Ninja Rankings reference now prevents self-pairs and reused people. Older saved Pybites tabs remain intact; use a new template tab to get the current test block.

Publication changes only problem definitions and course indexes. It does not write learner solutions or completion flags. The application image remains `cojudge:profiles-1bcab72d0f669737fd1b766a6e7b6ad93f4e3071`.

## Recovery

VPS backup: `/home/ubuntu/cojudge-backups/software-tickets.PJshjq/`.

`content-before.tar.gz` holds the original Pybites files and affected indexes.
`retired-courses/` holds the three removed course directories. `replaced-problems/`
holds the prior live Pybites directories. None of these paths is in the served content directory.

To reverse the course replacement, move `courses/software-engineering` out of the
live content directory and restore the original three indexes from the backup.
Restore the prior Pybites definitions from the backup if required. Keep the
`progress` directory and all learner data in place. New ticket problem files can
stay on disk without a course index.
