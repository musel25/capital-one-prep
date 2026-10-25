from copy import deepcopy
from .events import record


def comment(store, ticket_id, request):
    store.ticket(ticket_id)
    return record(store, ticket_id, 'comment', request.actor, {'body': request.body})


def change_status(store, ticket_id, request):
    ticket = store.ticket(ticket_id)
    previous = ticket['status']
    if previous != request.status:
        ticket['status'] = request.status
        record(store, ticket_id, 'status', request.actor, {'previous': previous, 'current': request.status})
    return deepcopy(ticket)
