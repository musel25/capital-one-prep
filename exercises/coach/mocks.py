"""Instructor-only contracts and controlled changes for larger mock apps."""
from fastapi.testclient import TestClient


def fresh():
    from app.main import create_app
    c = TestClient(create_app())
    for path in ('/', '/health', '/openapi.json', '/static/app.js', '/static/style.css'):
        assert c.get(path).status_code == 200, f'Keep {path} available.'
    return c


def support_bug():
    c = fresh()
    events = c.get('/api/events').json()
    support = c.get('/api/queues', params={'team': 'support', 'status': 'open'}).json()
    assert [t['id'] for t in support['items']] == ['t-2']
    platform = c.get('/api/queues', params={'team': 'platform', 'status': 'open', 'page_size': 1}).json()
    assert platform['total'] == 2 and platform['has_next'] is True, 'Queue totals and pages must describe the requested team/status, even after a different query.'
    assert [t['id'] for t in platform['items']] == ['t-1']
    assert [t['id'] for t in c.get('/api/queues?team=platform&status=open&page_size=1&page=2').json()['items']] == ['t-4']
    assert c.get('/api/queues?team=platform&status=open&page=9').json() == {'items': [], 'total': 2, 'has_next': False}
    assert [t['id'] for t in c.get('/api/queues?team=platform&status=resolved').json()['items']] == ['t-3']
    assert c.get('/api/events').json() == events, 'Reading queues must not create events.'
    assert c.post('/api/tickets/t-1/status', json={'status': 'resolved', 'actor': 'learner'}).status_code == 200
    assert c.get('/api/queues?team=platform&status=open').json()['total'] == 1
    assert c.get('/api/queues?team=platform&status=resolved').json()['total'] == 2
    assert c.get('/api/queues?team=unknown').status_code == 422
    assert c.get('/api/queues?page=0').status_code == 422
    c = fresh()
    c.get('/api/queues?team=platform&status=open')
    assert c.get('/api/queues?team=support&status=open').json()['total'] == 1, 'Filter isolation must work in either query order.'


def support_feature():
    c = fresh()
    initial = c.get('/api/tickets').json(), c.get('/api/events').json()
    bad = [(['t-1', 'missing'], 'a-1', 404), (['t-1', 't-2'], 'a-1', 409),
           (['t-1', 't-3'], 'a-1', 409), (['t-1'], 'a-3', 409), (['t-1'], 'missing', 404)]
    for ids, agent, status in bad:
        response = c.post('/api/assignments', json={'ticket_ids': ids, 'agent_id': agent, 'actor': 'learner'})
        assert response.status_code == status, 'Reject invalid batches with the documented status.'
        assert (c.get('/api/tickets').json(), c.get('/api/events').json()) == initial, 'A rejected batch must preserve every ticket and the entire event history.'
    c.get('/api/queues?team=platform&status=open')
    response = c.post('/api/assignments', json={'ticket_ids': ['t-4', 't-1', 't-4'], 'agent_id': 'a-1', 'actor': 'learner'})
    assert response.status_code == 200, 'Implement bulk assignment for valid open tickets.'
    assert response.json() == {'updated': ['t-4', 't-1']}
    assert all(t['assignee'] == 'a-1' for t in c.get('/api/queues?team=platform&status=open').json()['items'])
    events = c.get('/api/events').json()['items']
    assert [(e['ticket_id'], e['kind'], e['actor']) for e in events] == [('t-4', 'assignment', 'learner'), ('t-1', 'assignment', 'learner')]
    assert [e['sequence'] for e in events] == [1, 2]
    assert [e['detail'] for e in events] == [{'previous': None, 'current': 'a-1'}] * 2, 'Assignment history must describe the actual previous and current assignee.'
    assert c.post('/api/assignments', json={'ticket_ids': ['t-1'], 'agent_id': 'a-1', 'actor': 'learner'}).json() == {'updated': []}
    assert c.get('/api/events').json()['items'] == events
    assert c.post('/api/assignments', json={'ticket_ids': [], 'agent_id': 'a-1', 'actor': 'learner'}).status_code == 422
    assert c.post('/api/assignments', json={'ticket_ids': ['t-1'], 'agent_id': 'a-1', 'actor': ' '}).status_code == 422


def dispatch_bug():
    c = fresh()
    before = c.get('/api/orders').json(), c.get('/api/inventory').json(), c.get('/api/events').json()
    cases = [([250, 250], 'standard', False, 2, 280), ([500, 501], 'standard', False, 3, 320),
             ([1, 1000], 'express', True, 3, 725), ([500], 'standard', False, 1, 140)]
    for weights, service, signature, units, total in cases:
        response = c.post('/api/quotes', json={'weights_grams': weights, 'service': service, 'signature': signature})
        assert response.status_code == 200
        assert response.json()['total_cents'] == total, 'Round each separately labeled parcel up to 500 grams; apply its base charge separately.'
        assert response.json() == {'parcels': len(weights), 'billable_units': units,
                                   'transport_cents': total - (100 if signature else 0),
                                   'signature_cents': 100 if signature else 0,
                                   'total_cents': total}, 'The quote breakdown must explain the total correctly.'
    assert (c.get('/api/orders').json(), c.get('/api/inventory').json(), c.get('/api/events').json()) == before, 'Quotes must be read-only.'
    for weights in ([], [0], [True], [501.5], [20001]):
        assert c.post('/api/quotes', json={'weights_grams': weights, 'service': 'standard'}).status_code == 422
    shipped = c.post('/api/shipments', json={'order_id': 'o-1', 'service': 'standard', 'signature': False})
    assert shipped.status_code == 201 and shipped.json()['total_cents'] == 280, 'Shipment totals must use the corrected per-parcel quote rules.'


def dispatch_feature():
    c = fresh()
    baseline_events = c.get('/api/events').json()
    initial_orders = c.get('/api/orders').json()
    initial_stock = c.get('/api/inventory').json()
    assert c.post('/api/orders/missing/cancel').status_code == 404
    assert c.post('/api/orders/o-3/cancel').status_code == 409
    assert c.get('/api/events').json() == baseline_events
    assert c.get('/api/orders').json() == initial_orders
    assert c.get('/api/inventory').json() == initial_stock
    response = c.post('/api/orders/o-1/cancel')
    assert response.status_code == 200 and response.json()['status'] == 'cancelled', 'Reserved orders need a cancellation operation.'
    after = c.get('/api/inventory').json()
    assert {r['sku']: r['available'] for r in after['items']} == {'cable': 7, 'dock': 4}
    assert c.get('/api/orders/o-2').json()['status'] == 'reserved'
    events = c.get('/api/events').json()
    assert len(events['items']) == 1 and events['items'][0]['kind'] == 'cancelled'
    assert events['items'][0] == {'sequence': 1, 'order_id': 'o-1', 'kind': 'cancelled',
                                  'detail': {'items': [{'sku': 'cable', 'quantity': 2}]}}, 'Cancellation history must retain the released order items.'
    assert c.post('/api/orders/o-1/cancel').json() == response.json()
    assert c.get('/api/inventory').json() == after and c.get('/api/events').json() == events, 'Repeated cancellation must not restore stock or append events twice.'
    orders_before_rejection = c.get('/api/orders').json()
    assert c.get('/api/shipments/s-1').status_code == 404
    assert c.post('/api/shipments', json={'order_id': 'o-1', 'service': 'standard'}).status_code == 409
    assert c.get('/api/inventory').json() == after
    assert c.get('/api/orders').json() == orders_before_rejection
    assert c.get('/api/shipments/s-1').status_code == 404
    assert c.get('/api/events').json() == events, 'Rejected shipment must not change history.'
    # Repeated SKU lines reserve and restore their aggregate once.
    created = c.post('/api/orders', json={'customer': 'Rae', 'items': [{'sku': 'dock', 'quantity': 1}, {'sku': 'dock', 'quantity': 2}]})
    assert created.status_code == 201
    order = created.json()
    assert c.post(f"/api/orders/{order['id']}/cancel").status_code == 200
    assert c.get('/api/inventory').json() == after
    assert initial_stock != after


CHECKS = {'mock-support-bug': support_bug, 'mock-support-feature': support_feature,
          'mock-dispatch-bug': dispatch_bug, 'mock-dispatch-feature': dispatch_feature}

PATCHES = {
    'mock-support-bug': ('app/cache.py', 'queue_key', '''
def queue_key(team, status):
    return (status,)
'''),
    'mock-support-feature': ('app/assignments.py', 'assign_many', '''
def assign_many(store, request):
    raise HTTPException(501, 'Bulk assignment is not available yet')
'''),
    'mock-dispatch-bug': ('app/packages.py', 'billable_units', '''
def billable_units(weights):
    return (sum(weights) + 499) // 500
'''),
    'mock-dispatch-feature': ('app/orders.py', 'cancel', '''
def cancel(store, order_id):
    raise HTTPException(501, 'Cancellation is not available yet')
'''),
}
