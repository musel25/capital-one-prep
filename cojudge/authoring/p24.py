"""Idempotency records protect retried writes."""
REF='''def solve(data):
    cache = {}
    transfers = []
    out = []
    for request in data["requests"]:
        key, body = request["key"], request["body"]
        if key in cache:
            saved_body, result = cache[key]
            if body != saved_body:
                out.append({"status": 409, "body": {"error": "key_conflict"}, "replayed": False})
            else:
                out.append({"status": 201, "body": dict(result), "replayed": True})
        else:
            result = {"id": len(transfers) + 1, "to": body["to"], "amount": body["amount"]}
            transfers.append(dict(result))
            cache[key] = (dict(body), dict(result))
            out.append({"status": 201, "body": dict(result), "replayed": False})
    return {"responses": out, "transfers": transfers}
'''
JAVA='''public Object solve(Map<String,Object> d){
    Map<String,Map<String,Object>> bodies=new HashMap<>(), results=new HashMap<>();List<Object> out=new ArrayList<>(), transfers=new ArrayList<>();
    for(Object v:arr(d.get("requests"))){Map<String,Object> r=obj(v),body=obj(r.get("body"));String key=s(r.get("key"));
        if(bodies.containsKey(key)){
            Map<String,Object> old=bodies.get(key);boolean same=s(old.get("to")).equals(s(body.get("to")))&&n(old.get("amount"))==n(body.get("amount"));
            if(same)out.add(map("status",201,"body",results.get(key),"replayed",true));
            else out.add(map("status",409,"body",map("error","key_conflict"),"replayed",false));
        }else{Map<String,Object> result=map("id",transfers.size()+1,"to",body.get("to"),"amount",body.get("amount"));bodies.put(key,body);results.put(key,result);transfers.add(result);out.add(map("status",201,"body",result,"replayed",false));}
    }return map("responses",out,"transfers",transfers);
}'''
def r(k,to="a",amount=10):return {"key":k,"body":{"to":to,"amount":amount}}
def transfer(i,to="a",amount=10):return {"id":i,"to":to,"amount":amount}
def ok(t,replay=False):return {"status":201,"body":t,"replayed":replay}
CONFLICT={"status":409,"body":{"error":"key_conflict"},"replayed":False}
def case(requests,responses,transfers,label):return {"input":{"requests":requests},"expected":{"responses":responses,"transfers":transfers},"label":label}
T=transfer(1); U=transfer(2)
CASES=[case([r("k"),r("k")],[ok(T),ok(T,True)],[T],"same key and body replay one transfer"),case([r("k"),r("k",amount=11)],[ok(T),CONFLICT],[T],"same key with changed amount conflicts"),case([r("k"),r("j")],[ok(T),ok(U)],[T,U],"different keys permit same body"),case([],[],[],"empty batch"),case([r("one",amount=1)],[ok(transfer(1,amount=1))],[transfer(1,amount=1)],"minimum amount"),case([r("one",amount=1000000)],[ok(transfer(1,amount=1000000))],[transfer(1,amount=1000000)],"maximum amount"),case([r("k"),r("k","b")],[ok(T),CONFLICT],[T],"recipient conflict"),case([r("k"),r("k","b"),r("k")],[ok(T),CONFLICT,ok(T,True)],[T],"conflict does not replace cache"),case([r("k"),r("k",amount=11),r("j")],[ok(T),CONFLICT,ok(U)],[T,U],"conflict does not consume id"),case([r("k")]*4,[ok(T)]+[ok(T,True)]*3,[T],"many retries"),case([r("K"),r("k")],[ok(T),ok(U)],[T,U],"keys are case sensitive"),case([r("a"),r("b","b",20),r("a")],[ok(T),ok(transfer(2,"b",20)),ok(T,True)],[T,transfer(2,"b",20)],"nonadjacent replay"),case([r("x"),{"key":"x","body":{"amount":10,"to":"a"}}],[ok(T),ok(T,True)],[T],"object field order does not matter")]
GENERATED=[{"requests":[r(f"k{j%4}",f"recipient{(j+i)%3}",(j*i)%17+1) for j in range(i+2)]} for i in range(16)]
SPEC={"number":24,"slug":"idempotency-conflicts","title":"Replay writes with idempotency keys","difficulty":"Medium","time":30,"prerequisites":"Problems 20–23; state, validation, and response snapshots.","learn":"A client can lose a response after the server completes a write. Retrying the write without a stable identifier can create a second effect. An idempotency key names one logical request. The service stores the original body and result for that key. A retry with the same body gets the stored result. A different body must not silently reuse the key. The cache and the write need one atomic outcome in a real service. Here all operations are sequential and all bodies are valid. The exercise focuses on replay, conflicts, and identifier allocation. Cache expiration and concurrent requests are outside its scope.","task":"`requests` contains `{key:string, body:{to:string, amount:int}}`. All requests are valid. Process them in order with an initially empty key cache. A new key creates one transfer with consecutive id starting at 1. Return `{status:201, body:{id,to,amount}, replayed:false}`. An existing key with the same recipient and amount returns its original body with status 201 and `replayed:true`. An existing key with a different body returns `{status:409, body:{error:\"key_conflict\"}, replayed:false}`. A conflict changes nothing and consumes no id. Compare body fields, not serialized key order. Keys are case sensitive. Return `{responses:[...], transfers:[...]}` with transfers in creation order. This is a local application policy for a deterministic API simulation.","constraints":["0–200 requests. Keys and recipients are nonempty ASCII strings of at most 40 characters.","Amounts are integers from 1 through 1000000; booleans are excluded.","Bodies contain exactly to and amount. Keys never expire during one call."],"hints":["Store the original body together with the successful result.","Allocate an id only after deciding the key is new."],"starter":"def solve(data: dict) -> dict:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"A dictionary maps each key to its body and result. A new entry appends exactly one transfer. Replays and conflicts do not mutate state. Expected time is O(q), with O(q) space for distinct keys and output. A production implementation needs durable atomic storage, a retention policy, and a defined scope for each key.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"replay a key even when the amount changed","old":"if body != saved_body:","new":"if body['to'] != saved_body['to']:"}],"sources":["https://docs.stripe.com/api/idempotent_requests"]}
