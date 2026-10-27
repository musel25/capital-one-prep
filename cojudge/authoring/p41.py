import random
REFERENCE='''def solve(data: dict) -> dict:
    entries = {}
    results = []
    for op in data["ops"]:
        now = op["at"]
        for key in list(entries):
            if entries[key][1] <= now:
                del entries[key]
        key = op["key"]
        if op["op"] == "put":
            if op["ttl"] > 0:
                entries[key] = (op["value"], now + op["ttl"])
            else:
                entries.pop(key, None)
            results.append("stored")
        elif op["op"] == "get":
            results.append(entries[key][0] if key in entries else None)
        else:
            results.append(key in entries)
            entries.pop(key, None)
    return {"results": results, "keys": sorted(entries)}
'''
def p(at=0,key="a",value=7,ttl=5):return {"op":"put","at":at,"key":key,"value":value,"ttl":ttl}
def g(at=0,key="a"):return {"op":"get","at":at,"key":key}
def x(at=0,key="a"):return {"op":"invalidate","at":at,"key":key}
def c(ops,results,keys,label):return {"input":{"ops":ops},"expected":{"results":results,"keys":keys},"label":label}
CASES=[c([p(),g(4)],["stored",7],["a"],"read before expiration"),c([p(),g(5)],["stored",None],[],"exact expiration is a miss"),c([p(),x(1),g(2)],["stored",True,None],[],"explicit invalidation"),c([],[],[],"empty trace"),c([g()],[None],[],"missing key"),c([p(ttl=0),g()],["stored",None],[],"zero lifetime"),c([p(value=0),g()],["stored",0],["a"],"zero is a cached value"),c([p(),p(4,value=8,ttl=3),g(5),g(7)],["stored","stored",8,None],[],"replacement resets expiration"),c([p(),g(4),g(5)],["stored",7,None],[],"reads do not extend lifetime"),c([x(),x(1)],[False,False],[],"repeated missing invalidation"),c([p(),x(5)],["stored",False],[],"expired entry is already absent"),c([p(key="b"),p(key="a",ttl=1),g(1,"b")],["stored","stored",7],["b"],"cleanup removes other expired keys"),c([p(),p(1,ttl=0),g(1)],["stored","stored",None],[],"zero lifetime overwrites existing entry")]
rng=random.Random(41)
generated=[]
for i in range(24):
 now=i;ops=[]
 for j in range(20):
  now+=rng.randrange(3);key=rng.choice(["a","b","c"]);kind=rng.randrange(3)
  ops.append(p(now,key,rng.randrange(-3,8),rng.randrange(5)) if kind==0 else g(now,key) if kind==1 else x(now,key))
 generated.append({"ops":ops})
SPEC={"number":41,"slug":"ttl-cache-boundaries","title":"Expire and invalidate cache entries","difficulty":"Medium","time":25,"prerequisites":"Dictionaries and integer time arithmetic.",
"learn":"A time-to-live cache stores a value and its expiration time. If an entry is written at time t with lifetime d, its expiration is t + d. It is usable only while the current time is strictly less than that expiration. Reads do not extend this lifetime unless the contract explicitly says so. An overwrite replaces both the value and its expiration. Invalidation removes the entry immediately. Distinguish a missing key from a cached value such as zero. This exercise uses an integer clock supplied by each operation. It is a deterministic event trace, not an actual parallel, thread, or network test.",
"task":('**Input:** `data` has:\n'
    '- `ops`: a list of operations. Each has an integer time `at`. Times never decrease.\n'
    '\n'
    '**Rules:** before each operation, remove every entry whose expiration time is at or before `at`. Then:\n'
    '- `put` (`key`, integer `value`, `ttl`): replace the entry, set its expiration to `at + ttl`, and return `"stored"`. A `ttl` of 0 removes any old entry and stores nothing.\n'
    '- `get` (`key`): return the value, or `null` if there is no entry.\n'
    '- `invalidate` (`key`): remove the entry. Return `true` if an unexpired entry was removed, otherwise `false`.\n'
    '\n'
    '**Return** `{"results": [...], "keys": [...]}`: one result per operation, and the keys that remain after the last operation, in ASCII order. An empty `ops` list returns empty lists.'),
"constraints":["0–300 operations. at and ttl are 0–1000000.","Keys are nonempty ASCII strings; values are integers from -1000000 to 1000000."],"hints":["Expiration is an exclusive boundary.","Store value and expiration together; clean before every operation."],"starter":"def solve(data: dict) -> dict:\n    # data['ops'] is a deterministic event trace.\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){Map<String,long[]> cache=new TreeMap<>();List<Object> results=new ArrayList<>();for(Object raw:arr(d.get("ops"))){Map<String,Object> op=obj(raw);long now=lng(op.get("at"));cache.entrySet().removeIf(e->e.getValue()[1]<=now);String key=s(op.get("key")),kind=s(op.get("op"));if(kind.equals("put")){long ttl=lng(op.get("ttl"));if(ttl>0)cache.put(key,new long[]{lng(op.get("value")),now+ttl});else cache.remove(key);results.add("stored");}else if(kind.equals("get"))results.add(cache.containsKey(key)?cache.get(key)[0]:null);else{results.add(cache.containsKey(key));cache.remove(key);}}return map("results",results,"keys",new ArrayList<>(cache.keySet()));}''',
"approach":"Store each value with an absolute expiration and remove expired entries before processing. A simple scan costs O(O × K), where O is the number of operations and K is the maximum live key count; storage is O(K + O). A large cache can use a heap or lazy cleanup. Real services also need clock and concurrency policies.","cases":CASES,"generated":generated,"mutations":[{"name":"serves an entry at its expiration time","old":"entries[key][1] <= now","new":"entries[key][1] < now"}],"sources":["https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict"]}
