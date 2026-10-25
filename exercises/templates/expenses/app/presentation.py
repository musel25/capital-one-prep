def summary_payload(employee_id, month, categories):
    items = [{'category': category, **totals} for category, totals in sorted(categories.items())]
    return {'employee_id': employee_id, 'month': month,
            'approved_cents': sum(row['approved_cents'] for row in items),
            'pending_cents': sum(row['pending_cents'] for row in items), 'items': items}
