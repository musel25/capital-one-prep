"""Existing membership and request validation behavior."""
from fastapi.testclient import TestClient
from app.main import create_app


def test_inactive_member_does_not_qualify():
    with TestClient(create_app()) as client:
        response = client.post('/api/eligibility', json={
            'at': '2026-10-31T12:00:00Z', 'amount_cents': 6000, 'active_member': False,
        })
        assert response.status_code == 200
        assert response.json() == {'eligible': False}


def test_amount_requires_strict_positive_integer():
    with TestClient(create_app()) as client:
        for amount in (True, '5000', 0, -1, 5000.5):
            assert client.post('/api/eligibility', json={
                'at': '2026-10-31T12:00:00Z', 'amount_cents': amount, 'active_member': True,
            }).status_code == 422
