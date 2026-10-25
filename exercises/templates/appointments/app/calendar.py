from fastapi import HTTPException


class Calendar:
    def __init__(self):
        self.providers = [
            {'id': 'aria', 'name': 'Aria - bicycle repair'},
            {'id': 'ben', 'name': 'Ben - appliance repair'},
        ]
        self.hours = {
            ('aria', '2026-10-26'): (540, 720),
            ('aria', '2026-10-27'): (780, 840),
            ('ben', '2026-10-26'): (600, 660),
        }
        self.bookings = [
            {'id': 'b1', 'provider_id': 'aria', 'date': '2026-10-26', 'start': '10:00', 'end': '10:30', 'status': 'confirmed'},
            {'id': 'b2', 'provider_id': 'aria', 'date': '2026-10-26', 'start': '11:00', 'end': '11:30', 'status': 'canceled'},
            {'id': 'b3', 'provider_id': 'ben', 'date': '2026-10-26', 'start': '10:00', 'end': '10:30', 'status': 'confirmed'},
        ]

    def require_provider(self, provider_id):
        if not any(provider['id'] == provider_id for provider in self.providers):
            raise HTTPException(404, 'Provider not found')
