from fastapi import HTTPException


class Ledger:
    def __init__(self):
        self.employees = [{'id': 'ada', 'name': 'Ada'}, {'id': 'bo', 'name': 'Bo'}, {'id': 'cam', 'name': 'Cam'}]
        fixtures = [
            ('e1', 'ada', '2026-10-03', 'travel', 4200, 'approved', 'Train to site'),
            ('e2', 'ada', '2026-10-04', 'meals', 1200, 'pending', 'Team lunch'),
            ('e3', 'ada', '2026-10-05', 'travel', 800, 'rejected', 'Duplicate fare'),
            ('e4', 'ada', '2026-10-06', 'meals', 900, 'approved', 'Site visit lunch'),
            ('e5', 'ada', '2026-09-30', 'travel', 2000, 'approved', 'September train'),
            ('e6', 'cam', '2026-10-06', 'meals', 500, 'approved', 'Site breakfast'),
            ('e7', 'ada', '2026-10-07', 'supplies', 600, 'rejected', 'Personal stationery'),
        ]
        fields = ('id', 'employee_id', 'incurred_on', 'category', 'amount_cents', 'status', 'description')
        self.expenses = [dict(zip(fields, row)) for row in fixtures]

    def require_employee(self, employee_id):
        if not any(row['id'] == employee_id for row in self.employees):
            raise HTTPException(404, 'Employee not found')

    def submit(self, request):
        self.require_employee(request.employee_id)
        row = {'id': f'e{len(self.expenses) + 1}', **request.model_dump(mode='json'), 'status': 'pending'}
        self.expenses.append(row)
        return row
