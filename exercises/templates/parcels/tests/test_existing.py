from fastapi.testclient import TestClient
from app.main import create_app


def test_rate_cards_are_available():
    client = TestClient(create_app())
    rates = client.get('/api/rates').json()['items']
    assert [row['zone'] for row in rates] == ['local', 'regional', 'remote']
    assert client.get('/api/rates/regional').json()['standard_days'] == 4


def test_unknown_rate_card_returns_404():
    client = TestClient(create_app())
    assert client.get('/api/rates/missing').status_code == 404
    assert len(client.get('/api/rates').json()['items']) == 3


def test_quote_request_rejects_invalid_weight_and_service():
    client = TestClient(create_app())
    body = {'zone': 'local', 'service': 'standard', 'weight_grams': 500}
    for change in [{'weight_grams': 0}, {'weight_grams': True}, {'service': 'teleport'}]:
        assert client.post('/api/quotes', json={**body, **change}).status_code == 422
