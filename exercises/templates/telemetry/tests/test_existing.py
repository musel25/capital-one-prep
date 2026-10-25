from fastapi.testclient import TestClient
from app.main import create_app


def test_summary_counts_success_errors_and_slow_samples():
    c = TestClient(create_app())
    assert c.get('/api/services/atlas/summary').json() == {
        'service_id': 'atlas', 'count': 3, 'error_count': 1, 'slow_count': 1,
    }
    assert c.get('/api/services/unknown/summary').status_code == 404


def test_collection_keeps_service_samples_separate_and_rejects_invalid_input():
    c = TestClient(create_app())
    r = c.post('/api/readings', json={'service_id': 'beacon', 'duration_us': 250000, 'status': 'error'})
    assert r.status_code == 201 and r.json()['service_id'] == 'beacon'
    assert c.get('/api/services/beacon/summary').json() == {
        'service_id': 'beacon', 'count': 2, 'error_count': 1, 'slow_count': 1,
    }
    before = c.get('/api/services/beacon/readings').json()
    assert c.post('/api/readings', json={'service_id': 'beacon', 'duration_us': -1, 'status': 'ok'}).status_code == 422
    assert c.post('/api/readings', json={'service_id': 'unknown', 'duration_us': 1, 'status': 'ok'}).status_code == 404
    assert c.get('/api/services/beacon/readings').json() == before
    assert c.get('/api/services/atlas/summary').json()['count'] == 3
