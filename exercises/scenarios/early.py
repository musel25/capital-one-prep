"""Learner-facing context and interviewer answers for early revision-2 tasks."""

TASK_DATA = {
    'd02-feature': {
        'title': 'Add a support ticket timeline',
        'context': 'helpdesk',
        'brief': 'The support team can leave comments and update ticket status, but cannot see a combined activity timeline. Add that view while preserving the existing ticket workflow.',
        'contract': 'GET /api/tickets/{ticket_id}/timeline returns 200 with {items:[{id,sequence,kind,actor,text}]}. Include only that ticket\'s comments and status changes, ordered by ascending sequence. id is event-{sequence}; kind is comment or status. Comment actor/text come from author/body. Status actor comes from the transition actor and text is "previous → current" (spaces around the arrow). Existing ticket with no activity returns empty items; unknown ticket returns 404. New comments and actual status changes must appear immediately. Repeating the current status creates no event; rejected writes create none. Existing POST /api/tickets/{id}/comments takes {author,body}, returns 201, and rejects blank values with 422. POST /api/tickets/{id}/status takes {actor,status}, returns 200, and accepts only new/open/resolved; invalid requests return 422. Both write endpoints return 404 for an unknown ticket. Reading the timeline changes no ticket or activity.',
        'probe': 'curl http://127.0.0.1:8000/api/tickets/t-101/timeline',
        'orientation': 'Lantern Desk is a fictional internal support queue. The browser lists three tickets and provides comment and status controls. t-101 concerns a printer, t-102 a monitor, and t-103 a new starter. Data lives in memory and resets when the application restarts. Existing tests cover ticket lookup and updates.',
    },
    'd03-bug': {
        'title': 'Repair invoice preview totals',
        'context': 'invoices',
        'brief': 'A stationery supplier reports that some discounted invoice previews disagree with its expected whole-cent totals. Investigate a reproducible example and repair the preview without changing its catalog or request validation.',
        'contract': 'POST /api/invoices/preview takes {lines:[{sku,quantity}],discount_percent:0}. Each line subtotal is catalog unit_cents × quantity; its discount is the percentage of that subtotal, rounded down to whole cents. Line total is subtotal minus discount. Return {lines:[{sku,quantity,subtotal_cents,discount_cents,total_cents}],subtotal_cents,discount_cents,total_cents}; top-level values sum their corresponding line fields. Preserve input order and keep repeated SKUs as separate lines. All amounts are integer cents. discount_percent is a strict integer from 0 through 100 inclusive; quantity is a strict integer from 1 through 100 inclusive; booleans, strings and decimals are rejected. A nonempty lines list is required. Invalid bodies return 422; unknown SKU returns 404. GET /api/products supplies the catalog. A preview never changes products or persists an invoice.',
        'probe': 'curl -X POST http://127.0.0.1:8000/api/invoices/preview -H "Content-Type: application/json" -d \'{"lines":[{"sku":"notebook","quantity":1},{"sku":"labels","quantity":3}],"discount_percent":10}\'',
        'orientation': 'Paper Trail is a fictional stationery supplier. Its quote screen builds invoice lines from notebooks, label sheets and clip packs. The catalog uses integer unit prices. The app calculates previews only; there is no payment, stock allocation or persistence. Existing tests cover catalog lookup and undiscounted invoices.',
    },
    'd03-feature': {
        'title': 'Add parcel delivery quotes',
        'context': 'parcels',
        'brief': 'A parcel counter displays delivery rates but cannot calculate a customer quote. Implement a preview for package weight and selected service options.',
        'contract': 'POST /api/quotes takes {zone,service,weight_grams,signature:false}. service is standard or express. weight_grams must be a strict integer from 1 through 20000 inclusive; signature is a strict boolean. Invalid bodies return 422 and unknown zone returns 404. GET /api/rates lists local (base_cents=300,per_unit_cents=100,standard_days=2), regional (600,150,4), and remote (1000,250,7). One billable unit is 500 grams; any partial unit counts as a full unit. Standard transport is base_cents + units × per_unit_cents. Express doubles the transport charge and halves standard_days, rounding days up. Signature adds 250 cents after the service calculation. Return {zone,service,billable_units,transport_cents,signature_cents,total_cents,estimated_days}. All counts and money are integers. Quotes are read-only and do not change the rates.',
        'probe': 'curl -X POST http://127.0.0.1:8000/api/quotes -H "Content-Type: application/json" -d \'{"zone":"regional","service":"express","weight_grams":501,"signature":true}\'',
        'orientation': 'Parcel Lane is a fictional shipping counter. Rate cards cover three delivery zones; the browser has a weight input and service and signature options. The app only quotes prices, with no label purchase or address handling. Existing tests cover rate cards and request validation.',
    },
    'd04-bug': {
        'title': 'Repair filtered library pages',
        'context': 'library',
        'brief': 'Library readers see unexpectedly short or missing results when browsing filtered catalog pages. Investigate how the results change across pages and after a checkout, then repair the browsing behavior.',
        'contract': 'GET /api/books accepts optional genre (exact match), available_only (boolean, default false), page (default 1, minimum 1), and page_size (default 3, range 1–20). Return {items,total,page,page_size,has_next}. Items contain {id,title,author,genre,available}; order the matching catalog by title case-insensitively, then id ascending, and return the requested 1-based page. total counts all matches, and has_next is true only if matching results remain after this page. Unknown genres and pages past the end yield empty items and has_next=false. Invalid pagination returns 422. GET /api/books/{id} returns 404 for unknown books. Existing POST /api/loans takes {book_id,reader}, returns 201 and marks the book unavailable; unknown book returns 404 and already-unavailable book returns 409. A subsequent available_only browse must reflect a successful checkout. Browsing never creates loans or changes availability.',
        'probe': 'curl "http://127.0.0.1:8000/api/books?genre=science&page=2&page_size=2"',
        'orientation': 'Maple Library is a fictional neighborhood collection. Seven books span science, fiction and history; one book starts checked out. The browser provides catalog filters, page navigation and checkout controls. Data resets when the app restarts. Existing tests cover individual book lookup and borrowing.',
    },
}
