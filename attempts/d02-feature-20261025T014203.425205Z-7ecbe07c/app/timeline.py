from .tickets import get_ticket


def timeline(store, ticket_id):
    get_ticket(store, ticket_id)
    events = []

    for comment in store.comments:
        if comment['ticket_id'] == ticket_id:
            events.append({
                'id': f"event-{comment['sequence']}",
                'sequence': comment['sequence'],
                'kind': 'comment',
                'actor': comment['author'],
                'text': comment['body'],
            })

    for transition in store.transitions:
        if transition['ticket_id'] == ticket_id:
            events.append({
                'id': f"event-{transition['sequence']}",
                'sequence': transition['sequence'],
                'kind': 'status',
                'actor': transition['actor'],
                'text': f"{transition['previous']} → {transition['current']}",
            })

    return {'items': sorted(events, key=lambda event: event['sequence'])}
