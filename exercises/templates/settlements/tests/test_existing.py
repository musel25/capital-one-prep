"""Existing charge-feed behavior; add regression tests for your task."""
from fastapi.testclient import TestClient
from app.main import create_app


def test_charge_feed_preserves_lifecycle_data_between_reads():
    with TestClient(create_app()) as client:
        first = client.get('/api/charges')
        assert first.status_code == 200
        assert len(first.json()['items']) == 6
        assert {row['status'] for row in first.json()['items']} == {'captured', 'refunded', 'authorized'}
        assert client.get('/api/charges').json() == first.json()


def test_unknown_merchant_has_no_preview():
    with TestClient(create_app()) as client:
        response = client.get('/api/settlements', params={'merchant_id': 'unknown'})
        assert response.status_code == 200
        assert response.json() == {'items': []}
