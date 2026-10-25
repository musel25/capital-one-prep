from fastapi.testclient import TestClient
from app.main import create_app


def test_roster_and_booking_states_remain_visible():
    c = TestClient(create_app())
    assert [p['id'] for p in c.get('/api/providers').json()['items']] == ['aria', 'ben']
    assert [b['status'] for b in c.get('/api/bookings').json()['items']] == ['confirmed', 'canceled', 'confirmed']


def test_booking_creation_and_conflict_leave_consistent_history():
    c = TestClient(create_app())
    body = {'provider_id': 'aria', 'on': '2026-10-26', 'start': '09:00', 'duration_minutes': 30}
    r = c.post('/api/bookings', json=body)
    assert r.status_code == 201 and r.json()['status'] == 'confirmed'
    before = c.get('/api/bookings').json()
    assert c.post('/api/bookings', json=body).status_code == 409
    assert c.post('/api/bookings', json={**body, 'provider_id': 'unknown'}).status_code == 404
    assert c.post('/api/bookings', json={**body, 'start': '9am'}).status_code == 422
    assert c.get('/api/bookings').json() == before
