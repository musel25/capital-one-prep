from datetime import datetime, time, timezone

from fastapi import HTTPException


def daily_report(log, on):
    start = datetime.combine(on, time.min, tzinfo=timezone.utc)
    seconds_by_member = {}
    session_count = 0
    for session in log.sessions:
        if session['ended_at'] is None:
            continue
        entered = datetime.fromisoformat(session['started_at'])
        left = datetime.fromisoformat(session['ended_at'])
        # Compare offsets within a UTC day; constructing the next calendar date
        # would overflow when reporting 9999-12-31.
        overlap = min((left - start).total_seconds(), 86400) - max((entered - start).total_seconds(), 0)
        if overlap <= 0:
            continue
        session_count += 1
        member_id = session['member_id']
        seconds_by_member[member_id] = seconds_by_member.get(member_id, 0) + int(overlap)
    items = [{'member_id': member_id, 'minutes': seconds // 60} for member_id, seconds in sorted(seconds_by_member.items())]
    return {
        'date': on.isoformat(),
        'timezone': 'UTC',
        'session_count': session_count,
        'member_count': len(items),
        'total_minutes': sum(item['minutes'] for item in items),
        'items': items,
    }
