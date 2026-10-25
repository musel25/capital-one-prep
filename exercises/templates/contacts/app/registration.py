from fastapi import HTTPException


def register(directory, request):
    if directory.has_email(request.email):
        raise HTTPException(409, 'Email already exists')
    return directory.append(request)
