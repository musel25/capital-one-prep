from fastapi import HTTPException


def get_ticket(store, ticket_id):
    if ticket_id not in store.tickets:
        raise HTTPException(404, 'Ticket not found')
    return store.tickets[ticket_id]


def add_comment(store, ticket_id, request):
    get_ticket(store, ticket_id)
    comment = {'ticket_id': ticket_id, 'sequence': store.next_sequence(), **request.model_dump()}
    store.comments.append(comment)
    return comment


def change_status(store, ticket_id, request):
    ticket = get_ticket(store, ticket_id)
    if ticket['status'] != request.status:
        store.transitions.append({
            'ticket_id': ticket_id, 'sequence': store.next_sequence(), 'actor': request.actor,
            'previous': ticket['status'], 'current': request.status,
        })
        ticket['status'] = request.status
    return ticket
