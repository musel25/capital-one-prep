from fastapi import HTTPException

from .loans import find_loan


def accept_return(library, loan_id):
    loan = find_loan(library, loan_id)
    if loan['status'] == 'returned':
        return loan
    library.equipment[loan['equipment_id']]['available'] += loan['quantity']
    loan['status'] = 'returned'
    return loan
