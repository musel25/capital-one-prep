from fastapi import HTTPException
from .clock import minutes, slot


def conflicts(calendar, provider_id, day, start, end):
    return any(
        booking['provider_id'] == provider_id and booking['date'] == day
        and booking['status'] == 'confirmed'
        and start < minutes(booking['end']) and end > minutes(booking['start'])
        for booking in calendar.bookings
    )


def book(calendar, request):
    calendar.require_provider(request.provider_id)
    day = request.on.isoformat()
    hours = calendar.hours.get((request.provider_id, day))
    start = minutes(request.start)
    end = start + request.duration_minutes
    if hours is None or start < hours[0] or end > hours[1] or (start - hours[0]) % 30:
        raise HTTPException(409, 'Appointment outside available hours')
    if conflicts(calendar, request.provider_id, day, start, end):
        raise HTTPException(409, 'Appointment conflicts with an existing booking')
    row = {'id': f'b{len(calendar.bookings) + 1}', 'provider_id': request.provider_id,
           'date': day, **slot(start, end), 'status': 'confirmed'}
    calendar.bookings.append(row)
    return row


def availability(calendar, provider_id, on, duration_minutes):
    calendar.require_provider(provider_id)
    day = on.isoformat()
    hours = calendar.hours.get((provider_id, day))
    items = []
    if hours is not None:
        opening, closing = hours
        for start in range(opening, closing - duration_minutes + 1, 30):
            end = start + duration_minutes
            if not conflicts(calendar, provider_id, day, start, end):
                items.append(slot(start, end))
    return {'provider_id': provider_id, 'date': day,
            'duration_minutes': duration_minutes, 'items': items}
