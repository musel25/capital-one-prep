from fastapi.testclient import TestClient

from app.main import create_app


def test_inventory_and_existing_loans_are_visible():
    client = TestClient(create_app())
    equipment = client.get('/api/equipment').json()['items']
    assert [(item['id'], item['available']) for item in equipment] == [('camera', 1), ('tripod', 1)]
    assert client.get('/api/loans/loan-1').json()['borrower'] == 'Ada'
    assert client.get('/api/loans/loan-4').json()['status'] == 'returned'


def test_checkout_records_loan_and_reduces_availability():
    client = TestClient(create_app())
    result = client.post('/api/loans', json={'equipment_id': 'camera', 'borrower': 'Eli', 'quantity': 1})
    assert result.status_code == 201
    assert result.json()['status'] == 'active'
    assert client.get('/api/loans').json()['items'][-1] == result.json()
    assert client.get('/api/equipment').json()['items'][0]['available'] == 0


def test_rejected_checkout_does_not_change_inventory_or_loans():
    client = TestClient(create_app())
    before = [client.get(path).json() for path in ('/api/equipment', '/api/loans')]
    request = {'equipment_id': 'camera', 'borrower': 'Eli', 'quantity': 2}
    assert client.post('/api/loans', json=request).status_code == 409
    assert client.post('/api/loans', json={**request, 'equipment_id': 'missing'}).status_code == 404
    assert client.post('/api/loans', json={**request, 'quantity': 0}).status_code == 422
    assert [client.get(path).json() for path in ('/api/equipment', '/api/loans')] == before
