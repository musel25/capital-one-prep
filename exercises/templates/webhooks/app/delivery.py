from fastapi import HTTPException

from .notifications import notify


def receive(inbox, event):
    payload = event.model_dump()
    previous = inbox.receipts.get(event.event_id)
    if previous is not None:
        if previous['payload'] != payload:
            raise HTTPException(409, 'Event ID belongs to a different delivery')
        return previous['result']
    parcel = inbox.parcels.get(event.parcel_id)
    if parcel is None:
        raise HTTPException(404, 'Parcel not found')
    notification = notify(inbox, parcel, event.status)
    result = {'event_id': event.event_id, 'accepted': True, 'notification_id': notification['id']}
    inbox.receipts[event.event_id] = {'payload': payload, 'result': result}
    return result
