from fastapi import HTTPException


class Directory:
    def __init__(self):
        self.contacts = [
            {'id': 'c1', 'name': 'Kai Moss', 'email': 'kai@example.com', 'team': 'events'},
            {'id': 'c2', 'name': 'Nia Reed', 'email': 'nia@example.com', 'team': 'support'},
        ]

    def find(self, contact_id):
        for row in self.contacts:
            if row['id'] == contact_id:
                return row
        raise HTTPException(404, 'Contact not found')

    def has_email(self, email):
        return any(row['email'] == email for row in self.contacts)

    def append(self, request):
        row = {'id': f'c{len(self.contacts) + 1}', **request.model_dump()}
        self.contacts.append(row)
        return row
