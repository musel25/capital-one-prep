from fastapi import HTTPException


def borrow(catalog, request):
    book = catalog.get_book(request.book_id)
    if not book['available']:
        raise HTTPException(409, 'Book is already checked out')
    loan = {'id': f'loan-{len(catalog.loans) + 1}', **request.model_dump()}
    book['available'] = False
    catalog.loans.append(loan)
    return loan
