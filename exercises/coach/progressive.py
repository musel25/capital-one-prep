"""Instructor reference. Never copy this into a learner attempt."""
def summarize(events):
    seen = {}
    purchases = {}
    remaining = {}
    totals = {}
    for event in events:
        event_id = event['id']
        if event_id in seen:
            if seen[event_id] != event:
                raise ValueError('Conflicting event ID')
            continue
        if event['type'] == 'purchase':
            merchant, amount = event['merchant'], event['amount']
            purchases[event_id] = merchant
            remaining[event_id] = amount
            totals[merchant] = totals.get(merchant, 0) + amount
        else:
            purchase_id, amount = event['purchase_id'], event['amount']
            if purchase_id not in purchases or amount > remaining[purchase_id]:
                raise ValueError('Unknown purchase or excessive refund')
            remaining[purchase_id] -= amount
            totals[purchases[purchase_id]] -= amount
        seen[event_id] = dict(event)
    return totals
