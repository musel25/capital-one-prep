"""Existing single-product reservation and cancellation behavior."""
from fastapi.testclient import TestClient
from app.main import create_app


def test_single_product_reservation_can_be_canceled():
    with TestClient(create_app()) as client:
        before = client.get('/api/products').json()
        created = client.post('/api/reservations', json={'items': [{'sku': 'dock', 'quantity': 1}]})
        assert created.status_code == 201
        rid = created.json()['id']
        assert client.get('/api/products').json()['items'][0]['available'] == 4
        canceled = client.post(f'/api/reservations/{rid}/cancel')
        assert canceled.status_code == 200
        assert canceled.json()['status'] == 'canceled'
        assert client.get('/api/products').json() == before


def test_unknown_cancellation_does_not_change_products():
    with TestClient(create_app()) as client:
        before = client.get('/api/products').json()
        assert client.post('/api/reservations/missing/cancel').status_code == 404
        assert client.get('/api/products').json() == before
