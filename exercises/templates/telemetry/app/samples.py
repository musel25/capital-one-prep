from fastapi import HTTPException


class Samples:
    def __init__(self):
        self.services = [{'id': 'atlas', 'name': 'Atlas search'}, {'id': 'beacon', 'name': 'Beacon notifications'}]
        self.rows = [
            {'id': 'r1', 'service_id': 'atlas', 'duration_us': 125000, 'status': 'ok'},
            {'id': 'r2', 'service_id': 'atlas', 'duration_us': 1500, 'status': 'ok'},
            {'id': 'r3', 'service_id': 'atlas', 'duration_us': 250000, 'status': 'error'},
            {'id': 'r4', 'service_id': 'beacon', 'duration_us': 0, 'status': 'ok'},
        ]

    def require_service(self, service_id):
        if not any(row['id'] == service_id for row in self.services):
            raise HTTPException(404, 'Service not found')

    def for_service(self, service_id):
        self.require_service(service_id)
        return [row for row in self.rows if row['service_id'] == service_id]

    def collect(self, request):
        self.require_service(request.service_id)
        row = {'id': f'r{len(self.rows) + 1}', **request.model_dump()}
        self.rows.append(row)
        return row
