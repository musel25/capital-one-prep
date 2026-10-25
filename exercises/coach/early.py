"""Instructor-only starters and HTTP checks for four independent applications."""
from fastapi.testclient import TestClient


PATCHES = {
    'd02-feature': ('app/timeline.py', 'timeline', '''
def timeline(store, ticket_id):
    raise HTTPException(501, 'Ticket timeline is not available yet')
'''),
    'd03-bug': ('app/billing.py', 'line_discount', '''
def line_discount(subtotal_cents, percent):
    return round(subtotal_cents * percent / 100)
'''),
    'd03-feature': ('app/quotes.py', 'quote', '''
def quote(request):
    raise HTTPException(501, 'Shipping quotes are not available yet')
'''),
    'd04-bug': ('app/search.py', 'browse', '''
def browse(catalog, genre, available_only, page, page_size):
    start = (page - 1) * page_size
    ordered = sorted(catalog.books.values(), key=lambda book: (book['title'].casefold(), book['id']))
    items = matching(ordered[start:start + page_size], genre, available_only)
    total = len(matching(ordered, genre, available_only))
    return {'items': items, 'total': total, 'page': page, 'page_size': page_size, 'has_next': start + page_size < total}
'''),
}


def fresh():
    from app.main import create_app
    client = TestClient(create_app())
    assert client.get('/health').json() == {'status': 'ok'}
    for path in ('/', '/static/app.js', '/static/style.css', '/openapi.json'):
        assert client.get(path).status_code == 200, f'Keep {path} available.'
    return client


def d02_feature():
    c = fresh()
    response = c.get('/api/tickets/t-101/timeline')
    assert response.status_code == 200, 'An existing ticket needs a readable timeline.'
    assert response.json() == {'items': [
        {'id': 'event-1', 'sequence': 1, 'kind': 'status', 'actor': 'Mina', 'text': 'new → open'},
        {'id': 'event-3', 'sequence': 3, 'kind': 'comment', 'actor': 'Jo', 'text': 'The printer is on the guest network.'},
    ]}
    assert c.get('/api/tickets/t-103/timeline').json() == {'items': []}
    assert c.get('/api/tickets/missing/timeline').status_code == 404
    assert c.post('/api/tickets/t-101/comments', json={'author': 'Alex', 'body': 'Moved to staff Wi-Fi.'}).status_code == 201
    assert c.post('/api/tickets/t-101/status', json={'actor': 'Alex', 'status': 'resolved'}).status_code == 200
    rows = c.get('/api/tickets/t-101/timeline').json()['items']
    assert rows[-2:] == [
        {'id': 'event-4', 'sequence': 4, 'kind': 'comment', 'actor': 'Alex', 'text': 'Moved to staff Wi-Fi.'},
        {'id': 'event-5', 'sequence': 5, 'kind': 'status', 'actor': 'Alex', 'text': 'open → resolved'},
    ]
    assert c.post('/api/tickets/t-101/status', json={'actor': 'Alex', 'status': 'resolved'}).status_code == 200
    assert c.post('/api/tickets/t-101/comments', json={'author': 'Alex', 'body': ' '}).status_code == 422
    assert c.post('/api/tickets/t-101/status', json={'actor': 'Alex', 'status': 'invalid'}).status_code == 422
    assert c.get('/api/tickets/t-101/timeline').json()['items'] == rows
    assert c.get('/api/tickets/t-102/timeline').json()['items'] == [
        {'id': 'event-2', 'sequence': 2, 'kind': 'comment', 'actor': 'Sam', 'text': 'The cable was replaced.'},
    ]
    assert c.get('/api/tickets/t-101').json()['status'] == 'resolved'


def d03_bug():
    c = fresh()
    before = c.get('/api/products').json()
    body = {'lines': [{'sku': 'notebook', 'quantity': 1}, {'sku': 'labels', 'quantity': 3}], 'discount_percent': 10}
    response = c.post('/api/invoices/preview', json=body)
    assert response.status_code == 200
    assert response.json() == {
        'lines': [
            {'sku': 'notebook', 'quantity': 1, 'subtotal_cents': 999, 'discount_cents': 99, 'total_cents': 900},
            {'sku': 'labels', 'quantity': 3, 'subtotal_cents': 147, 'discount_cents': 14, 'total_cents': 133},
        ], 'subtotal_cents': 1146, 'discount_cents': 113, 'total_cents': 1033,
    }, 'Invoice line discounts and totals must use the agreed whole-cent policy.'
    for percent, expected_total, expected_discount in [(0, 999, 0), (100, 0, 999)]:
        result = c.post('/api/invoices/preview', json={'lines': [{'sku': 'notebook', 'quantity': 1}], 'discount_percent': percent}).json()
        assert (result['total_cents'], result['discount_cents']) == (expected_total, expected_discount)
    repeat = c.post('/api/invoices/preview', json={'lines': [{'sku': 'labels', 'quantity': 1}, {'sku': 'labels', 'quantity': 1}], 'discount_percent': 50}).json()
    assert repeat['discount_cents'] == 48 and repeat['total_cents'] == 50
    assert c.post('/api/invoices/preview', json={'lines': [{'sku': 'missing', 'quantity': 1}]}).status_code == 404
    for percent in [-1, 101, True, 1.5, '10']:
        assert c.post('/api/invoices/preview', json={**body, 'discount_percent': percent}).status_code == 422
    for quantity in [0, 101, True, '1', 1.5]:
        assert c.post('/api/invoices/preview', json={'lines': [{'sku': 'labels', 'quantity': quantity}]}).status_code == 422
    assert c.post('/api/invoices/preview', json={'lines': []}).status_code == 422
    assert c.post('/api/invoices/preview', json=body).json() == response.json()
    assert c.get('/api/products').json() == before, 'Previews must not alter the product catalog.'


def d03_feature():
    c = fresh()
    before = c.get('/api/rates').json()
    body = {'zone': 'local', 'service': 'standard', 'weight_grams': 500, 'signature': False}
    response = c.post('/api/quotes', json=body)
    assert response.status_code == 200, 'Expose a shipping quote for supported routes.'
    assert response.json() == {'zone': 'local', 'service': 'standard', 'billable_units': 1, 'transport_cents': 400, 'signature_cents': 0, 'total_cents': 400, 'estimated_days': 2}
    for weight, units, total in [(1, 1, 400), (499, 1, 400), (501, 2, 500), (20000, 40, 4300)]:
        result = c.post('/api/quotes', json={**body, 'weight_grams': weight}).json()
        assert (result['billable_units'], result['total_cents']) == (units, total)
    express = c.post('/api/quotes', json={**body, 'zone': 'regional', 'service': 'express', 'weight_grams': 501, 'signature': True}).json()
    assert express == {'zone': 'regional', 'service': 'express', 'billable_units': 2, 'transport_cents': 1800, 'signature_cents': 250, 'total_cents': 2050, 'estimated_days': 2}
    remote = c.post('/api/quotes', json={**body, 'zone': 'remote', 'service': 'express'}).json()
    assert (remote['total_cents'], remote['estimated_days']) == (2500, 4)
    assert c.post('/api/quotes', json={**body, 'zone': 'missing'}).status_code == 404
    for change in [{'service': 'overnight'}, {'weight_grams': 0}, {'weight_grams': 20001}, {'weight_grams': True}, {'weight_grams': 0.5}, {'weight_grams': '500'}, {'signature': 'yes'}]:
        assert c.post('/api/quotes', json={**body, **change}).status_code == 422
    assert c.post('/api/quotes', json=body).json() == response.json()
    assert c.get('/api/rates').json() == before


def d04_bug():
    c = fresh()
    response = c.get('/api/books?genre=science&page=2&page_size=2')
    assert response.status_code == 200
    result = response.json()
    assert [row['id'] for row in result['items']] == ['b-05', 'b-07'], 'Filtered catalog pages must contain the next matching books.'
    assert {key: result[key] for key in ('total', 'page', 'page_size', 'has_next')} == {'total': 4, 'page': 2, 'page_size': 2, 'has_next': False}
    first = c.get('/api/books?genre=science&page=1&page_size=2').json()
    assert [row['id'] for row in first['items']] == ['b-01', 'b-03'] and first['has_next'] is True
    available = c.get('/api/books?genre=science&available_only=true&page_size=2').json()
    assert [row['id'] for row in available['items']] == ['b-01', 'b-05'] and available['total'] == 3
    for query in ['genre=missing', 'genre=science&page=3&page_size=2']:
        empty = c.get('/api/books?' + query).json()
        assert empty['items'] == [] and empty['has_next'] is False
    for query in ['page=0', 'page_size=0', 'page_size=21']:
        assert c.get('/api/books?' + query).status_code == 422
    assert c.post('/api/loans', json={'book_id': 'b-01', 'reader': 'Alex'}).status_code == 201
    after = c.get('/api/books?genre=science&available_only=true&page_size=2').json()
    assert [row['id'] for row in after['items']] == ['b-05', 'b-07'] and after['total'] == 2
    assert c.get('/api/books/b-01').json()['available'] is False
    assert c.get('/api/books?genre=science&page_size=20').json()['total'] == 4
    assert c.get('/api/loans').json()['items'] == [{'id': 'loan-1', 'book_id': 'b-01', 'reader': 'Alex'}]


CHECKS = {'d02-feature': d02_feature, 'd03-bug': d03_bug, 'd03-feature': d03_feature, 'd04-bug': d04_bug}
