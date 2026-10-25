from fastapi.testclient import TestClient
from app.main import create_app


def test_ticket_details_and_missing_ticket():
    client = TestClient(create_app())
    assert len(client.get('/api/tickets').json()['items']) == 3
    assert client.get('/api/tickets/t-101').json()['subject'] == 'Printer cannot connect'
    assert client.get('/api/tickets/missing').status_code == 404


def test_comment_creation_validates_text():
    client = TestClient(create_app())
    response = client.post('/api/tickets/t-101/comments', json={'author': 'Jo', 'body': 'Checking the cable.'})
    assert response.status_code == 201
    assert response.json()['body'] == 'Checking the cable.'
    assert client.post('/api/tickets/t-101/comments', json={'author': 'Jo', 'body': ' '}).status_code == 422
    assert client.post('/api/tickets/missing/comments', json={'author': 'Jo', 'body': 'Hello'}).status_code == 404


def test_status_update_is_visible_on_ticket():
    client = TestClient(create_app())
    assert client.post('/api/tickets/t-103/status', json={'actor': 'Jo', 'status': 'open'}).status_code == 200
    assert client.get('/api/tickets/t-103').json()['status'] == 'open'
    assert client.post('/api/tickets/t-103/status', json={'actor': 'Jo', 'status': 'lost'}).status_code == 422
    assert client.get('/api/tickets/t-103').json()['status'] == 'open'
