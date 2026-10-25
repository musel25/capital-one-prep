"""Public revision-2 prompts for the final unfamiliar feature applications."""

TASK_DATA = {
    'd07-bug': {
        'title': 'Investigate repeated delivery notifications',
        'context': 'webhooks',
        'brief': 'Residents sometimes receive two notifications for one parcel update. Investigate the delivery workflow and repair the observed behavior while preserving legitimate updates.',
        'orientation': 'Parcel Signal receives delivery updates from a fictional locker operator and displays outgoing resident notifications. Two parcels are registered, and each update carries an event ID, parcel ID and delivery status.',
        'contract': '''POST /api/deliveries accepts {event_id, parcel_id, status}; status is "arrived" or "delayed". Event IDs are nonempty strings of at most 80 characters. A first valid event returns 200 with {event_id, accepted: true, notification_id} and appends exactly one notification.

An exact retry of an accepted event ID and payload returns the original response with 200 and sends no additional notification. Reusing an accepted event ID with a different parcel_id or status returns 409 without changing receipts or notifications. Check this identity conflict even if the new parcel ID is unknown. Different event IDs remain independent, including updates for the same parcel.

An unknown parcel on a new event returns 404; malformed payloads return 422. Rejected events create no receipts or notifications and do not reserve an event ID. GET /api/parcels, /api/deliveries and /api/notifications retain their {items: [...]} shapes. Parcel records are not modified by delivery updates. Retry guarantees cover sequential requests in one server process.''',
        'probe': '''curl -s -X POST http://127.0.0.1:8000/api/deliveries -H 'Content-Type: application/json' -d '{"event_id":"delivery-1001","parcel_id":"parcel-101","status":"arrived"}'
curl -s http://127.0.0.1:8000/api/notifications''',
    },
    'd07-feature': {
        'title': 'Add repeatable export submissions',
        'context': 'jobs',
        'brief': 'The operations team wants to retry an export submission after losing the response without creating another export job. Add request-key support while keeping ordinary submissions available.',
        'orientation': 'Export Desk queues fictional museum and support dataset exports. Jobs have a dataset, output format, row count and queued status; no background worker runs in this demo.',
        'contract': '''POST /api/jobs accepts {dataset_id, format}; format is "csv" or "json". A successful submission returns 201 with {id, dataset_id, format, row_count, status: "queued"}. Add optional Idempotency-Key header behavior: the first successful use creates one job; the same key and same dataset_id/format returns the original job with 201; the same key with a changed dataset_id or format returns 409 without creating a job. Keys are case-sensitive, are not trimmed, contain 1–64 characters and cannot be whitespace-only. Empty, whitespace-only or oversized headers return 422.

Without the header, every valid call creates a separate job. Different keys are independent even for identical payloads. Unknown datasets return 404; invalid formats or missing required fields return 422. A failed submission must not reserve a key. No rejected request changes the queue or dataset catalog. GET /api/jobs lists {items: [...]} and GET /api/jobs/{id} returns the stored job (404 if absent). Scope is sequential requests in one server process.''',
        'probe': '''curl -s -X POST http://127.0.0.1:8000/api/jobs -H 'Content-Type: application/json' -H 'Idempotency-Key: export-request-1' -d '{"dataset_id":"visits","format":"csv"}'
curl -s http://127.0.0.1:8000/api/jobs''',
    },
    'd08-feature': {
        'title': 'Build a daily studio attendance report',
        'context': 'attendance',
        'brief': 'The studio coordinator needs a daily report of completed attendance, including time spent by each member. Add the report without changing the session log or member views.',
        'orientation': 'Studio Attendance records entry and exit timestamps for three fictional members. Its sample log contains timezone offsets, visits across midnight and a visit whose exit has not yet been recorded.',
        'contract': '''GET /api/attendance?on=YYYY-MM-DD returns 200 with {date, timezone: "UTC", session_count, member_count, total_minutes, items: [{member_id, minutes}]}. The date is required; malformed or impossible dates return 422.

The reporting interval is midnight UTC on that date through, but not including, the next midnight. Include only sessions with an ended_at value and positive overlap with this interval. Interpret each timestamp's timezone offset; a visit spanning days contributes only its overlap with the requested day. A visit ending exactly at the day's start or starting exactly at its end contributes nothing. Open visits are excluded entirely.

session_count counts included sessions, while member_count counts distinct included members. For each member, sum overlap seconds and floor that member's total to whole minutes. Sort items by member_id ascending. total_minutes is the sum of the returned member minutes. No attendance returns zero counts, zero total_minutes and items: []. October 31 has 4 completed overlapping sessions, 2 members and 195 minutes (ada: 105, ben: 90). Reporting must not alter /api/sessions, /api/members or member-specific session views.''',
        'probe': 'curl -s "http://127.0.0.1:8000/api/attendance?on=2026-10-31"',
    },
    'd09-feature': {
        'title': 'Quote a mid-period subscription upgrade',
        'context': 'subscriptions',
        'brief': 'Customer support needs a preview of the charge for changing plans during a billing period. Add an upgrade quote with a caller-supplied maximum charge; requesting a quote must not change the subscription.',
        'orientation': 'Plan Studio has three fictional subscription plans priced in integer cents and customer subscriptions with explicit billing-period dates. The current product exposes catalogs and account detail; billing and payment collection are outside this exercise.',
        'contract': '''POST /api/subscriptions/{id}/quote accepts {target_plan, effective_on, cap_cents?}. effective_on is a calendar date. cap_cents is optional/null or a nonnegative strict integer; reject booleans, strings, fractions and negative caps with 422. Return 200 with {subscription_id, target_plan, effective_on, cycle_days, remaining_days, uncapped_cents, charge_cents}.

Use the subscription's period_start and period_end dates: cycle_days is end minus start and remaining_days is end minus effective_on. effective_on may equal either endpoint but must not lie outside them (422). The quote is the monthly target price minus current price, multiplied by remaining_days and divided by cycle_days, floored once to integer cents. The end date therefore quotes zero. charge_cents is the smaller of this amount and the optional cap; an omitted/null cap is unlimited and a zero cap is valid.

Unknown subscriptions or target plans return 404. Cancelled subscriptions and a target priced below the current plan return 409; quoting the current plan is allowed and returns zero. Do not mutate subscriptions or plan prices, including after rejection. For sub-100 changing from basic (1200) to plus (3100) on 2026-10-16, cycle_days is 31, remaining_days is 16 and uncapped_cents is 980.''',
        'probe': '''curl -s -X POST http://127.0.0.1:8000/api/subscriptions/sub-100/quote -H 'Content-Type: application/json' -d '{"target_plan":"plus","effective_on":"2026-10-16","cap_cents":500}' ''',
    },
    'd10-feature': {
        'title': 'Record equipment returns safely',
        'context': 'lending',
        'brief': 'The equipment desk can check out field kits but needs to record full-loan returns. Staff may submit the same return more than once when the network is unreliable. Add the return operation and preserve accurate availability.',
        'orientation': 'Field Kit Library tracks a small shared inventory and named loans. Cameras and tripods have total and available quantities; the initial loan list includes active loans and one already returned loan.',
        'contract': '''POST /api/loans/{loan_id}/return requires no body. For an active loan, return 200 with the loan's existing {id, equipment_id, borrower, quantity, status} fields and status "returned". Restore exactly that loan's quantity to the matching equipment's available count. Other equipment and loans remain unchanged.

Repeating a return, including for a loan that was already returned in the initial fixtures, returns the same loan with 200 and does not change availability again. This remains true if the equipment has been checked out under another loan in the meantime. Unknown loan IDs return 404 and change no state. Returns are full-loan only; do not create a replacement loan or change total stock.

GET /api/equipment, GET /api/loans and GET /api/loans/{id} reflect successful operations. Preserve checkout behavior: POST /api/loans accepts {equipment_id, borrower, quantity}, creates an active loan with 201 and reduces availability; unknown equipment returns 404, insufficient availability returns 409 and nonpositive/non-integer quantities return 422. Retry guarantees cover sequential requests in one server process.''',
        'probe': '''curl -s -X POST http://127.0.0.1:8000/api/loans/loan-1/return
curl -s http://127.0.0.1:8000/api/equipment''',
    },
}
