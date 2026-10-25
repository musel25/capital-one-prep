from copy import deepcopy
from .cache import invalidate


def record(store, ticket_id, kind, actor, detail):
    event = {'sequence': len(store.events) + 1, 'ticket_id': ticket_id,
             'kind': kind, 'actor': actor, 'detail': detail}
    store.events.append(event)
    invalidate(store)
    return deepcopy(event)


def history(store, ticket_id=None):
    if ticket_id is not None:
        store.ticket(ticket_id)
    return {'items': deepcopy([e for e in store.events if ticket_id is None or e['ticket_id'] == ticket_id])}
