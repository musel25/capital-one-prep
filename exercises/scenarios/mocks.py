"""Learner-facing context and acceptance criteria for the larger mock apps."""
SUPPORT_CONTEXT = (
    'Atlas Support Operations is a fictional internal help desk. The browser explores queues, '
    'assigns work, comments on tickets and changes status. The API also provides search, '
    'a staff directory, overview counts and activity history. Platform starts with open t-1 '
    '(priority 1) and t-4 (priority 3), plus resolved t-3. Support starts with open t-2 '
    '(priority 2). a-1 is active in platform, a-2 active in support, a-3 inactive in platform. '
    'All state belongs to one in-memory app instance. Discover the request path and relevant '
    'tests without reading every module. Bug and feature attempts are separate snapshots.'
)
DISPATCH_CONTEXT = (
    'Parcel Dispatch is a fictional warehouse console with catalog, inventory, order '
    'reservation, rate cards, quote previews, shipment records, tracking and activity history. '
    'Each physical product unit is packed separately. Cable weighs 250 grams and dock 750. '
    'Available inventory starts at cable=5 and dock=4, already excluding existing reservations. '
    'o-1 reserves two cables, o-2 reserves one dock and o-3 is already shipped. '
    'No carrier calls or real purchases occur. Data resets with a new app instance. '
    'Bug and feature attempts are independent snapshots.'
)
TASK_DATA = {
    'mock-support-bug': {
        'title': 'Investigate inconsistent support queues', 'context': 'support_ops',
        'brief': 'An operator says a queue sometimes shows work from the wrong team after switching filters. Reproduce the issue and restore accurate queue results without changing fixtures or removing supported filters.',
        'orientation': SUPPORT_CONTEXT,
        'contract': 'GET /api/queues accepts team=platform|support (default platform), status=open|resolved (default open), page>=1 (default 1), page_size=1..20 (default 2). Return {items,total,has_next}. Select exactly the requested team/status, sort by priority then id ascending, then paginate. total is the full matching count; has_next is true only when more matching rows remain. Past-end pages have empty items. Queries must be independent of previous queries and their order; comments/status changes and assignments must be reflected in later reads. Reads never change tickets or append events. Invalid filter values or pagination return 422. Preserve comments, status changes, assignments, search and event history. POST /api/tickets/{id}/status takes {actor,status}; actors are trimmed nonblank strings, statuses open|resolved. An actual transition adds one event; repeating status adds none.',
        'probe': 'curl "http://127.0.0.1:8000/api/queues?team=support&status=open"; curl "http://127.0.0.1:8000/api/queues?team=platform&status=open"',
    },
    'mock-support-feature': {
        'title': 'Assign a batch of support tickets', 'context': 'support_ops',
        'brief': 'Team leads need to assign several open tickets in one operation. Implement the existing bulk-assignment API so invalid requests cannot leave partially assigned work.',
        'orientation': SUPPORT_CONTEXT,
        'contract': 'POST /api/assignments accepts {ticket_ids:[id,...],agent_id,actor}. ticket_ids must have 1..10 entries; all strings are trimmed and nonblank. Invalid bodies return 422. Deduplicate ticket IDs in first-occurrence order. Missing agent or ticket returns 404; an inactive agent, resolved ticket or ticket from a different team returns 409. If any validation fails, preserve ALL tickets and the complete event history, including sequence numbering. For a valid batch, change only tickets not already assigned to that agent. Return 200 with {updated:[changed IDs in first-occurrence order]}; add exactly one assignment event for each change, with the supplied actor and previous/current agent IDs. No-op assignments return empty updated and no events. Subsequent queue/overview/ticket/history reads must reflect successful changes. Existing comment/status/search behavior remains supported. Sequential requests and in-memory state only; do not claim database/concurrent atomicity.',
        'probe': 'curl -X POST http://127.0.0.1:8000/api/assignments -H "Content-Type: application/json" -d \'{"ticket_ids":["t-4","t-1"],"agent_id":"a-1","actor":"learner"}\'',
    },
    'mock-dispatch-bug': {
        'title': 'Investigate multi-parcel shipping charges', 'context': 'dispatch',
        'brief': 'The shipping desk reports that some multi-parcel previews and shipment charges disagree with its rate cards. Reproduce a discrepancy and repair the shared behavior without changing stock, catalog weights or rates.',
        'orientation': DISPATCH_CONTEXT,
        'contract': 'POST /api/quotes accepts {weights_grams:[...],service,signature:false}. There must be 1..200 parcel weights, each a strict integer from 1 through 20000. service is standard|express and signature is a strict boolean. Invalid requests return 422. Each separately labeled parcel has its own base charge and is rounded UP independently to 500-gram billing units. Standard: 100 cents base per parcel + 40 per unit. Express: 200 base per parcel + 75 per unit. Signature adds 100 cents once per shipment, not per parcel. Return {parcels,billable_units,transport_cents,signature_cents,total_cents}, all integer counts/cents. Quotes are read-only. POST /api/shipments takes {order_id,service,signature:false}; a reserved order ships each physical unit as a separate parcel, uses the same quote rules, becomes shipped and adds one shipment event. Unknown order returns 404; shipped/cancelled order returns 409 without mutation. Preserve reservation, tracking and event behavior.',
        'probe': 'curl -X POST http://127.0.0.1:8000/api/quotes -H "Content-Type: application/json" -d \'{"weights_grams":[250,250],"service":"standard"}\'',
    },
    'mock-dispatch-feature': {
        'title': 'Cancel warehouse reservations safely', 'context': 'dispatch',
        'brief': 'Customers need to cancel reserved orders before shipment. Implement the cancellation API and make repeated cancellation safe, while preserving order history and inventory accuracy.',
        'orientation': DISPATCH_CONTEXT,
        'contract': 'POST /api/orders/{id}/cancel takes no body and returns the full order with status=cancelled. For a reserved order, restore every reserved quantity to available inventory, set cancelled, and append one cancelled event containing the order items. Repeated cancellation returns 200 with the same order and changes neither stock nor events. Unknown order returns 404. A shipped order returns 409 and preserves orders, stock, shipments and history. Other orders are unaffected. A cancelled order cannot ship: POST /api/shipments must return 409 without mutation. Repeated SKU lines in an order restore their combined quantity once. Existing POST /api/orders accepts {customer,items:[{sku,quantity}]} and reserves all lines together; invalid stock/SKU requests change nothing. GET /api/inventory, /api/orders/{id}, /api/events and /api/orders/{id}/events expose the results. Use the existing sequential in-memory scope, not external persistence or carrier operations.',
        'probe': 'curl -X POST http://127.0.0.1:8000/api/orders/o-1/cancel',
    },
}
