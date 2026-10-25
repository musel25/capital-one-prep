"""Instructor-only seeds and HTTP checks for the final unfamiliar applications."""

PATCHES = {
    'd07-bug': ('app/delivery.py', 'receive', '''
def receive(inbox, event):
    payload = event.model_dump()
    previous = inbox.receipts.get(event.event_id)
    if previous is not None and previous['payload'] != payload:
        raise HTTPException(409, 'Event ID belongs to a different delivery')
    parcel = inbox.parcels.get(event.parcel_id)
    if parcel is None:
        raise HTTPException(404, 'Parcel not found')
    notification = notify(inbox, parcel, event.status)
    result = {'event_id': event.event_id, 'accepted': True, 'notification_id': notification['id']}
    inbox.receipts[event.event_id] = {'payload': payload, 'result': result}
    return result
'''),
    'd07-feature': ('app/submission.py', 'submit', '''
def submit(registry, request, key):
    if key is not None and (not key.strip() or len(key) > 64):
        raise HTTPException(422, 'Idempotency-Key must contain 1 to 64 characters and not be blank')
    return enqueue(registry, request)
'''),
    'd08-feature': ('app/reporting.py', 'daily_report', '''
def daily_report(log, on):
    raise HTTPException(501, 'Daily attendance reporting is not implemented')
'''),
    'd09-feature': ('app/pricing.py', 'quote', '''
def quote(accounts, subscription_id, request):
    raise HTTPException(501, 'Upgrade quotes are not implemented')
'''),
    'd10-feature': ('app/returns.py', 'accept_return', '''
def accept_return(library, loan_id):
    raise HTTPException(501, 'Equipment returns are not implemented')
'''),
}


def _assert_interface(client):
    assert client.get('/health').json() == {'status': 'ok'}
    for path in ('/', '/static/app.js', '/static/style.css', '/openapi.json'):
        assert client.get(path).status_code == 200, f'Keep the public interface available: {path}'


def d07_bug():
    from fastapi.testclient import TestClient
    from app.main import create_app

    client = TestClient(create_app())
    _assert_interface(client)
    parcels = client.get('/api/parcels').json()
    event = {'event_id': 'delivery-1', 'parcel_id': 'parcel-101', 'status': 'arrived'}
    first = client.post('/api/deliveries', json=event)
    retry = client.post('/api/deliveries', json=event)
    assert first.status_code == retry.status_code == 200
    assert first.json() == retry.json(), 'A retried delivery returns its original acknowledgement.'
    notifications = client.get('/api/notifications').json()
    assert len(notifications['items']) == 1, 'A delivery retry must not notify the resident twice.'
    assert notifications['items'][0]['id'] == first.json()['notification_id']
    receipts = client.get('/api/deliveries').json()
    assert receipts == {'items': [first.json()]}
    for changed in ({'status': 'delayed'}, {'parcel_id': 'parcel-102'}, {'parcel_id': 'unknown'}):
        assert client.post('/api/deliveries', json={**event, **changed}).status_code == 409
        assert client.get('/api/notifications').json() == notifications
        assert client.get('/api/deliveries').json() == receipts
    rejected = {**event, 'event_id': 'retry-after-rejection', 'parcel_id': 'unknown'}
    assert client.post('/api/deliveries', json=rejected).status_code == 404
    assert client.get('/api/notifications').json() == notifications
    assert client.get('/api/deliveries').json() == receipts
    corrected = {**rejected, 'parcel_id': 'parcel-102', 'status': 'delayed'}
    assert client.post('/api/deliveries', json=corrected).status_code == 200
    assert client.post('/api/deliveries', json={**event, 'event_id': 'delivery-2'}).status_code == 200
    assert len(client.get('/api/notifications').json()['items']) == 3
    assert len(client.get('/api/deliveries').json()['items']) == 3
    assert client.get('/api/parcels').json() == parcels
    for changed in ({'event_id': ''}, {'event_id': 'x' * 81}, {'status': 'lost'}):
        assert client.post('/api/deliveries', json={**event, **changed}).status_code == 422
    assert len(client.get('/api/notifications').json()['items']) == 3
    boundary = {**event, 'event_id': 'x' * 80}
    assert client.post('/api/deliveries', json=boundary).status_code == 200
    assert client.post('/api/deliveries', json=boundary).status_code == 200
    assert len(client.get('/api/notifications').json()['items']) == 4


def d07_feature():
    from fastapi.testclient import TestClient
    from app.main import create_app

    client = TestClient(create_app())
    _assert_interface(client)
    datasets = client.get('/api/datasets').json()
    payload = {'dataset_id': 'visits', 'format': 'csv'}
    headers = {'Idempotency-Key': 'request-1'}
    first = client.post('/api/jobs', json=payload, headers=headers)
    retry = client.post('/api/jobs', json=payload, headers=headers)
    assert first.status_code == retry.status_code == 201
    assert first.json() == retry.json(), 'A repeated export key and payload must return the original job.'
    assert client.get('/api/jobs').json() == {'items': [first.json()]}
    assert client.get('/api/jobs/' + first.json()['id']).json() == first.json()
    for changed in ({'dataset_id': 'tickets'}, {'format': 'json'}):
        assert client.post('/api/jobs', json={**payload, **changed}, headers=headers).status_code == 409
    assert client.get('/api/jobs').json() == {'items': [first.json()]}
    failed_headers = {'Idempotency-Key': 'initially-invalid'}
    assert client.post('/api/jobs', json={**payload, 'dataset_id': 'missing'}, headers=failed_headers).status_code == 404
    assert client.get('/api/jobs').json() == {'items': [first.json()]}
    assert client.post('/api/jobs', json=payload, headers=failed_headers).status_code == 201
    malformed_headers = {'Idempotency-Key': 'initially-malformed'}
    assert client.post('/api/jobs', json={**payload, 'format': 'xml'}, headers=malformed_headers).status_code == 422
    assert client.post('/api/jobs', json=payload, headers=malformed_headers).status_code == 201
    before = client.get('/api/jobs').json()
    for key in ('', '   ', 'x' * 65):
        assert client.post('/api/jobs', json=payload, headers={'Idempotency-Key': key}).status_code == 422
    assert client.get('/api/jobs').json() == before
    for key in ('x' * 64, 'X' * 64, ' request-1 '):
        response = client.post('/api/jobs', json=payload, headers={'Idempotency-Key': key})
        assert response.status_code == 201
        assert client.post('/api/jobs', json=payload, headers={'Idempotency-Key': key}).json() == response.json()
    unkeyed_a = client.post('/api/jobs', json=payload)
    unkeyed_b = client.post('/api/jobs', json=payload)
    assert unkeyed_a.status_code == unkeyed_b.status_code == 201
    assert unkeyed_a.json()['id'] != unkeyed_b.json()['id']
    assert len(client.get('/api/jobs').json()['items']) == 8
    assert client.get('/api/datasets').json() == datasets


def d08_feature():
    from fastapi.testclient import TestClient
    from app.main import create_app

    client = TestClient(create_app())
    _assert_interface(client)
    paths = ['/api/sessions', '/api/members', '/api/members/ada/sessions']
    before = [client.get(path).json() for path in paths]
    response = client.get('/api/attendance?on=2026-10-31')
    assert response.status_code == 200, 'Provide the requested daily attendance report.'
    assert response.json() == {
        'date': '2026-10-31', 'timezone': 'UTC', 'session_count': 4,
        'member_count': 2, 'total_minutes': 195,
        'items': [{'member_id': 'ada', 'minutes': 105}, {'member_id': 'ben', 'minutes': 90}],
    }, 'Count completed overlaps within the UTC day, grouped by member.'
    assert client.get('/api/attendance?on=2026-10-30').json() == {
        'date': '2026-10-30', 'timezone': 'UTC', 'session_count': 1,
        'member_count': 1, 'total_minutes': 30, 'items': [{'member_id': 'ada', 'minutes': 30}],
    }, 'Timestamp text with another offset must not move attendance into the wrong UTC day.'
    assert client.get('/api/attendance?on=2026-11-01').json() == {
        'date': '2026-11-01', 'timezone': 'UTC', 'session_count': 2,
        'member_count': 2, 'total_minutes': 90,
        'items': [{'member_id': 'ben', 'minutes': 30}, {'member_id': 'cam', 'minutes': 60}],
    }
    for day in ('2026-10-29', '2026-11-02', '0001-01-01', '9999-12-31'):
        response = client.get(f'/api/attendance?on={day}')
        assert response.status_code == 200, 'Every supported calendar day can be reported.'
        assert response.json() == {
            'date': day, 'timezone': 'UTC', 'session_count': 0,
            'member_count': 0, 'total_minutes': 0, 'items': [],
        }
    for suffix in ('', '?on=nope', '?on=2026-02-30'):
        assert client.get('/api/attendance' + suffix).status_code == 422
    assert [client.get(path).json() for path in paths] == before, 'Reports must not rewrite the session log.'


def d09_feature():
    from fastapi.testclient import TestClient
    from app.main import create_app

    client = TestClient(create_app())
    _assert_interface(client)
    before = [client.get(path).json() for path in ('/api/plans', '/api/subscriptions')]
    url = '/api/subscriptions/sub-100/quote'
    payload = {'target_plan': 'plus', 'effective_on': '2026-10-16'}
    response = client.post(url, json=payload)
    assert response.status_code == 200, 'Provide a read-only subscription upgrade quote.'
    expected = {
        'subscription_id': 'sub-100', 'target_plan': 'plus', 'effective_on': '2026-10-16',
        'cycle_days': 31, 'remaining_days': 16, 'uncapped_cents': 980, 'charge_cents': 980,
    }
    assert response.json() == expected, 'Prorate the price difference over exact calendar days, flooring once.'
    for cap, charge in ((None, 980), (0, 0), (500, 500), (980, 980), (1000, 980)):
        result = client.post(url, json={**payload, 'cap_cents': cap})
        assert result.status_code == 200
        assert result.json() == {**expected, 'charge_cents': charge}
    for day, remaining, charge in (('2026-10-01', 31, 1900), ('2026-10-31', 1, 61), ('2026-11-01', 0, 0)):
        result = client.post(url, json={**payload, 'effective_on': day})
        assert result.status_code == 200
        assert result.json() == {**expected, 'effective_on': day, 'remaining_days': remaining, 'uncapped_cents': charge, 'charge_cents': charge}
    assert client.post(url, json={**payload, 'target_plan': 'basic'}).json()['charge_cents'] == 0
    second = client.post('/api/subscriptions/sub-200/quote', json={'target_plan': 'team', 'effective_on': '2026-11-01'})
    assert second.status_code == 200
    assert second.json()['remaining_days'] == 14 and second.json()['charge_cents'] == 858
    for changed in ({'effective_on': '2026-09-30'}, {'effective_on': '2026-11-02'}, {'effective_on': 'invalid'}):
        assert client.post(url, json={**payload, **changed}).status_code == 422
    for invalid in (True, False, '50', 1.5, -1):
        assert client.post(url, json={**payload, 'cap_cents': invalid}).status_code == 422
    assert client.post(url, json={**payload, 'target_plan': 'missing'}).status_code == 404
    assert client.post('/api/subscriptions/missing/quote', json=payload).status_code == 404
    assert client.post('/api/subscriptions/sub-300/quote', json=payload).status_code == 409
    assert client.post('/api/subscriptions/sub-200/quote', json={**payload, 'target_plan': 'basic'}).status_code == 409
    assert [client.get(path).json() for path in ('/api/plans', '/api/subscriptions')] == before


def d10_feature():
    from fastapi.testclient import TestClient
    from app.main import create_app

    client = TestClient(create_app())
    _assert_interface(client)
    initial = client.get('/api/equipment').json()
    original_loan = client.get('/api/loans/loan-1').json()
    other_loans = [client.get(f'/api/loans/loan-{number}').json() for number in (2, 3, 4)]
    response = client.post('/api/loans/loan-1/return')
    assert response.status_code == 200, 'Accept a full equipment-loan return.'
    assert response.json() == {**original_loan, 'status': 'returned'}
    after = client.get('/api/equipment').json()
    assert after['items'][0] == {**initial['items'][0], 'available': 2}
    assert after['items'][1] == initial['items'][1]
    assert client.get('/api/loans/loan-1').json() == response.json()
    assert [client.get(f'/api/loans/loan-{number}').json() for number in (2, 3, 4)] == other_loans
    assert client.post('/api/loans/loan-1/return').json() == response.json()
    assert client.get('/api/equipment').json() == after, 'Retrying a return must not add inventory again.'
    loan_before = client.get('/api/loans').json()
    assert client.post('/api/loans/missing/return').status_code == 404
    assert client.get('/api/equipment').json() == after
    assert client.get('/api/loans').json() == loan_before
    already_returned = client.post('/api/loans/loan-4/return')
    assert already_returned.status_code == 200 and already_returned.json() == other_loans[-1]
    assert client.get('/api/equipment').json() == after
    assert client.post('/api/loans/loan-2/return').status_code == 200
    assert client.get('/api/equipment').json()['items'][0]['available'] == 3
    request = {'equipment_id': 'camera', 'borrower': 'Eli', 'quantity': 2}
    new_loan = client.post('/api/loans', json=request)
    assert new_loan.status_code == 201
    assert client.get('/api/equipment').json()['items'][0]['available'] == 1
    assert client.post('/api/loans/loan-1/return').json() == response.json()
    assert client.get('/api/equipment').json()['items'][0]['available'] == 1
    returned = client.post(f"/api/loans/{new_loan.json()['id']}/return")
    assert returned.status_code == 200 and returned.json()['quantity'] == 2
    assert client.get('/api/equipment').json()['items'][0]['available'] == 3
    assert client.post(f"/api/loans/{new_loan.json()['id']}/return").json() == returned.json()
    assert client.get('/api/equipment').json()['items'][0]['available'] == 3
    assert client.get('/api/equipment').json()['items'][1] == initial['items'][1]


CHECKS = {
    'd07-bug': d07_bug,
    'd07-feature': d07_feature,
    'd08-feature': d08_feature,
    'd09-feature': d09_feature,
    'd10-feature': d10_feature,
}
