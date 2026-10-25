"""Instructor-only starter substitutions and HTTP checks for middle scenarios."""

from fastapi.testclient import TestClient


PATCHES = {
    'd04-feature': ('app/scheduling.py', 'availability', '''
def availability(calendar, provider_id, on, duration_minutes):
    raise HTTPException(501, 'Availability is not implemented')
'''),
    'd05-bug': ('app/billing.py', 'bill', '''
def bill(feed, workspace_id, month):
    feed.require_workspace(workspace_id)
    rows = [row for row in feed.events if row['workspace_id'] == workspace_id
            and row['month'] == month and row['status'] == 'accepted']
    units = sum(row['units'] for row in rows)
    return invoice(workspace_id, month, len(rows), units)
'''),
    'd05-feature': ('app/summaries.py', 'employee_summary', '''
def employee_summary(ledger, employee_id, month):
    raise HTTPException(501, 'Employee summary is not implemented')
'''),
    'd06-bug': ('app/representation.py', 'reading', '''
def reading(row):
    return {'id': row['id'], 'service_id': row['service_id'],
            'duration_ms': row['duration_us'], 'status': row['status']}
'''),
    'd06-feature': ('app/importing.py', 'import_contacts', '''
def import_contacts(directory, request):
    raise HTTPException(501, 'Batch import is not implemented')
'''),
}


def client():
    from app.main import create_app
    result = TestClient(create_app())
    assert result.get('/health').json() == {'status': 'ok'}
    for path in ('/', '/static/app.js', '/static/style.css', '/openapi.json'):
        assert result.get(path).status_code == 200, f'Application interface unavailable: {path}'
    return result


def d04_feature():
    c = client()
    path = '/api/availability?provider_id=aria&on=2026-10-26'
    before = c.get('/api/bookings').json()
    r = c.get(path)
    assert r.status_code == 200, 'Availability must return candidate appointments.'
    assert r.json() == {
        'provider_id': 'aria', 'date': '2026-10-26', 'duration_minutes': 30,
        'items': [{'start': '09:00', 'end': '09:30'}, {'start': '09:30', 'end': '10:00'},
                  {'start': '10:30', 'end': '11:00'}, {'start': '11:00', 'end': '11:30'},
                  {'start': '11:30', 'end': '12:00'}],
    }, 'Respect conflicts, canceled visits, touching endpoints, and closing time.'
    assert c.get(path + '&duration_minutes=60').json()['items'] == [
        {'start': '09:00', 'end': '10:00'}, {'start': '10:30', 'end': '11:30'},
        {'start': '11:00', 'end': '12:00'},
    ]
    assert c.get('/api/availability?provider_id=ben&on=2026-10-26').json()['items'] == [
        {'start': '10:30', 'end': '11:00'},
    ]
    assert c.get('/api/availability?provider_id=aria&on=2026-10-27').json()['items'] == [
        {'start': '13:00', 'end': '13:30'}, {'start': '13:30', 'end': '14:00'},
    ]
    assert c.get('/api/availability?provider_id=aria&on=2026-10-28').json()['items'] == []
    assert c.get('/api/availability?provider_id=missing&on=2026-10-26').status_code == 404
    for suffix in ('&duration_minutes=0', '&duration_minutes=45', '&duration_minutes=90'):
        assert c.get(path + suffix).status_code == 422
    assert c.get('/api/availability?provider_id=aria&on=2026-02-30').status_code == 422
    assert c.get('/api/bookings').json() == before, 'Availability is a read-only preview.'
    body = {'provider_id': 'aria', 'on': '2026-10-26', 'start': '11:30', 'duration_minutes': 30}
    assert c.post('/api/bookings', json=body).status_code == 201
    after = c.get('/api/bookings').json()
    assert c.post('/api/bookings', json=body).status_code == 409
    assert c.get('/api/bookings').json() == after
    assert c.get(path).json()['items'][-1] == {'start': '11:00', 'end': '11:30'}
    assert c.get(path + '&duration_minutes=60').json()['items'] == [
        {'start': '09:00', 'end': '10:00'}, {'start': '10:30', 'end': '11:30'},
    ]


def d05_bug():
    c = client()
    before = c.get('/api/events').json()
    path = '/api/workspaces/north/bill?month=2026-10'
    expected = {'workspace_id': 'north', 'month': '2026-10', 'billable_samples': 3,
                'units': 147, 'charge_cents': 441}
    assert c.get(path).json() == expected, 'Repeated deliveries must not increase metered usage.'
    assert c.get('/api/workspaces/south/bill?month=2026-10').json()['units'] == 10
    assert c.get('/api/workspaces/north/bill?month=2026-09').json()['units'] == 25
    assert c.get('/api/workspaces/north/bill?month=2026-11').json() == {
        'workspace_id': 'north', 'month': '2026-11', 'billable_samples': 0,
        'units': 0, 'charge_cents': 0,
    }
    assert c.get('/api/events').json() == before, 'Invoices must preserve raw delivery history.'
    repeated = {'event_id': 'delivery-9', 'workspace_id': 'north', 'month': '2026-10',
                'meter_id': 'api', 'sample_id': 's2', 'units': 40, 'status': 'accepted'}
    assert c.post('/api/events', json=repeated).status_code == 201
    assert c.get(path).json() == expected
    assert len(c.get('/api/events').json()['items']) == len(before['items']) + 1
    assert c.post('/api/events', json={**repeated, 'event_id': 'delivery-10', 'sample_id': 'new', 'units': 1}).status_code == 201
    assert c.get(path).json() == {**expected, 'billable_samples': 4, 'units': 148, 'charge_cents': 444}
    after = c.get('/api/events').json()
    assert c.post('/api/events', json=repeated).status_code == 409
    assert c.post('/api/events', json={**repeated, 'event_id': 'bad', 'workspace_id': 'missing'}).status_code == 404
    for invalid in (True, '1', 0, -1, 1.5):
        assert c.post('/api/events', json={**repeated, 'event_id': 'bad', 'units': invalid}).status_code == 422
    assert c.get('/api/events').json() == after
    assert c.get('/api/workspaces/missing/bill?month=2026-10').status_code == 404
    for month in ('2026-13', '2026-00', '2026-1', '0000-01', 'bad'):
        assert c.get('/api/workspaces/north/bill', params={'month': month}).status_code == 422
        assert c.post('/api/events', json={**repeated, 'event_id': 'bad-month', 'month': month}).status_code == 422


def d05_feature():
    c = client()
    before = c.get('/api/expenses').json()
    path = '/api/employees/ada/summary?month=2026-10'
    r = c.get(path)
    assert r.status_code == 200, 'Expose an employee monthly summary.'
    assert r.json() == {
        'employee_id': 'ada', 'month': '2026-10', 'approved_cents': 5100, 'pending_cents': 1200,
        'items': [{'category': 'meals', 'approved_cents': 900, 'pending_cents': 1200},
                  {'category': 'travel', 'approved_cents': 4200, 'pending_cents': 0}],
    }, 'Keep approved/pending totals distinct and exclude rejected-only categories.'
    for employee, month in [('bo', '2026-10'), ('ada', '2026-11')]:
        assert c.get(f'/api/employees/{employee}/summary?month={month}').json() == {
            'employee_id': employee, 'month': month, 'approved_cents': 0, 'pending_cents': 0, 'items': [],
        }
    assert c.get('/api/employees/ada/summary?month=2026-09').json()['approved_cents'] == 2000
    assert c.get('/api/employees/cam/summary?month=2026-10').json()['approved_cents'] == 500
    assert c.get('/api/expenses').json() == before
    claim = {'employee_id': 'ada', 'incurred_on': '2026-10-31', 'category': 'supplies',
             'amount_cents': 1, 'description': 'Replacement label'}
    assert c.post('/api/expenses', json=claim).status_code == 201
    result = c.get(path).json()
    assert result['approved_cents'] == 5100 and result['pending_cents'] == 1201
    assert result['items'][1] == {'category': 'supplies', 'approved_cents': 0, 'pending_cents': 1}
    after = c.get('/api/expenses').json()
    assert c.post('/api/expenses', json={**claim, 'employee_id': 'missing'}).status_code == 404
    assert c.post('/api/expenses', json={**claim, 'amount_cents': True}).status_code == 422
    assert c.get('/api/expenses').json() == after
    assert c.get('/api/employees/missing/summary?month=2026-10').status_code == 404
    for month in ('2026-13', '2026-00', '2026-1', '0000-01', 'bad'):
        assert c.get('/api/employees/ada/summary', params={'month': month}).status_code == 422


def d06_bug():
    c = client()
    path = '/api/services/atlas/readings'
    rows = c.get(path).json()['items']
    assert rows == [
        {'id': 'r1', 'service_id': 'atlas', 'duration_ms': 125, 'status': 'ok'},
        {'id': 'r2', 'service_id': 'atlas', 'duration_ms': 1.5, 'status': 'ok'},
        {'id': 'r3', 'service_id': 'atlas', 'duration_ms': 250, 'status': 'error'},
    ], 'Public readings must use milliseconds and preserve sub-millisecond precision.'
    assert c.get('/api/services/beacon/readings').json()['items'][0]['duration_ms'] == 0
    assert c.get('/api/services/atlas/summary').json() == {
        'service_id': 'atlas', 'count': 3, 'error_count': 1, 'slow_count': 1,
    }
    for micros, millis in [(0, 0), (1, 0.001), (199999, 199.999), (200000, 200)]:
        r = c.post('/api/readings', json={'service_id': 'atlas', 'duration_us': micros, 'status': 'ok'})
        assert r.status_code == 201
        assert r.json()['duration_ms'] == millis
        assert 'duration_us' not in r.json()
        assert c.get(path).json()['items'][-1] == r.json()
    assert c.get('/api/services/atlas/summary').json() == {
        'service_id': 'atlas', 'count': 7, 'error_count': 1, 'slow_count': 2,
    }
    before = c.get(path).json()
    for invalid in (True, '1', -1, 1.5):
        assert c.post('/api/readings', json={'service_id': 'atlas', 'duration_us': invalid, 'status': 'ok'}).status_code == 422
    assert c.post('/api/readings', json={'service_id': 'missing', 'duration_us': 1, 'status': 'ok'}).status_code == 404
    assert c.get('/api/services/missing/readings').status_code == 404
    assert c.get(path).json() == before, 'Rejected samples must not change the monitor.'


def d06_feature():
    c = client()
    before = c.get('/api/contacts').json()
    valid = {'name': '  Rae Lin  ', 'email': ' RAE@example.com ', 'team': 'events'}
    second = {'name': 'Mo Tan', 'email': 'mo@example.com', 'team': 'support'}
    r = c.post('/api/imports', json={'contacts': [valid, second]})
    assert r.status_code == 201, 'Batch import must accept validated contact rows.'
    assert r.json() == {'items': [
        {'id': 'c3', 'name': 'Rae Lin', 'email': 'rae@example.com', 'team': 'events'},
        {'id': 'c4', 'name': 'Mo Tan', 'email': 'mo@example.com', 'team': 'support'},
    ]}
    assert c.get('/api/contacts').json()['items'] == before['items'] + r.json()['items']
    after = c.get('/api/contacts').json()
    new = {'name': 'Lee', 'email': 'lee@example.com', 'team': 'events'}
    for rows in ([new, {**new, 'email': ' LEE@example.com '}], [new, valid], [new, {**new, 'email': 'KAI@example.com'}]):
        assert c.post('/api/imports', json={'contacts': rows}).status_code == 409
        assert c.get('/api/contacts').json() == after, 'Duplicate batches must leave no partial contacts.'
    for bad in ({**new, 'name': '  '}, {**new, 'email': 'bad'}, {**new, 'email': 'a@@example.com'},
                {**new, 'email': 'a b@example.com'}, {**new, 'email': 'a@localhost'},
                {**new, 'team': 'unknown'}, {**new, 'name': 12}):
        assert c.post('/api/imports', json={'contacts': [new, bad]}).status_code == 422
        assert c.get('/api/contacts').json() == after
    assert c.post('/api/imports', json={'contacts': []}).status_code == 422
    assert c.post('/api/imports', json={'contacts': [{**new, 'email': f'p{i}@example.com'} for i in range(51)]}).status_code == 422
    assert c.get('/api/contacts').json() == after
    last = c.post('/api/imports', json={'contacts': [new]})
    assert last.status_code == 201 and last.json()['items'][0]['id'] == 'c5', 'Rejected batches must consume no IDs.'
    batch = [{**new, 'email': f'p{i}@example.com'} for i in range(50)]
    assert c.post('/api/imports', json={'contacts': batch}).status_code == 201
    assert len(c.get('/api/contacts').json()['items']) == 55
    assert c.get('/api/contacts/missing').status_code == 404


CHECKS = {
    'd04-feature': d04_feature,
    'd05-bug': d05_bug,
    'd05-feature': d05_feature,
    'd06-bug': d06_bug,
    'd06-feature': d06_feature,
}
