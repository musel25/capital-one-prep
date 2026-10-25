"""Public behavior checks. Add tests for your assigned issue independently."""
from fastapi.testclient import TestClient
from app.main import create_app


def test_directory_and_ticket_search():
    c = TestClient(create_app())
    assert len(c.get('/api/agents').json()['items']) == 3
    assert [t['id'] for t in c.get('/api/tickets/search?q=BUILD').json()['items']] == ['t-1']
    assert c.get('/api/tickets/missing').status_code == 404


def test_comment_and_status_workflow_and_event_order():
    c = TestClient(create_app())
    assert c.post('/api/tickets/t-1/comments', json={'actor': 'Rae', 'body': 'Investigating'}).status_code == 201
    response = c.post('/api/tickets/t-1/status', json={'actor': 'Rae', 'status': 'resolved'})
    assert response.json()['status'] == 'resolved'
    assert c.get('/api/overview').json()['resolved'] == 2
    rows = c.get('/api/tickets/t-1/events').json()['items']
    assert [e['kind'] for e in rows] == ['comment', 'status']
    assert [e['sequence'] for e in rows] == [1, 2]
    c.post('/api/tickets/t-1/status', json={'actor': 'Rae', 'status': 'resolved'})
    assert c.get('/api/tickets/t-1/events').json()['items'] == rows
    assert c.post('/api/tickets/t-1/comments', json={'actor': 'Rae', 'body': ' '}).status_code == 422


def test_application_instances_do_not_share_state():
    first, second = TestClient(create_app()), TestClient(create_app())
    first.post('/api/tickets/t-1/status', json={'actor': 'Rae', 'status': 'resolved'})
    assert second.get('/api/tickets/t-1').json()['status'] == 'open'
