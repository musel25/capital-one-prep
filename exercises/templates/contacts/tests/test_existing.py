from fastapi.testclient import TestClient
from app.main import create_app


def test_directory_lookup_and_unknown_contact():
    c = TestClient(create_app())
    first = c.get('/api/contacts').json()['items'][0]
    assert first['email'] == 'kai@example.com'
    assert c.get('/api/contacts/c1').json() == first
    assert c.get('/api/contacts/missing').status_code == 404


def test_individual_creation_normalizes_fields_and_rejects_duplicates():
    c = TestClient(create_app())
    body = {'name': '  Rae Lin ', 'email': ' RAE@example.com ', 'team': 'events'}
    r = c.post('/api/contacts', json=body)
    assert r.status_code == 201
    assert r.json() == {'id': 'c3', 'name': 'Rae Lin', 'email': 'rae@example.com', 'team': 'events'}
    before = c.get('/api/contacts').json()
    assert c.post('/api/contacts', json=body).status_code == 409
    assert c.post('/api/contacts', json={**body, 'email': 'invalid'}).status_code == 422
    assert c.get('/api/contacts').json() == before
