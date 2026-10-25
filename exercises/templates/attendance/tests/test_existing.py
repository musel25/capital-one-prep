from fastapi.testclient import TestClient

from app.main import create_app


def test_member_roster_and_log_are_available():
    client = TestClient(create_app())
    assert [member['id'] for member in client.get('/api/members').json()['items']] == ['ada', 'ben', 'cam']
    assert len(client.get('/api/sessions').json()['items']) == 6


def test_member_session_lookup_preserves_log_details():
    client = TestClient(create_app())
    sessions = client.get('/api/members/ben/sessions').json()['items']
    assert [session['id'] for session in sessions] == ['visit-3', 'visit-4']
    assert sessions[0]['started_at'] == '2026-10-30T23:30:00-07:00'
    assert client.get('/api/members/missing/sessions').status_code == 404


def test_open_visits_remain_visible_in_member_log():
    client = TestClient(create_app())
    sessions = client.get('/api/members/cam/sessions').json()['items']
    assert sessions[-1]['ended_at'] is None
    assert client.get('/api/sessions').json()['items'][-1] == sessions[-1]
