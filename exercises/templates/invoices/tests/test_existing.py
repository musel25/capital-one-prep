from fastapi.testclient import TestClient
from app.main import create_app


def test_catalog_has_prices_and_unknown_product_returns_404():
    client = TestClient(create_app())
    assert len(client.get('/api/products').json()['items']) == 3
    assert client.get('/api/products/notebook').json()['unit_cents'] == 999
    assert client.get('/api/products/missing').status_code == 404


def test_undiscounted_invoice_preserves_line_order():
    client = TestClient(create_app())
    response = client.post('/api/invoices/preview', json={'lines': [{'sku': 'clips', 'quantity': 2}, {'sku': 'notebook', 'quantity': 1}]})
    assert response.status_code == 200
    assert [line['sku'] for line in response.json()['lines']] == ['clips', 'notebook']
    assert response.json()['total_cents'] == 1209


def test_invalid_line_does_not_change_catalog():
    client = TestClient(create_app())
    before = client.get('/api/products').json()
    assert client.post('/api/invoices/preview', json={'lines': [{'sku': 'notebook', 'quantity': 0}]}).status_code == 422
    assert client.post('/api/invoices/preview', json={'lines': [{'sku': 'missing', 'quantity': 1}]}).status_code == 404
    assert client.get('/api/products').json() == before
