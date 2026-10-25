from .cache import cached_rows
from .pagination import page_of
from .search import select_tickets


def queue_report(store, team, status, page, page_size):
    rows = cached_rows(store, team, status, lambda: select_tickets(store, team, status))
    return page_of(rows, page, page_size)


def overview(store):
    rows = store.ticket_snapshot()
    return {'open': sum(t['status'] == 'open' for t in rows),
            'unassigned_open': sum(t['status'] == 'open' and t['assignee'] is None for t in rows),
            'resolved': sum(t['status'] == 'resolved' for t in rows),
            'events': len(store.events)}
