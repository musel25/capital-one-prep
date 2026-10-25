"""Learner-facing product briefs for the middle of the sequence."""

TASK_DATA = {
    'd04-feature': {
        'title': 'Offer appointment availability',
        'context': 'appointments',
        'brief': 'The reception team can see bookings but cannot offer visitors a list of available appointments. Add an availability view that stays accurate as appointments are booked.',
        'contract': 'GET /api/availability?provider_id=aria&on=2026-10-26&duration_minutes=30 returns {provider_id,date,duration_minutes,items:[{start,end}]}, with HH:MM times ascending. duration_minutes is 30 (default) or 60; other values and invalid dates return 422. Candidate starts are every 30 minutes from that provider’s opening time; the entire requested duration must fit before or at closing. Exclude candidates overlapping a confirmed booking for the same provider and day. Intervals are half-open: an appointment ending at a booking’s start, or starting at its end, is allowed. Canceled bookings do not block. A known provider without hours that day returns empty items; unknown provider returns 404. GET is read-only. Existing POST /api/bookings takes {provider_id,on,start,duration_minutes}, creates a confirmed booking with 201, rejects an unavailable slot with 409, and rejects an unknown provider with 404 without mutation. Local clock times require no timezone conversion in this exercise.',
        'probe': 'curl "http://127.0.0.1:8000/api/availability?provider_id=aria&on=2026-10-26&duration_minutes=30"',
        'orientation': 'Juniper Appointments is a fictional neighborhood repair clinic. Providers have dated opening hours; bookings include confirmed and canceled visits. The browser shows the roster and bookings and offers an availability request. All state resets on restart.',
    },
    'd05-bug': {
        'title': 'Reconcile a usage invoice',
        'context': 'usage',
        'brief': 'A customer’s usage invoice is larger than the metered work they performed. Investigate the usage feed and repair the billing total while preserving the raw delivery history.',
        'contract': 'GET /api/workspaces/{workspace_id}/bill?month=YYYY-MM returns {workspace_id,month,billable_samples,units,charge_cents}. Only accepted events in the requested workspace and month are billable. A logical sample is identified by (workspace_id,month,meter_id,sample_id); repeated deliveries of that sample count once even when event_id differs. Different meters, months, workspaces, and sample IDs remain independent. Accepted repeated deliveries of a logical sample have identical units in this exercise. Rate is 3 cents per unit. Pending and rejected events contribute nothing. Empty month returns zeros; unknown workspace returns 404; malformed or impossible month returns 422. GET must preserve raw events. POST /api/events accepts {event_id,workspace_id,month,meter_id,sample_id,units,status}; IDs are nonempty, units is a strict positive JSON integer, status is accepted/pending/rejected, and month follows the same rule. Unknown workspace returns 404, reused event_id returns 409, and invalid requests return 422 with no mutation. A new event_id can record another delivery of the same sample.',
        'probe': 'curl "http://127.0.0.1:8000/api/workspaces/north/bill?month=2026-10"',
        'orientation': 'Meter Trail is a fictional developer platform. Its raw feed records delivery events for API and storage meters. Workspace invoices and raw events are separate views; the browser can inspect both and ingest an example delivery. All state is in memory.',
    },
    'd05-feature': {
        'title': 'Summarize employee expenses',
        'context': 'expenses',
        'brief': 'The operations team needs a monthly view of approved reimbursement and expenses still awaiting review. Add an employee summary without changing the claim submission workflow.',
        'contract': 'GET /api/employees/{employee_id}/summary?month=YYYY-MM returns {employee_id,month,approved_cents,pending_cents,items:[{category,approved_cents,pending_cents}]}. Select expenses for this employee by incurred_on month. Sum approved and pending amounts separately, including them in both overall and per-category totals. Exclude rejected expenses completely, including categories containing only rejected expenses. Categories sort ascending. A known employee with no included expenses returns zero totals and empty items. Unknown employee returns 404; malformed or impossible month returns 422. The summary is read-only. Existing POST /api/expenses accepts {employee_id,incurred_on,category,amount_cents,description}; it creates a pending expense with 201. Categories are meals, supplies, or travel; amount is a strict positive integer; blank descriptions and invalid dates return 422; unknown employee returns 404. Failed submissions leave the ledger unchanged.',
        'probe': 'curl "http://127.0.0.1:8000/api/employees/ada/summary?month=2026-10"',
        'orientation': 'Fieldwork Expenses is a fictional operations ledger. Employees submit dated claims, and fixture claims have approved, pending, or rejected review states. The browser displays employees and the ledger, with a monthly summary control. Amounts use integer cents.',
    },
    'd06-bug': {
        'title': 'Restore the latency display contract',
        'context': 'telemetry',
        'brief': 'The service monitor displays implausibly large request latencies even though its requests succeed. Trace the browser/API agreement and restore the expected values without changing the collected samples.',
        'contract': 'GET /api/services/{service_id}/readings returns {items:[{id,service_id,duration_ms,status}]} in collection order. duration_ms is a JSON number measured in milliseconds, with fractional milliseconds preserved. Stored samples and POST /api/readings input use duration_us (integer microseconds); 1000 microseconds equals 1 millisecond. The browser uses duration_ms directly and formats one decimal place with an ms label. POST accepts {service_id,duration_us,status}, where duration_us is a strict integer >=0 and status is ok/error, and returns the same public reading shape with 201. Unknown service returns 404; invalid input returns 422 without recording a sample. GET /api/services/{service_id}/summary returns {service_id,count,error_count,slow_count}; slow means at least 200000 microseconds. Preserve this existing summary and all raw samples. Zero and fractional-millisecond readings must remain valid. Explain why HTTP 200 alone did not establish a correct interface.',
        'probe': 'curl "http://127.0.0.1:8000/api/services/atlas/readings"',
        'orientation': 'Pulse Window is a fictional browser service monitor. Collectors submit request timings, while operators inspect a latency table and simple health counts. The collector’s storage unit is documented in the API input schema. The browser includes a sample submission control.',
    },
    'd06-feature': {
        'title': 'Validate a contact batch import',
        'context': 'contacts',
        'brief': 'An events team wants to import several contacts in one request. Build the batch operation so invalid or conflicting rows never leave a partially imported directory.',
        'contract': 'POST /api/imports takes {contacts:[{name,email,team}]} with 1 through 50 rows and returns 201 with {items:[{id,name,email,team}]} in input order. Existing row rules apply: name is a nonblank string, email is a trimmed address with one @ and a dotted domain and no whitespace, and team is events or support. Names are trimmed and emails are trimmed/lowercased before storage. Reject invalid rows or batch size with 422. Reject repeated normalized emails within the batch or emails already in the directory with 409. Any rejection preserves the entire directory and consumes no IDs. Success adds all rows exactly once and returns consecutive IDs. GET /api/contacts lists contacts in creation order; GET /api/contacts/{id} returns 404 for an unknown ID. Existing POST /api/contacts creates one validated contact and rejects duplicate normalized emails with 409. In-memory, single-process scope; import retry idempotency is not requested.',
        'probe': 'curl -i -X POST http://127.0.0.1:8000/api/imports -H "Content-Type: application/json" -d \'{"contacts":[{"name":"Rae Lin","email":"rae@example.com","team":"events"}]}\'',
        'orientation': 'Gather Directory is a fictional events-team contact list. A small address book already supports individual contact creation; the browser also offers a JSON batch form. Teams and contact IDs are local to this training application. All state resets on restart.',
    },
}
