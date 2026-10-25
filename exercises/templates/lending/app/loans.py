from fastapi import HTTPException


def checkout(library, request):
    equipment = library.equipment.get(request.equipment_id)
    if equipment is None:
        raise HTTPException(404, 'Equipment not found')
    if equipment['available'] < request.quantity:
        raise HTTPException(409, 'Not enough equipment available')
    loan = {'id': f'loan-{len(library.loans) + 1}', **request.model_dump(), 'status': 'active'}
    equipment['available'] -= request.quantity
    library.loans[loan['id']] = loan
    return loan


def find_loan(library, loan_id):
    if loan_id not in library.loans:
        raise HTTPException(404, 'Loan not found')
    return library.loans[loan_id]
