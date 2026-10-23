"""Instructor-only behavior checks. Never copied into a learner attempt."""
from fastapi.testclient import TestClient


def fresh():
    from app.main import create_app
    client = TestClient(create_app())
    assert client.get('/health').json() == {'status': 'ok'}, 'Application health must remain available.'
    for path in ('/', '/static/app.js', '/static/style.css', '/openapi.json'):
        assert client.get(path).status_code == 200, f'Keep the application interface available: {path}.'
    return client


def transfer(client, **extra):
    body = {'source': 'checking', 'target': 'savings', 'amount_cents': 500}
    body.update(extra)
    return client.post('/api/transfers', json=body)


def d01_bug():
    c = fresh()
    rows = c.get('/api/transactions').json()['items']
    assert [r['id'] for r in rows] == ['t05', 't02', 't03', 't04', 't06', 't01', 't07'], 'Order real instants descending and equal instants by ID ascending.'


def d01_feature():
    c = fresh()
    rows = c.get('/api/transactions?category=groceries&min_cents=1500').json()['items']
    assert [r['id'] for r in rows] == ['t06', 't01', 't07'], 'Combine category and inclusive minimum amount before pagination.'
    assert c.get('/api/transactions?min_cents=-1').status_code == 422
    assert c.get('/api/transactions?category=absent').json()['items'] == []


def d02_bug():
    c = fresh()
    before = c.get('/api/accounts').json()
    assert transfer(c, target='missing').status_code == 404
    assert c.get('/api/accounts').json() == before, 'Rejected transfer must leave every balance untouched.'
    assert transfer(c, amount_cents=999999).status_code == 409
    assert c.get('/api/accounts').json() == before
    assert transfer(c).status_code == 201
    assert c.get('/api/accounts').json()['items'] == [{'id': 'checking', 'balance_cents': 99500}, {'id': 'savings', 'balance_cents': 20500}]


def d02_feature():
    c = fresh()
    assert c.get('/api/accounts/checking/history').status_code == 200, 'Expose history for existing accounts, including empty history.'
    assert c.get('/api/accounts/checking/history').json() == {'items': []}
    response = transfer(c)
    assert response.status_code == 201
    sent = c.get('/api/accounts/checking/history').json()['items']
    received = c.get('/api/accounts/savings/history').json()['items']
    assert len(sent) == len(received) == 1
    assert sent[0]['transfer_id'] == received[0]['transfer_id'] == response.json()['id']
    assert sent[0]['amount_cents'] == -500 and received[0]['amount_cents'] == 500
    transfer(c, target='missing')
    assert c.get('/api/accounts/checking/history').json()['items'] == sent
    assert c.get('/api/accounts/missing/history').status_code == 404


def d03_bug():
    c = fresh()
    r = c.get('/api/cashback?month=2026-10')
    assert r.status_code == 200
    assert r.json()['cashback_cents'] == 213, 'Floor 2% per posted purchase in the month; never round or include refunds/pending.'
    assert c.get('/api/cashback?month=2026-09').json()['cashback_cents'] == 40


def d03_feature():
    c = fresh()
    for cap, expected in [(120, 120), (213, 213), (500, 213), (0, 0)]:
        assert c.get(f'/api/cashback?month=2026-10&cap_cents={cap}').json()['cashback_cents'] == expected, 'Apply a nonnegative monthly cap after summing per-purchase rewards.'
    assert c.get('/api/cashback?month=2026-10&cap_cents=-1').status_code == 422


def d04_bug():
    c = fresh()
    rows = c.get('/api/transactions?category=groceries&page=2&page_size=2').json()['items']
    assert [r['id'] for r in rows] == ['t01', 't07'], 'Filter and sort the complete set before taking the requested page.'
    assert c.get('/api/transactions?page=0').status_code == 422
    assert c.get('/api/transactions?page_size=101').status_code == 422


def d04_feature():
    c = fresh()
    body = c.get('/api/transactions?category=groceries&page=1&page_size=2').json()
    assert {k: body.get(k) for k in ['total', 'page', 'page_size', 'has_next']} == {'total': 4, 'page': 1, 'page_size': 2, 'has_next': True}, 'Metadata uses the filtered total, not page length.'
    final = c.get('/api/transactions?category=groceries&page=2&page_size=2').json()
    assert final['has_next'] is False and final['total'] == 4
    empty = c.get('/api/transactions?category=absent&page=4&page_size=2').json()
    assert empty['items'] == [] and empty['total'] == 0 and empty['has_next'] is False


def d05_bug():
    c = fresh()
    assert c.get('/api/spend?month=2026-10').json()['net_cents'] == 10200, 'Subtract posted refunds; exclude pending transactions.'
    assert c.get('/api/spend?month=2026-09').json()['net_cents'] == 2000
    assert c.get('/api/spend?month=2026-11').json()['net_cents'] == 0


def d05_feature():
    c = fresh()
    r = c.get('/api/spend/categories?month=2026-10')
    assert r.status_code == 200, 'Implement category net-spend summaries.'
    assert r.json() == {'items': [{'category': 'groceries', 'net_cents': 5200}, {'category': 'travel', 'net_cents': 5000}]}, 'Refunds belong to their original purchase category, not adjustments.'
    assert c.get('/api/spend/categories?month=2026-11').json() == {'items': []}


def d06_bug():
    c = fresh()
    r = c.get('/api/accounts')
    assert r.status_code == 200
    assert r.json()['items'] == [{'id': 'checking', 'balance_cents': 100000}, {'id': 'savings', 'balance_cents': 20000}], 'Account API must return the integer-cent fields consumed by the dashboard.'
    transfer(c)
    assert c.get('/api/accounts').json()['items'][0]['balance_cents'] == 99500


def d06_feature():
    c = fresh()
    before = c.get('/api/accounts').json()
    for invalid in [True, False, '500', 2.5, 0, -1]:
        assert transfer(c, amount_cents=invalid).status_code == 422, f'Reject non-integer or nonpositive cents: {invalid!r}.'
    assert transfer(c, source='checking', target='checking').status_code == 422
    assert c.get('/api/accounts').json() == before
    assert transfer(c, amount_cents=1).status_code == 201


def d07_bug():
    c = fresh()
    event = {'event_id': 'evt-1', 'amount_cents': 1234}
    first = c.post('/api/events', json=event)
    again = c.post('/api/events', json=event)
    assert first.status_code == again.status_code == 200
    assert first.json() == again.json(), 'Acknowledgement retries return the same event result.'
    assert c.get('/api/accounts').json()['items'][0]['balance_cents'] == 101234, 'A repeated callback must credit once.'
    assert c.post('/api/events', json={'event_id': 'evt-1', 'amount_cents': 999}).status_code == 409
    assert c.post('/api/events', json={'event_id': 'evt-2', 'amount_cents': 1}).status_code == 200
    assert c.get('/api/accounts').json()['items'][0]['balance_cents'] == 101235


def d07_feature():
    c = fresh()
    body = {'source': 'checking', 'target': 'savings', 'amount_cents': 500}
    first = c.post('/api/transfers', json=body, headers={'Idempotency-Key': 'request-1'})
    again = c.post('/api/transfers', json=body, headers={'Idempotency-Key': 'request-1'})
    assert first.status_code == again.status_code == 201
    assert first.json() == again.json(), 'Same key and same payload returns original result without another transfer.'
    assert c.get('/api/accounts').json()['items'][0]['balance_cents'] == 99500
    conflict = c.post('/api/transfers', json={**body, 'amount_cents': 600}, headers={'Idempotency-Key': 'request-1'})
    assert conflict.status_code == 409
    rejected = {**body, 'target': 'missing'}
    assert c.post('/api/transfers', json=rejected, headers={'Idempotency-Key': 'retry-failed'}).status_code == 404
    assert c.post('/api/transfers', json=body, headers={'Idempotency-Key': 'retry-failed'}).status_code == 201
    assert transfer(c).status_code == 201
    assert c.get('/api/accounts').json()['items'][0]['balance_cents'] == 98500


def d08_bug():
    c = fresh()
    r = c.get('/api/settlements?merchant_id=fern')
    assert r.status_code == 200
    assert [x['id'] for x in r.json()['items']] == ['s01', 's03'], 'Only captured, unsettled charges are eligible.'
    assert c.get('/api/settlements?merchant_id=missing').json()['items'] == []


def d08_feature():
    c = fresh()
    r = c.get('/api/merchants/fern/summary?on=2026-10-30')
    assert r.status_code == 200, 'Expose a merchant daily summary.'
    assert r.json() == {'merchant_id': 'fern', 'date': '2026-10-30', 'count': 2, 'gross_cents': 16000, 'fees_cents': 480, 'net_cents': 15520}
    empty = c.get('/api/merchants/fern/summary?on=2026-10-31').json()
    assert empty['count'] == empty['net_cents'] == 0
    assert c.get('/api/merchants/fern/summary?on=invalid').status_code == 422


def d09_bug():
    c = fresh()
    for at, amount, active, expected in [
        ('2026-10-30T00:00:00Z', 5000, True, True),
        ('2026-11-01T00:00:00Z', 5000, True, False),
        ('2026-10-31T23:59:59Z', 4999, True, False),
        ('2026-10-31T12:00:00Z', 5000, False, False),
        ('2026-10-29T17:00:00-07:00', 5000, True, True),
    ]:
        r = c.post('/api/eligibility', json={'at': at, 'amount_cents': amount, 'active_member': active})
        assert r.status_code == 200
        assert r.json()['eligible'] is expected, 'Window is inclusive start, exclusive end in UTC; minimum spend is inclusive.'


def d09_feature():
    c = fresh()
    for cents, active, expected in [(5001, True, 250), (10000, True, 500), (50000, True, 500), (4999, True, 0), (5000, False, 0)]:
        r = c.post('/api/rewards/quote', json={'at': '2026-10-31T10:00:00Z', 'amount_cents': cents, 'active_member': active})
        assert r.status_code == 200, 'Expose a reward quote using the existing eligibility rules.'
        assert r.json()['reward_cents'] == expected, 'Floor 5% of eligible cents and cap at 500 cents.'
    assert c.post('/api/rewards/quote', json={'at': '2026-11-01T00:00:00Z', 'amount_cents': 6000, 'active_member': True}).json()['reward_cents'] == 0


def d10_bug():
    c = fresh()
    before = c.get('/api/products').json()
    r = c.post('/api/reservations', json={'items': [{'sku': 'dock', 'quantity': 2}, {'sku': 'cable', 'quantity': 99}]})
    assert r.status_code == 409
    assert c.get('/api/products').json() == before, 'Reject the whole reservation without partial stock changes.'
    assert c.get('/api/reservations').json()['items'] == []
    assert c.post('/api/reservations', json={'items': [{'sku': 'missing', 'quantity': 1}]}).status_code == 404
    assert c.post('/api/reservations', json={'items': [{'sku': 'dock', 'quantity': 3}, {'sku': 'dock', 'quantity': 3}]}).status_code == 409
    assert c.get('/api/products').json() == before
    assert c.post('/api/reservations', json={'items': [{'sku': 'dock', 'quantity': 2}, {'sku': 'dock', 'quantity': 1}]}).status_code == 201
    assert c.get('/api/products').json()['items'][0]['available'] == 2


def d10_feature():
    c = fresh()
    before = c.get('/api/products').json()
    created = c.post('/api/reservations', json={'items': [{'sku': 'dock', 'quantity': 2}, {'sku': 'cable', 'quantity': 3}]})
    assert created.status_code == 201
    rid = created.json()['id']
    for _ in range(2):
        canceled = c.post(f'/api/reservations/{rid}/cancel')
        assert canceled.status_code == 200, 'Cancellation restores stock exactly once and can be retried.'
        assert canceled.json()['status'] == 'canceled'
        assert c.get('/api/products').json() == before
    assert c.post('/api/reservations/unknown/cancel').status_code == 404
    assert c.get('/api/reservations').json()['items'][0]['status'] == 'canceled'


CHECKS = {name.replace('_', '-'): value for name, value in list(globals().items()) if name.startswith('d') and callable(value)}
