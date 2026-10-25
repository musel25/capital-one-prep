from fastapi.testclient import TestClient
from app.main import create_app


def test_employees_and_review_states_are_visible():
    c = TestClient(create_app())
    assert [e['id'] for e in c.get('/api/employees').json()['items']] == ['ada', 'bo', 'cam']
    rows = c.get('/api/expenses').json()['items']
    assert len(rows) == 7 and {e['status'] for e in rows} == {'approved', 'pending', 'rejected'}


def test_submission_is_pending_and_invalid_claims_do_not_append():
    c = TestClient(create_app())
    body = {'employee_id': 'bo', 'incurred_on': '2026-10-26', 'category': 'travel',
            'amount_cents': 100, 'description': 'Bus fare'}
    r = c.post('/api/expenses', json=body)
    assert r.status_code == 201 and r.json()['status'] == 'pending'
    assert c.get('/api/expenses').json()['items'][-1]['description'] == 'Bus fare'
    before = c.get('/api/expenses').json()
    assert c.post('/api/expenses', json={**body, 'employee_id': 'unknown'}).status_code == 404
    assert c.post('/api/expenses', json={**body, 'description': '   '}).status_code == 422
    assert c.post('/api/expenses', json={**body, 'amount_cents': '100'}).status_code == 422
    assert c.get('/api/expenses').json() == before
