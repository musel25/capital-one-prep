from fastapi import HTTPException
from .events import record


def assign_many(store, request):
    agent = store.agent(request.agent_id)
    if not agent['active']:
        raise HTTPException(409, 'Agent is inactive')
    ids = list(dict.fromkeys(request.ticket_ids))
    tickets = [store.ticket(ticket_id) for ticket_id in ids]
    for ticket in tickets:
        if ticket['team'] != agent['team'] or ticket['status'] != 'open':
            raise HTTPException(409, 'All tickets must be open and belong to the agent team')
    updated = []
    for ticket in tickets:
        if ticket['assignee'] != agent['id']:
            previous = ticket['assignee']
            ticket['assignee'] = agent['id']
            record(store, ticket['id'], 'assignment', request.actor,
                   {'previous': previous, 'current': agent['id']})
            updated.append(ticket['id'])
    return {'updated': updated}
