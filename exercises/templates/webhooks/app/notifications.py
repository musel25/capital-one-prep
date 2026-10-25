def notify(inbox, parcel, status):
    notification = {
        'id': f'n-{len(inbox.notifications) + 1}',
        'parcel_id': parcel['id'],
        'recipient': parcel['recipient'],
        'message': f"Parcel {parcel['id']} is {status} at locker {parcel['locker']}.",
    }
    inbox.notifications.append(notification)
    return notification
