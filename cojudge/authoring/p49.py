import random
REFERENCE='''def solve(data: dict) -> dict:
    available = data["stock"]
    reservations = {}
    results = []
    for op in data["ops"]:
        now = op["at"]
        for item in reservations.values():
            if item["state"] == "held" and item["expires"] <= now:
                item["state"] = "expired"
                available += item["qty"]
        key = op["id"]
        existing = reservations.get(key)
        if op["op"] == "reserve":
            if existing is not None:
                same = existing["qty"] == op["qty"] and existing["ttl"] == op["ttl"]
                results.append(existing["state"] if same else "conflict")
            elif op["qty"] > available:
                results.append("insufficient")
            else:
                available -= op["qty"]
                reservations[key] = {"qty": op["qty"], "ttl": op["ttl"], "expires": now + op["ttl"], "state": "held"}
                results.append("held")
        elif existing is None:
            results.append("missing")
        else:
            if existing["state"] == "held":
                if op["op"] == "confirm":
                    existing["state"] = "confirmed"
                else:
                    existing["state"] = "released"
                    available += existing["qty"]
            results.append(existing["state"])
    return {"results": results, "available": available, "reservations": [[key, reservations[key]["state"]] for key in sorted(reservations)]}
'''
def r(at=0,id="a",qty=2,ttl=5):return {"op":"reserve","at":at,"id":id,"qty":qty,"ttl":ttl}
def confirm(at=0,id="a"):return {"op":"confirm","at":at,"id":id}
def release(at=0,id="a"):return {"op":"release","at":at,"id":id}
def c(stock,ops,results,available,states,label):return {"input":{"stock":stock,"ops":ops},"expected":{"results":results,"available":available,"reservations":states},"label":label}
CASES=[c(5,[r(),confirm(4)],["held","confirmed"],3,[["a","confirmed"]],"confirm before expiry consumes stock"),c(5,[r(),confirm(5)],["held","expired"],5,[["a","expired"]],"confirmation at expiry is too late"),c(5,[r(),release(1),release(2)],["held","released","released"],5,[["a","released"]],"release restores stock only once"),c(0,[],[],0,[],"empty stock and trace"),c(1,[r()],["insufficient"],1,[],"insufficient request reserves no ID"),c(2,[r()],["held"],0,[["a","held"]],"reserve exact remaining stock"),c(5,[confirm(),release()],["missing","missing"],5,[],"unknown ID"),c(5,[r(),r(4),confirm(5)],["held","held","expired"],5,[["a","expired"]],"replay does not extend deadline"),c(5,[r(),r(1,qty=3),r(2,ttl=6)],["held","conflict","conflict"],3,[["a","held"]],"payload conflict covers quantity and TTL"),c(5,[r(),confirm(1),confirm(2),release(10)],["held","confirmed","confirmed","confirmed"],3,[["a","confirmed"]],"confirmed reservation never expires or refunds"),c(5,[r(),release(1),confirm(2),r(3)],["held","released","released","released"],5,[["a","released"]],"terminal release blocks reuse"),c(2,[r(),r(5,"b")],["held","held"],0,[["a","expired"],["b","held"]],"expiry frees stock before next reserve"),c(2,[r(),r(1,"b"),release(2),r(3,"b")],["held","insufficient","released","held"],0,[["a","released"],["b","held"]],"insufficient attempt may retry after release"),c(5,[r(),r(5),release(6)],["held","expired","expired"],5,[["a","expired"]],"expired ID remains terminal"),c(5,[r(),r(1,"b",3),confirm(5,"b")],["held","held","confirmed"],2,[["a","expired"],["b","confirmed"]],"expiry cleanup isolates reservations")]
rng=random.Random(49)
generated=[]
for i in range(24):
 now=0;ops=[]
 for j in range(25):
  now+=rng.randrange(3);id=rng.choice("abcd");kind=rng.randrange(3);ops.append(r(now,id,rng.randint(1,5),rng.randint(1,6)) if kind==0 else confirm(now,id) if kind==1 else release(now,id))
 generated.append({"stock":i,"ops":ops})
SPEC={"number":49,"slug":"reservation-expiry","title":"Expire reservations and make transitions idempotent","difficulty":"Hard","time":40,"prerequisites":"State machines, inventory invariants, and idempotency.",
"learn":"A reservation temporarily removes stock from the available pool. Confirmation makes that allocation permanent. Release or expiry returns the held stock, but must do so only once. Terminal states prevent repeated commands from creating extra stock. An idempotent reserve retry also must not extend the original deadline. Here each accepted reservation retains its ID, payload, and final state. Insufficient attempts create no record and may retry later. Expire held records before processing every command, including commands for another ID. This makes the exact expiry boundary explicit. The task is a deterministic event trace, not an actual parallel, thread, or network test.",
"scenario": ('A ticket site holds seats in a cart for a short time. If the customer does not pay before the hold expires, the seats go back on sale. Clients can send a request again, so a repeated request must be safe.'),
 "example_notes": ['Hold 2 seats, then confirm at 4, before the expiry at 5.', 'At 5 the hold expires. The confirm returns `expired`, and the seats come back.', 'A second release returns `released` again. The seats come back only once.'],
 "task":('**Input:** `data` has:\n'
    '- `stock`: the starting integer stock.\n'
    '- `ops`: a list of operations. Each has `at` (times never decrease), `id`, and `op`.\n'
    '\n'
    '**Rules:** before each operation, every `held` reservation with `expires` at or before `at` changes to `expired`, and its quantity goes back to the stock.\n'
    '- `reserve` (also has positive `qty` and `ttl`):\n'
    '  - Existing ID: return its current state if `qty` and `ttl` match, otherwise `"conflict"`. Never extend the expiry.\n'
    '  - New ID and the stock is less than `qty`: return `"insufficient"` and store no record.\n'
    '  - New ID otherwise: subtract `qty` from the stock, set `expires = at + ttl`, store the state `held`, and return `"held"`.\n'
    '- `confirm`: change `held` to `confirmed`. The stock does not come back.\n'
    '- `release`: change `held` to `released`. The quantity goes back to the stock once.\n'
    '- `confirm` and `release` return the current state after the operation, or `"missing"` for an unknown ID.\n'
    '- `confirmed`, `released`, and `expired` never change.\n'
    '\n'
    '**Return** `{"results": [...], "available": int, "reservations": [[id, state], ...]}`, with the reservations sorted by ASCII ID.'),"constraints":["Stock is 0–1000000. There are 0–300 operations.","Times are 0–1000000; qty and ttl are 1–1000000. IDs are nonempty ASCII strings."],"hints":["Only the held state can release stock.","Retain terminal records so duplicate commands remain idempotent."],"starter":"def solve(data: dict) -> dict:\n    # Track available stock and reservation state by ID.\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){long available=lng(d.get("stock"));Map<String,Map<String,Object>> records=new TreeMap<>();List<Object> results=new ArrayList<>();for(Object raw:arr(d.get("ops"))){Map<String,Object> op=obj(raw);long now=lng(op.get("at"));for(Map<String,Object> item:records.values())if(s(item.get("state")).equals("held")&&lng(item.get("expires"))<=now){item.put("state","expired");available+=lng(item.get("qty"));}String id=s(op.get("id")),kind=s(op.get("op"));Map<String,Object> item=records.get(id);if(kind.equals("reserve")){if(item!=null){boolean same=lng(item.get("qty"))==lng(op.get("qty"))&&lng(item.get("ttl"))==lng(op.get("ttl"));results.add(same?item.get("state"):"conflict");}else if(lng(op.get("qty"))>available)results.add("insufficient");else{available-=lng(op.get("qty"));records.put(id,map("qty",op.get("qty"),"ttl",op.get("ttl"),"expires",now+lng(op.get("ttl")),"state","held"));results.add("held");}}else if(item==null)results.add("missing");else{if(s(item.get("state")).equals("held")){if(kind.equals("confirm"))item.put("state","confirmed");else{item.put("state","released");available+=lng(item.get("qty"));}}results.add(item.get("state"));}}List<Object> states=new ArrayList<>();for(String id:records.keySet())states.add(list(id,records.get(id).get("state")));return map("results",results,"available",available,"reservations",states);}''',
"approach":"Store each reservation's immutable payload, expiry, and state. Expire held records before commands, and allow stock returns only from held. Scanning gives O(O × R) time and O(R + O) space. A real inventory service needs atomic storage transitions, clock policy, and protection against concurrent overselling.","cases":CASES,"generated":generated,"mutations":[{"name":"confirms a hold at its expiration boundary","old":"item[\"expires\"] <= now","new":"item[\"expires\"] < now"}],"sources":["https://docs.python.org/3.11/library/enum.html","https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict"]}
