"""Learner-facing briefs. The separate starter patches are instructor material."""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    context: str
    brief: str
    contract: str
    probe: str
    minutes: int = 20


TASKS = [
    Task('d01-bug', 'Restore transaction chronology', 'bank',
         'A customer says an afternoon purchase appears below an earlier purchase. Diagnose the observed ordering, write a regression test, and repair it without changing the fixtures.',
         'GET /api/transactions returns {items:[...]}. Sort by the actual occurred_at instant descending, accepting timezone offsets; ties use ID ascending. Preserve every transaction and its fields. Default pagination includes all seven fixtures. Pending transactions remain visible in this list.',
         'curl "http://127.0.0.1:8000/api/transactions"'),
    Task('d01-feature', 'Combine transaction filters', 'bank',
         'Customers need to narrow their transaction list by category and minimum amount. Add the two filters without changing existing chronology or pagination.',
         'GET /api/transactions accepts optional category (exact, case-sensitive) and min_cents (inclusive, integer >=0). Combine supplied filters with AND before pagination. Unknown categories return an empty items list. Omitted filters preserve current behavior; invalid minimum yields HTTP 422.',
         'curl "http://127.0.0.1:8000/api/transactions?category=groceries&min_cents=1500"'),
    Task('d02-bug', 'Keep rejected transfers atomic', 'bank',
         'After a transfer to an unknown destination fails, the sender reports a changed balance. Reproduce the issue and make rejected operations safe.',
         'POST /api/transfers takes {source,target,amount_cents}. Unknown source or destination: 404; insufficient funds: 409. Every rejected request leaves all balances and history unchanged. Success: 201 with {id,source,target,amount_cents}, debit once and credit once. No persistence or multi-worker concurrency is required for this local in-memory exercise.',
         'curl -i -X POST http://127.0.0.1:8000/api/transfers -H "Content-Type: application/json" -d \'{"source":"checking","target":"missing","amount_cents":500}\''),
    Task('d02-feature', 'Show both sides of transfer history', 'bank',
         'Support wants an account activity view that explains money moving in and out. Add transfer history using the existing transfer operation.',
         'GET /api/accounts/{account}/history returns {items:[{transfer_id,amount_cents}]}, in transfer creation order. Amount is negative for outgoing and positive for incoming. Both entries use the transfer response id. Existing accounts with no transfers return an empty list. Unknown account: 404. Failed transfers create no entries.',
         'curl "http://127.0.0.1:8000/api/accounts/checking/history"'),
    Task('d03-bug', 'Calculate cashback in exact cents', 'bank',
         'The October rewards preview differs from the written policy by a cent. Identify the discrepancy and preserve the posted/pending and purchase/refund rules.',
         'GET /api/cashback?month=YYYY-MM returns {cashback_cents}. Award 2% per posted purchase in the requested fixture month, floor each purchase reward to whole cents, then sum. Exclude pending transactions and all refunds. Use integer arithmetic. Empty month yields zero. Optional cap_cents already exists and must continue working.',
         'curl "http://127.0.0.1:8000/api/cashback?month=2026-10"'),
    Task('d03-feature', 'Add the monthly rewards cap', 'bank',
         'The rewards team introduced a configurable monthly maximum. Extend the existing preview without changing per-purchase rounding.',
         'GET /api/cashback accepts optional cap_cents, an integer >=0. Return the smaller of the calculated monthly total and the cap. Omitted cap is unlimited. Zero cap awards zero; negative cap returns 422. The cap applies after summing the floored 2% reward for each posted purchase.',
         'curl "http://127.0.0.1:8000/api/cashback?month=2026-10&cap_cents=120"'),
    Task('d04-bug', 'Repair filtered page boundaries', 'bank',
         'A customer scrolling a filtered feed sees sparse pages and missing purchases. Repair the interaction of filtering and pagination.',
         'GET /api/transactions uses category/min_cents filters, then chronology, then 1-based pagination. page>=1; page_size from 1 through 100. Page two of category=groceries with size two contains t01 then t07. Out-of-range pages return empty items. Keep total/page/page_size/has_next metadata consistent.',
         'curl "http://127.0.0.1:8000/api/transactions?category=groceries&page=2&page_size=2"'),
    Task('d04-feature', 'Return useful pagination metadata', 'bank',
         'The UI cannot tell whether to offer another page. Add metadata that continues to work on filtered and empty results.',
         'Extend GET /api/transactions response with total (all matching rows before slicing), page, page_size, and has_next (whether at least one matching row exists beyond this page). Preserve items. Empty results have total=0 and has_next=false. Exact final pages and out-of-range pages have has_next=false. Defaults remain page=1 and page_size=50.',
         'curl "http://127.0.0.1:8000/api/transactions?category=groceries&page=1&page_size=2"'),
    Task('d05-bug', 'Subtract refunds from net spending', 'bank',
         'The spending widget increases after a posted refund. Reproduce and fix the calculation while keeping pending purchases out of the report.',
         'GET /api/spend?month=YYYY-MM returns {net_cents}. In the requested fixture month, add posted purchases and subtract posted refunds; exclude pending rows. Each amount_cents is a positive magnitude. Refunds count in the refund month. Empty month yields zero. Do not change transaction data.',
         'curl "http://127.0.0.1:8000/api/spend?month=2026-10"'),
    Task('d05-feature', 'Group net spending by purchase category', 'bank',
         'Build a monthly category breakdown, including the effect of refunds. Refund feed labels are operational labels and should not create a separate spending category.',
         'GET /api/spend/categories?month=YYYY-MM returns {items:[{category,net_cents}]} sorted by category ascending. Include posted rows only. A refund is subtracted from the category of its purchase_id, even if its own category is adjustments. Filter by each row\'s month before aggregation; original purchase may be outside that month. Return an empty list for no posted rows. Fixture refund links are valid.',
         'curl "http://127.0.0.1:8000/api/spend/categories?month=2026-10"'),
    Task('d06-bug', 'Repair the dashboard account contract', 'bank',
         'The browser dashboard renders NaN for account balances although the server responds successfully. Trace the request/response and repair the interface contract.',
         'GET /api/accounts must return {items:[{id,balance_cents}]}. Each balance_cents is an integer number of cents. The browser displays dollars by dividing that value by 100 and formatting two decimal places. Keep the established API field name and the currency conversion in the browser; successful transfers must be reflected on refresh. Explain why HTTP 200 alone did not prove correct behavior.',
         'curl "http://127.0.0.1:8000/api/accounts"'),
    Task('d06-feature', 'Validate transfers at the API boundary', 'bank',
         'Browser form constraints are bypassable. Enforce transfer input rules at the server boundary and explain the division of responsibility.',
         'POST /api/transfers accepts amount_cents only as a strict positive JSON integer. Reject booleans, numeric strings, fractions, zero and negative values with HTTP 422. Also reject equal source and target with 422. Validation failure changes neither balance nor history. Existing valid transfers, unknown-account 404 and insufficient-funds 409 behavior remain. Do not rely on HTML validation.',
         'curl -i -X POST http://127.0.0.1:8000/api/transfers -H "Content-Type: application/json" -d \'{"source":"checking","target":"savings","amount_cents":"500"}\''),
    Task('d07-bug', 'Recover an unsafe AI retry change', 'bank',
         'A constructed AI-generated draft claims payment callback retries are safe. A repeated callback credits the balance twice. Treat the claim as unverified: reproduce it, inspect the change, and add evidence for the repaired behavior. No external AI service is required.',
         'POST /api/events takes {event_id,amount_cents} and credits checking. First valid callback returns 200 with {event_id,amount_cents,accepted:true}. Same event_id and amount returns exactly that response and credits nothing further. Same ID with different amount returns 409 without mutation. Distinct IDs credit independently. State is only in memory for this exercise.',
         'curl -X POST http://127.0.0.1:8000/api/events -H "Content-Type: application/json" -d \'{"event_id":"evt-1","amount_cents":1234}\''),
    Task('d07-feature', 'Make transfer retries idempotent', 'bank',
         'A client can lose the transfer response and retry. Add request-level idempotency while keeping ordinary transfers working.',
         'POST /api/transfers accepts optional Idempotency-Key header. Same key plus identical source/target/amount returns the original 201 body without another debit, credit or history entry. Reusing a key with a different payload returns 409. Without a key, each request is independent. Store keys only after a successful transfer, so a failed request does not consume its key. In-memory, single-process scope is sufficient.',
         'curl -X POST http://127.0.0.1:8000/api/transfers -H "Content-Type: application/json" -H "Idempotency-Key: request-1" -d \'{"source":"checking","target":"savings","amount_cents":500}\''),
    Task('d08-bug', 'Mock: select charges eligible for settlement', 'settlements',
         'You have joined the merchant operations team. Its payout preview includes a charge that is not ready to settle. Explore this unfamiliar repository and repair the eligibility rule. Work independently for 20 minutes, then explain for 5.',
         'GET /api/settlements?merchant_id=... returns {items:[charge]}. Include only charges for that merchant with status=captured and settled=false, in fixture order. Exclude authorized, refunded and already-settled charges. Unknown merchant yields empty items. This endpoint is a preview and must not mutate charges.',
         'curl "http://127.0.0.1:8000/api/settlements?merchant_id=fern"'),
    Task('d08-feature', 'Mock: summarize merchant payouts by day', 'settlements',
         'From a fresh clean snapshot, implement a daily payout preview for a merchant. Do not carry changes from the bug task. Work independently for 20 minutes, then explain for 5.',
         'GET /api/merchants/{merchant_id}/summary?on=YYYY-MM-DD returns {merchant_id,date,count,gross_cents,fees_cents,net_cents}. Aggregate that day\'s captured, unsettled charges for that merchant. net=gross-fees, all integer cents. Empty or unknown merchant yields zeros. Invalid date returns 422. A preview never marks charges settled.',
         'curl "http://127.0.0.1:8000/api/merchants/fern/summary?on=2026-10-30"'),
    Task('d09-bug', 'Variant: promotion window boundaries', 'promotions',
         'Support reports that a promotion is still offered at its exact expiration instant. Recheck all boundaries, including an equivalent timestamp expressed with an offset.',
         'POST /api/eligibility takes {at,amount_cents,active_member} and returns {eligible:boolean}. at is a timezone-aware ISO instant. Qualification requires active_member=true, amount_cents>=5000, and 2026-10-30T00:00:00Z <= at < 2026-11-01T00:00:00Z. Compare instants, not local date text. Existing strict type validation must remain.',
         'curl -X POST http://127.0.0.1:8000/api/eligibility -H "Content-Type: application/json" -d \'{"at":"2026-11-01T00:00:00Z","amount_cents":5000,"active_member":true}\''),
    Task('d09-feature', 'Variant: quote a capped promotion reward', 'promotions',
         'Build a reward quote on top of the existing promotion policy. Exercise the minimum, rounding and cap boundaries explicitly.',
         'POST /api/rewards/quote accepts the same body as /api/eligibility and returns {eligible:boolean,reward_cents:int}. Eligible purchases earn 5%, floored to whole cents, capped at 500 cents per purchase. Ineligible purchases earn zero. Reuse the existing membership, minimum-spend and inclusive-start/exclusive-end rules; do not duplicate conflicting eligibility logic.',
         'curl -X POST http://127.0.0.1:8000/api/rewards/quote -H "Content-Type: application/json" -d \'{"at":"2026-10-31T10:00:00Z","amount_cents":5001,"active_member":true}\''),
    Task('d10-bug', 'Final mock: reserve inventory atomically', 'inventory',
         'You are on a supply platform team. A rejected order appears to consume inventory. Explore this unfamiliar app, reproduce the failure, and repair the reservation behavior. Use 20 minutes and a 5-minute explanation.',
         'POST /api/reservations takes {items:[{sku,quantity}]}. Sum repeated SKUs. Unknown SKU returns 404; insufficient total stock for any SKU returns 409. Failure changes no stock and creates no reservation. Success returns 201 with {id,status:"active",items} and decrements each SKU by its total quantity exactly once. Positive strict integer quantities and nonempty lists are required. Local single-process in-memory scope.',
         'curl -X POST http://127.0.0.1:8000/api/reservations -H "Content-Type: application/json" -d \'{"items":[{"sku":"dock","quantity":2},{"sku":"cable","quantity":99}]}\''),
    Task('d10-feature', 'Final mock: cancel reservations safely', 'inventory',
         'Start a fresh snapshot. Add cancellation without allowing retries to create stock. Use 20 minutes and a 5-minute explanation; preserve all existing reservation behavior.',
         'POST /api/reservations/{id}/cancel returns the reservation with status="canceled" and HTTP 200. Restore all reserved quantities exactly once. Repeating cancellation returns the same canceled reservation without changing stock again. Unknown ID returns 404. GET /api/reservations must reflect the canceled status. Cancellation and reservation use integer quantities.',
         'curl -X POST http://127.0.0.1:8000/api/reservations/r-1/cancel'),
]

BY_ID = {task.id: task for task in TASKS}


def public_tasks():
    return [asdict(task) for task in TASKS]
