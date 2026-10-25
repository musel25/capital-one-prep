"""Public checks cover unrelated existing behavior, not the assigned task."""
from fastapi.testclient import TestClient
from app.main import create_app


def test_catalog_and_atomic_reservation():
    c = TestClient(create_app())
    before = c.get('/api/inventory').json()
    failed = c.post('/api/orders', json={'customer': 'Rae', 'items': [{'sku': 'dock', 'quantity': 1}, {'sku': 'cable', 'quantity': 6}]})
    assert failed.status_code == 409 and c.get('/api/inventory').json() == before
    assert c.get('/api/events').json() == {'items': []}
    response = c.post('/api/orders', json={'customer': 'Rae', 'items': [{'sku': 'dock', 'quantity': 1}]})
    assert response.status_code == 201 and response.json()['status'] == 'reserved'
    assert c.get('/api/inventory').json()['items'][1]['available'] == 3
    assert c.get('/api/orders/missing').status_code == 404


def test_single_parcel_shipment_and_tracking():
    c = TestClient(create_app())
    response = c.post('/api/shipments', json={'order_id': 'o-2', 'service': 'standard'})
    assert response.status_code == 201 and response.json()['total_cents'] == 180
    assert c.get('/api/orders/o-2').json()['status'] == 'shipped'
    assert c.get('/api/shipments/s-1').json()['events'][0]['kind'] == 'shipped'
    assert c.post('/api/shipments', json={'order_id': 'o-2', 'service': 'standard'}).status_code == 409
    assert c.get('/api/shipments/unknown').status_code == 404


def test_app_instances_are_independent():
    first, second = TestClient(create_app()), TestClient(create_app())
    first.post('/api/shipments', json={'order_id': 'o-2', 'service': 'standard'})
    assert second.get('/api/orders/o-2').json()['status'] == 'reserved'
