from fastapi import HTTPException
from .presentation import summary_payload


def employee_summary(ledger, employee_id, month):
    ledger.require_employee(employee_id)
    categories = {}
    for row in ledger.expenses:
        if row['employee_id'] != employee_id or row['incurred_on'][:7] != month:
            continue
        if row['status'] not in ('approved', 'pending'):
            continue
        totals = categories.setdefault(row['category'], {'approved_cents': 0, 'pending_cents': 0})
        totals[f"{row['status']}_cents"] += row['amount_cents']
    return summary_payload(employee_id, month, categories)
