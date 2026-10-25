"""Learner briefs for revision 2; original attempts retain revision 1 contracts."""
from dataclasses import asdict, dataclass, replace

from exercises.legacy.catalog import TASKS as LEGACY_TASKS, BY_ID as LEGACY_BY_ID
from exercises.scenarios.early import TASK_DATA as EARLY
from exercises.scenarios.middle import TASK_DATA as MIDDLE
from exercises.scenarios.late import TASK_DATA as LATE


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    context: str
    brief: str
    contract: str
    probe: str
    minutes: int = 20
    orientation: str = ''


ORIENTATIONS = {
    'bank': 'Cedar Wallet tracks accounts, transfers and seven fictional purchase/refund records. Checking starts with 100000 cents and savings with 20000. Some records use different timezone offsets and some are pending.',
    'settlements': 'Fern Merchant Operations provides a payout preview for fictional merchants. Charges have a lifecycle, a settlement flag, a gross amount and a fee in integer cents.',
    'promotions': 'Juniper Rewards evaluates fictional purchases against a time-limited promotion. The product records purchase instants, membership and amounts in cents.',
    'inventory': 'Harbor Supply tracks product availability and reservations. Its initial catalog has 5 docks and 10 cables; each request can contain several lines.',
}

UPDATES = {**EARLY, **MIDDLE, **LATE}
assert len(UPDATES) == len(EARLY) + len(MIDDLE) + len(LATE), 'Duplicate scenario task ID'
TASKS = [Task(id=old.id, **UPDATES[old.id]) if old.id in UPDATES
         else Task(**asdict(old), orientation=ORIENTATIONS[old.context])
         for old in LEGACY_TASKS]

# Keep the unseen late bug applications; lead with symptoms instead of a recipe.
OPENINGS = {
    'd08-bug': ('Investigate a payout preview discrepancy',
                'A merchant says the payout preview includes a charge that should not be paid out yet. Investigate the report and repair the behavior without changing charge records.'),
    'd09-bug': ('Investigate a promotion complaint',
                'Support received a complaint about an offer being shown after its advertised availability. Establish a reproducible example and repair the decision while preserving other eligibility rules.'),
    'd10-bug': ('Investigate rejected supply orders',
                'The warehouse reports that a rejected multi-item order changed what can be reserved afterward. Investigate and repair the behavior without changing initial stock.'),
}
TASKS = [replace(task, title=OPENINGS[task.id][0], brief=OPENINGS[task.id][1])
         if task.id in OPENINGS else task for task in TASKS]
BY_ID = {task.id: task for task in TASKS}


def public_tasks():
    return [asdict(task) for task in TASKS]
