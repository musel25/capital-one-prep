"""Timeline API expectations; each test gets a fresh in-memory application."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client():
    with TestClient(create_app()) as client:
        yield client


def read_timeline(client, ticket_id):
    response = client.get(f'/api/tickets/{ticket_id}/timeline')
    assert response.status_code == 200, response.text
    return response.json()


def test_timeline_combines_seeded_events_in_sequence_order(client):
    # Sequence 2 belongs to another ticket: gaps must be preserved.
    assert read_timeline(client, 't-101') == {'items': [
        {'id': 'event-1', 'sequence': 1, 'kind': 'status',
         'actor': 'Mina', 'text': 'new → open'},
        {'id': 'event-3', 'sequence': 3, 'kind': 'comment',
         'actor': 'Jo', 'text': 'The printer is on the guest network.'},
    ]}


def test_timeline_immediately_interleaves_new_comments_and_status_changes(client):
    first = client.post('/api/tickets/t-103/comments',
                        json={'author': 'Musel', 'body': 'Checking access.'})
    assert first.status_code == 201
    assert first.json()['body'] == 'Checking access.'
    assert client.post('/api/tickets/t-103/status',
                       json={'actor': 'Alex', 'status': 'open'}).status_code == 200
    assert client.post('/api/tickets/t-103/comments',
                       json={'author': 'Jo', 'body': 'Access confirmed.'}).status_code == 201

    assert read_timeline(client, 't-103') == {'items': [
        {'id': 'event-4', 'sequence': 4, 'kind': 'comment',
         'actor': 'Musel', 'text': 'Checking access.'},
        {'id': 'event-5', 'sequence': 5, 'kind': 'status',
         'actor': 'Alex', 'text': 'new → open'},
        {'id': 'event-6', 'sequence': 6, 'kind': 'comment',
         'actor': 'Jo', 'text': 'Access confirmed.'},
    ]}
    assert client.get('/api/tickets/t-103').json()['status'] == 'open'
    tickets = client.get('/api/tickets').json()['items']
    assert next(ticket for ticket in tickets if ticket['id'] == 't-103')['status'] == 'open'


def test_timeline_excludes_other_tickets_new_activity(client):
    assert client.post('/api/tickets/t-101/comments',
                       json={'author': 'Musel', 'body': 'Printer only.'}).status_code == 201
    assert client.post('/api/tickets/t-102/status',
                       json={'actor': 'Alex', 'status': 'resolved'}).status_code == 200
    assert read_timeline(client, 't-103') == {'items': []}


def test_existing_ticket_without_activity_has_empty_timeline(client):
    assert read_timeline(client, 't-103') == {'items': []}


def test_unknown_ticket_timeline_returns_not_found(client):
    assert client.get('/api/tickets/missing/timeline').status_code == 404


def test_timeline_with_only_comments(client):
    assert read_timeline(client, 't-102') == {'items': [
        {'id': 'event-2', 'sequence': 2, 'kind': 'comment',
         'actor': 'Sam', 'text': 'The cable was replaced.'},
    ]}


def test_timeline_with_only_status_changes(client):
    assert client.post('/api/tickets/t-103/status',
                       json={'actor': 'Alex', 'status': 'open'}).status_code == 200
    assert read_timeline(client, 't-103') == {'items': [
        {'id': 'event-4', 'sequence': 4, 'kind': 'status',
         'actor': 'Alex', 'text': 'new → open'},
    ]}


def test_repeating_current_status_does_not_create_activity(client):
    assert client.post('/api/tickets/t-103/status',
                       json={'actor': 'Musel', 'status': 'new'}).status_code == 200
    assert read_timeline(client, 't-103') == {'items': []}
    assert client.get('/api/tickets/t-103').json()['status'] == 'new'


@pytest.mark.parametrize(('endpoint', 'payload'), [
    ('comments', {'author': 'Musel', 'body': ' '}),
    ('comments', {'author': ' ', 'body': 'Test'}),
    ('status', {'actor': 'Musel', 'status': 'closed'}),
    ('status', {'actor': ' ', 'status': 'open'}),
])
def test_rejected_write_does_not_create_activity(client, endpoint, payload):
    assert client.post(f'/api/tickets/t-103/{endpoint}', json=payload).status_code == 422
    assert read_timeline(client, 't-103') == {'items': []}
    assert client.get('/api/tickets/t-103').json()['status'] == 'new'


def test_reading_timeline_does_not_change_tickets_or_activity(client):
    tickets_before = client.get('/api/tickets').json()
    history = read_timeline(client, 't-101')
    assert read_timeline(client, 't-101') == history
    assert client.get('/api/tickets').json() == tickets_before
    # Reads must not consume sequence numbers or insert hidden events.
    comment = client.post('/api/tickets/t-101/comments',
                          json={'author': 'Musel', 'body': 'Still investigating.'})
    assert comment.status_code == 201
    assert comment.json()['sequence'] == 4
    assert read_timeline(client, 't-101') == {'items': history['items'] + [
        {'id': 'event-4', 'sequence': 4, 'kind': 'comment',
         'actor': 'Musel', 'text': 'Still investigating.'},
    ]}
