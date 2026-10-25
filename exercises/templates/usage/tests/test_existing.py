from fastapi.testclient import TestClient
from app.main import create_app


def test_raw_events_preserve_delivery_identity_and_review_state():
    c = TestClient(create_app())
    rows = c.get('/api/events').json()['items']
    assert len(rows) == 8
    assert rows[0]['event_id'] != rows[1]['event_id']
    assert {row['status'] for row in rows} == {'accepted', 'pending', 'rejected'}


def test_ingest_adds_a_delivery_and_rejects_a_reused_event_id():
    c = TestClient(create_app())
    body = {'event_id': 'new-delivery', 'workspace_id': 'north', 'month': '2026-10',
            'meter_id': 'api', 'sample_id': 'new-sample', 'units': 5, 'status': 'pending'}
    assert c.post('/api/events', json=body).status_code == 201
    before = c.get('/api/events').json()
    assert before['items'][-1] == body
    assert c.post('/api/events', json=body).status_code == 409
    assert c.post('/api/events', json={**body, 'event_id': 'other', 'workspace_id': 'unknown'}).status_code == 404
    assert c.post('/api/events', json={**body, 'units': 0}).status_code == 422
    assert c.get('/api/events').json() == before
