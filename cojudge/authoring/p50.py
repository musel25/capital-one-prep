import random
REFERENCE='''def solve(data: dict) -> dict:
    balances = dict(data["balances"])
    committed = {}
    events = []
    results = []
    for op in data["payments"]:
        key = op["key"]
        payload = (op["from"], op["to"], op["amount"])
        if key in committed:
            results.append("replay" if committed[key] == payload else "conflict")
            continue
        source, target, amount = payload
        if balances[source] < amount:
            results.append("insufficient")
            continue
        staged = dict(balances)
        staged[source] -= amount
        if op["fail"] == "debit":
            results.append("failed")
            continue
        staged[target] += amount
        event = [key, source, target, amount]
        if op["fail"] == "outbox":
            results.append("failed")
            continue
        balances = staged
        committed[key] = payload
        events.append(event)
        results.append("ok")
    return {"results": results, "balances": balances, "events": events}
'''
def p(key="k",amount=2,fail="none",source="a",target="b"):return {"key":key,"from":source,"to":target,"amount":amount,"fail":fail}
def ev(key="k",amount=2,source="a",target="b"):return [key,source,target,amount]
def c(balances,ops,status,end,events,label):return {"input":{"balances":balances,"payments":ops},"expected":{"results":status,"balances":end,"events":events},"label":label}
CASES=[c({"a":5,"b":0},[p()],["ok"],{"a":3,"b":2},[ev()],"payment commits balance changes and event"),c({"a":5,"b":0},[p(),p()],["ok","replay"],{"a":3,"b":2},[ev()],"retry has no duplicate effect or event"),c({"a":5,"b":0},[p(fail="debit"),p()],["failed","ok"],{"a":3,"b":2},[ev()],"retry after partial staged debit"),c({},[],[],{},[],"empty service"),c({"a":0,"b":0},[p()],["insufficient"],{"a":0,"b":0},[],"insufficient funds reserve no key"),c({"a":2,"b":1},[p()],["ok"],{"a":0,"b":3},[ev()],"exact balance"),c({"a":5,"b":0},[p(fail="outbox")],["failed"],{"a":5,"b":0},[],"outbox failure rolls back all state"),c({"a":5,"b":0},[p(),p(amount=3)],["ok","conflict"],{"a":3,"b":2},[ev()],"changed amount conflicts"),c({"a":5,"b":0,"c":0},[p(),p(target="c")],["ok","conflict"],{"a":3,"b":2,"c":0},[ev()],"changed destination conflicts"),c({"a":5,"b":5,"c":0},[p(target="c"),p(source="b",target="c")],["ok","conflict"],{"a":3,"b":5,"c":2},[ev(target="c")],"changed source conflicts"),c({"a":2,"b":0},[p(),p(fail="outbox")],["ok","replay"],{"a":0,"b":2},[ev()],"replay precedes balance and fault checks"),c({"a":1,"b":4},[p(),p("fund",3,source="b",target="a"),p()],["insufficient","ok","ok"],{"a":2,"b":3},[ev("fund",3,"b","a"),ev()],"retry after incoming funds"),c({"a":10,"b":0},[p("z",3),p("a",4,"outbox"),p("a",2)],["ok","failed","ok"],{"a":5,"b":5},[ev("z",3),ev("a",2)],"events preserve commit order and failed payload can change"),c({"a":1,"b":0},[p(fail="debit")],["insufficient"],{"a":1,"b":0},[],"funds rejection precedes fault"),c({"a":5,"b":0},[p(),p(amount=9,fail="outbox")],["ok","conflict"],{"a":3,"b":2},[ev()],"conflict precedes funds and fault")]
rng=random.Random(50)
generated=[]
for i in range(24):
 ops=[]
 for j in range(30):
  source,target=rng.sample("abc",2);ops.append(p(rng.choice("klmn"),rng.randint(1,9),rng.choice(["none","debit","outbox"]),source,target))
 generated.append({"balances":{"a":i+10,"b":i,"c":5},"payments":ops})
SPEC={"number":50,"slug":"payment-service-integration","title":"Compose a bounded reliable payment service","difficulty":"Hard","time":45,"prerequisites":"Atomic transfers, idempotency payloads, and transactional outbox records.",
"learn":"A reliable payment boundary combines rules that are easy to implement incorrectly in isolation. The idempotency key identifies the complete request payload, including both accounts and the amount. A successful payment changes two balances, records that key, and creates an event as one logical commit. Replays return before checking the current balance because the original payment already happened. Failed attempts retain no key, so they can retry after recovery. This bounded exercise stages changes in memory and publishes them only after all fault points pass. It is a deterministic event trace, not an actual parallel, thread, or network test. Production storage would need a real durable transaction.",
"task":('**Input:** `data` has:\n'
    '- `balances`: maps existing account IDs to nonnegative integer balances.\n'
    '- `payments`: a list of `{"key": ..., "from": ..., "to": ..., "amount": ..., "fail": ...}`. The two accounts exist and differ. `amount` is positive. `fail` is `"none"`, `"debit"` (a fault after the debit is staged), or `"outbox"` (a fault after the event is prepared).\n'
    '\n'
    '**Rules:** for each payment:\n'
    '1. **Key already committed:** the same `(from, to, amount)` → `"replay"`. Any difference → `"conflict"`. These checks ignore `fail` and the current funds.\n'
    '2. **New key, and the source has less than `amount`:** return `"insufficient"`. Do not store the key.\n'
    '3. **New key otherwise:** stage the debit, the credit, the key, and the outbox event as one atomic operation.\n'
    '   - Either fault → return `"failed"`. No committed state changes, and the key is not reserved.\n'
    '   - No fault → commit and return `"ok"`.\n'
    '\n'
    '**Return** `{"results": [...], "balances": {...}, "events": [[key, from, to, amount], ...]}`. Events are in successful commit order. No network delivery is needed.'),"constraints":["0–100 accounts and 0–300 payments. IDs and keys are nonempty ASCII strings.","Initial balances are 0–1000000 and amounts are 1–1000000.","Implement only this bounded state model; no HTTP server, database setup, or background worker is required."],"hints":["Check prior committed payloads before validating a new payment.","Keep staged state separate until every injected failure point has passed."],"starter":"def solve(data: dict) -> dict:\n    # Compose idempotency, atomic balances, and an ordered outbox.\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){Map<String,Object> balances=new TreeMap<>(obj(d.get("balances")));Map<String,List<Object>> committed=new HashMap<>();List<Object> events=new ArrayList<>(),results=new ArrayList<>();for(Object raw:arr(d.get("payments"))){Map<String,Object> op=obj(raw);String key=s(op.get("key")),source=s(op.get("from")),target=s(op.get("to"));long amount=lng(op.get("amount"));List<Object> payload=list(source,target,amount);if(committed.containsKey(key)){results.add(committed.get(key).equals(payload)?"replay":"conflict");continue;}long before=lng(balances.get(source));if(before<amount){results.add("insufficient");continue;}if(!s(op.get("fail")).equals("none")){results.add("failed");continue;}balances.put(source,before-amount);balances.put(target,lng(balances.get(target))+amount);committed.put(key,payload);events.add(list(key,source,target,amount));results.add("ok");}return map("results",results,"balances",balances,"events",events);}''',
"approach":"Validate the committed key first. For a new payment, copy balances, stage both writes and the event, then publish all state only after fault checks. For A accounts and P payments, this model costs O(P × A) time and O(A + P) storage. Real services must replace staged memory with durable transactions and add authorization, observability, concurrent conflict handling, and outbox delivery. Completing this exercise does not certify production or interview readiness.","cases":CASES,"generated":generated,"mutations":[{"name":"stages debit in live committed balances","old":"staged = dict(balances)","new":"staged = balances"}],"sources":["https://www.sqlite.org/lang_transaction.html","https://docs.python.org/3.11/library/copy.html"]}
