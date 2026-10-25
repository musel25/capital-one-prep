class Library:
    def __init__(self):
        self.equipment = {
            'camera': {'id': 'camera', 'name': 'Mirrorless camera', 'total': 3, 'available': 1},
            'tripod': {'id': 'tripod', 'name': 'Travel tripod', 'total': 2, 'available': 1},
        }
        self.loans = {
            'loan-1': {'id': 'loan-1', 'equipment_id': 'camera', 'borrower': 'Ada', 'quantity': 1, 'status': 'active'},
            'loan-2': {'id': 'loan-2', 'equipment_id': 'camera', 'borrower': 'Ben', 'quantity': 1, 'status': 'active'},
            'loan-3': {'id': 'loan-3', 'equipment_id': 'tripod', 'borrower': 'Cam', 'quantity': 1, 'status': 'active'},
            'loan-4': {'id': 'loan-4', 'equipment_id': 'tripod', 'borrower': 'Dee', 'quantity': 1, 'status': 'returned'},
        }
