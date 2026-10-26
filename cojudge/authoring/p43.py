import random
REFERENCE='''def solve(data: dict) -> dict:
    processed = set()
    total = data["total"]
    results = []
    for delivery in data["deliveries"]:
        key = delivery["id"]
        if key in processed:
            results.append("ack")
            continue
        if delivery["fail"] == "before":
            results.append("retry")
            continue
        total += delivery["amount"]
        processed.add(key)
        results.append("retry" if delivery["fail"] == "after" else "ack")
    return {"results": results, "total": total, "processed": sorted(processed)}
'''
def o(id="a",amount=2,fail="none"):return {"id":id,"amount":amount,"fail":fail}
def c(total,ops,status,end,ids,label):return {"input":{"total":total,"deliveries":ops},"expected":{"results":status,"total":end,"processed":ids},"label":label}
CASES=[c(0,[o(),o()],["ack","ack"],2,["a"],"duplicate delivery has one effect"),c(0,[o(fail="before"),o()],["retry","ack"],2,["a"],"failure before commit can retry"),c(0,[o(fail="after"),o()],["retry","ack"],2,["a"],"lost acknowledgement after commit"),c(7,[],[],7,[],"no deliveries"),c(0,[o(fail="before")],["retry"],0,[],"failed attempt is not processed"),c(0,[o(fail="after")],["retry"],2,["a"],"commit survives lost acknowledgement"),c(0,[o(),o(fail="before")],["ack","ack"],2,["a"],"dedup precedes fault"),c(0,[o(),o(fail="after")],["ack","ack"],2,["a"],"duplicate is acknowledged without work"),c(3,[o("b",2),o("a",2)],["ack","ack"],7,["a","b"],"equal amounts have distinct IDs"),c(0,[o(amount=0),o(amount=0)],["ack","ack"],0,["a"],"zero effect still records ID"),c(5,[o(amount=-3),o(amount=-3)],["ack","ack"],2,["a"],"signed delta applied once"),c(0,[o("a",2,"before"),o("b",4),o("a",2,"after"),o("b",4),o("a",2)],["retry","ack","retry","ack","ack"],6,["a","b"],"interleaved retries")]
rng=random.Random(43)
SPEC={"number":43,"slug":"message-deduplication","title":"Deduplicate at-least-once message delivery","difficulty":"Medium","time":25,"prerequisites":"Sets, idempotency, and transaction boundaries.",
"learn":"At-least-once delivery means a message can arrive more than once. A consumer should identify the logical message by its ID and record completed IDs with the business effect. These two changes form one logical commit in this model. If processing fails before commit, a retry must still apply the effect. If the acknowledgement is lost after commit, a retry must acknowledge the message without applying it again. Do not mark a message complete before its effect commits. This task supplies the failures directly. It is a deterministic event trace, not an actual parallel, thread, or network test, and it makes no claim of end-to-end exactly-once delivery.",
"task":"`total` is the initial integer total. `deliveries` contains `{id, amount, fail}`. All deliveries with the same ID have the same amount. If an ID is already processed, return `ack` with no effect, regardless of `fail`. For a new ID, `before` returns `retry` without committing. Otherwise atomically add `amount` and record the ID. Then `after` returns `retry` to model a lost acknowledgement; `none` returns `ack`. Return `{results: [...], total: integer, processed: [...]}` with processed IDs sorted in ASCII order. This is an in-memory model of a commit boundary.","constraints":["0–300 deliveries. IDs are nonempty ASCII strings.","total and amounts are integers from -1000000 to 1000000. fail is none, before, or after."],"hints":["An acknowledgement can fail after the effect is already durable in the model.","Only the before failure leaves the ID unprocessed."],"starter":"def solve(data: dict) -> dict:\n    # Model atomic effect + processed ID, then acknowledgement.\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){long total=lng(d.get("total"));Set<String> processed=new TreeSet<>();List<Object> results=new ArrayList<>();for(Object raw:arr(d.get("deliveries"))){Map<String,Object> op=obj(raw);String id=s(op.get("id")),fault=s(op.get("fail"));if(processed.contains(id))results.add("ack");else if(fault.equals("before"))results.add("retry");else{total+=lng(op.get("amount"));processed.add(id);results.add(fault.equals("after")?"retry":"ack");}}return map("results",results,"total",total,"processed",new ArrayList<>(processed));}''',
"approach":"Use a processed-ID set and apply the effect only on the first committed delivery. Processing is expected O(D), with O(P log P) for sorted output and O(P + D) space. In a real consumer, the effect and dedup record need shared durable transaction semantics; an in-memory set is not sufficient after restart.","cases":CASES,"generated":[{"total":i,"deliveries":[o(k,(ord(k)-97)*3-2,rng.choice(["none","before","after"])) for k in [rng.choice("abcde") for _ in range(25)]]} for i in range(24)],"mutations":[{"name":"forgets to record processed ID","old":"processed.add(key)","new":"pass  # missing dedup record"}],"sources":["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html"]}
