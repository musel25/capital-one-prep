from fastapi.testclient import TestClient
from app.main import create_app


def test_book_lookup_and_missing_book():
    client = TestClient(create_app())
    assert client.get('/api/books/b-01').json()['title'] == 'A Brief Atlas'
    assert client.get('/api/books/missing').status_code == 404


def test_checkout_changes_availability_and_records_reader():
    client = TestClient(create_app())
    response = client.post('/api/loans', json={'book_id': 'b-01', 'reader': 'Alex'})
    assert response.status_code == 201
    assert client.get('/api/books/b-01').json()['available'] is False
    assert client.get('/api/loans').json()['items'][0]['reader'] == 'Alex'
    assert client.post('/api/loans', json={'book_id': 'b-01', 'reader': 'Alex'}).status_code == 409


def test_rejected_checkout_creates_no_loan():
    client = TestClient(create_app())
    assert client.post('/api/loans', json={'book_id': 'missing', 'reader': 'Alex'}).status_code == 404
    assert client.post('/api/loans', json={'book_id': 'b-01', 'reader': ' '}).status_code == 422
    assert client.get('/api/loans').json() == {'items': []}
