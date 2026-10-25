from fastapi import HTTPException

from .roster import MEMBERS


class SessionLog:
    def __init__(self):
        self.sessions = [
            {'id': 'visit-1', 'member_id': 'ada', 'started_at': '2026-10-30T23:30:00Z', 'ended_at': '2026-10-31T00:30:00Z'},
            {'id': 'visit-2', 'member_id': 'ada', 'started_at': '2026-10-31T09:00:00Z', 'ended_at': '2026-10-31T10:15:00Z'},
            {'id': 'visit-3', 'member_id': 'ben', 'started_at': '2026-10-30T23:30:00-07:00', 'ended_at': '2026-10-31T00:30:00-07:00'},
            {'id': 'visit-4', 'member_id': 'ben', 'started_at': '2026-10-31T23:30:00Z', 'ended_at': '2026-11-01T00:30:00Z'},
            {'id': 'visit-5', 'member_id': 'cam', 'started_at': '2026-11-01T00:00:00Z', 'ended_at': '2026-11-01T01:00:00Z'},
            {'id': 'visit-6', 'member_id': 'cam', 'started_at': '2026-10-31T11:00:00Z', 'ended_at': None},
        ]


def member_sessions(log, member_id):
    if member_id not in MEMBERS:
        raise HTTPException(404, 'Member not found')
    return [session for session in log.sessions if session['member_id'] == member_id]
