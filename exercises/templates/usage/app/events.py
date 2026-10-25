from fastapi import HTTPException


class EventFeed:
    def __init__(self):
        self.workspaces = [{'id': 'north', 'name': 'North lab'}, {'id': 'south', 'name': 'South lab'}]
        fixtures = [
            ('delivery-1', 'north', '2026-10', 'api', 's1', 100, 'accepted'),
            ('delivery-2', 'north', '2026-10', 'api', 's1', 100, 'accepted'),
            ('delivery-3', 'north', '2026-10', 'api', 's2', 40, 'accepted'),
            ('delivery-4', 'north', '2026-10', 'api', 's3', 900, 'rejected'),
            ('delivery-5', 'north', '2026-10', 'api', 's4', 20, 'pending'),
            ('delivery-6', 'south', '2026-10', 'api', 's1', 10, 'accepted'),
            ('delivery-7', 'north', '2026-09', 'api', 's1', 25, 'accepted'),
            ('delivery-8', 'north', '2026-10', 'storage', 's1', 7, 'accepted'),
        ]
        fields = ('event_id', 'workspace_id', 'month', 'meter_id', 'sample_id', 'units', 'status')
        self.events = [dict(zip(fields, row)) for row in fixtures]

    def require_workspace(self, workspace_id):
        if not any(row['id'] == workspace_id for row in self.workspaces):
            raise HTTPException(404, 'Workspace not found')

    def append(self, request):
        self.require_workspace(request.workspace_id)
        if any(row['event_id'] == request.event_id for row in self.events):
            raise HTTPException(409, 'Delivery ID already exists')
        row = request.model_dump()
        self.events.append(row)
        return row
