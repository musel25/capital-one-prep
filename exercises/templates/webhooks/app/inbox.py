class Inbox:
    def __init__(self):
        self.parcels = {
            'parcel-101': {'id': 'parcel-101', 'recipient': 'Ada', 'locker': 'A-12'},
            'parcel-102': {'id': 'parcel-102', 'recipient': 'Ben', 'locker': 'B-03'},
        }
        self.receipts = {}
        self.notifications = []
