from fastapi.testclient import TestClient

from app.main import create_app


def test_known_parcels_are_visible():
    client = TestClient(create_app())
    parcels = client.get('/api/parcels').json()['items']
    assert [parcel['id'] for parcel in parcels] == ['parcel-101', 'parcel-102']
    assert parcels[0]['locker'] == 'A-12'
    assert client.get('/api/notifications').json() == {'items': []}


def test_first_delivery_produces_a_notification():
    client = TestClient(create_app())
    result = client.post('/api/deliveries', json={'event_id': 'new', 'parcel_id': 'parcel-101', 'status': 'arrived'})
    assert result.status_code == 200
    assert result.json() == {'event_id': 'new', 'accepted': True, 'notification_id': 'n-1'}
    notification = client.get('/api/notifications').json()['items'][0]
    assert notification['recipient'] == 'Ada'
    assert 'arrived' in notification['message']


def test_invalid_delivery_does_not_send_a_notification():
    client = TestClient(create_app())
    body = {'event_id': 'new', 'parcel_id': 'unknown', 'status': 'delayed'}
    assert client.post('/api/deliveries', json=body).status_code == 404
    assert client.post('/api/deliveries', json={**body, 'status': 'lost'}).status_code == 422
    assert client.get('/api/notifications').json() == {'items': []}
    assert client.get('/api/deliveries').json() == {'items': []}
