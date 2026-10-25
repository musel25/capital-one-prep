from fastapi import HTTPException


def import_contacts(directory, request):
    emails = set()
    for contact in request.contacts:
        if contact.email in emails or directory.has_email(contact.email):
            raise HTTPException(409, 'Email already exists in the directory or import')
        emails.add(contact.email)
    return {'items': [directory.append(contact) for contact in request.contacts]}
