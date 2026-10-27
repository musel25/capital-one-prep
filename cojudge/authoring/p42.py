import random
REFERENCE='''from collections import OrderedDict

def solve(data: dict) -> dict:
    cache = OrderedDict()
    results = []
    for op in data["ops"]:
        key = op["key"]
        if op["op"] == "put":
            cache[key] = op["value"]
            cache.move_to_end(key)
            evicted = None
            if len(cache) > data["capacity"]:
                evicted, _ = cache.popitem(last=False)
            results.append(evicted)
        elif op["op"] == "get":
            if key in cache:
                results.append(cache[key])
                cache.move_to_end(key)
            else:
                results.append(None)
        else:
            results.append(key in cache)
            cache.pop(key, None)
    return {"results": results, "entries": [[key, value] for key, value in cache.items()]}
'''
def p(k="a",v=1):return {"op":"put","key":k,"value":v}
def g(k="a"):return {"op":"get","key":k}
def x(k="a"):return {"op":"delete","key":k}
def c(cap,ops,results,entries,label):return {"input":{"capacity":cap,"ops":ops},"expected":{"results":results,"entries":entries},"label":label}
CASES=[c(2,[p(),p("b",2),p("c",3)],[None,None,"a"],[["b",2],["c",3]],"evict oldest use"),c(2,[p(),p("b",2),g(),p("c",3)],[None,None,1,"b"],[["a",1],["c",3]],"read refreshes recency"),c(2,[p(),p("b",2),p("a",9)],[None,None,None],[["b",2],["a",9]],"overwrite refreshes recency"),c(0,[],[],[],"empty zero capacity"),c(0,[p(),g()],["a",None],[],"zero capacity evicts inserted key"),c(1,[p(),p("b",2),g()],[None,"a",None],[["b",2]],"capacity one"),c(2,[g(),x()],[None,False],[],"missing read and delete"),c(2,[p(v=0),g()],[None,0],[["a",0]],"zero is present"),c(2,[p(),p("b",2),g("z"),p("c",3)],[None,None,None,"a"],[["b",2],["c",3]],"miss does not change recency"),c(2,[p(),x(),x()],[None,True,False],[],"delete is idempotent"),c(2,[p(),p("b",2),x(),p("c",3)],[None,None,True,None],[["b",2],["c",3]],"delete frees capacity"),c(1,[p(),p(v=2),p(v=3)],[None,None,None],[["a",3]],"repeated overwrite does not evict"),c(3,[p("c",3),p("b",2),p(),g("c")],[None,None,None,3],[["b",2],["a",1],["c",3]],"order is recency rather than key order")]
rng=random.Random(42)
SPEC={"number":42,"slug":"bounded-lru-cache","title":"Build a capacity-bounded LRU cache","difficulty":"Medium","time":30,"prerequisites":"Dictionaries, ordered collections, and cache misses.",
"learn":"A least-recently-used cache evicts the entry whose last successful use is oldest. A successful read counts as use. In this contract, an insert or overwrite also counts as use. A missing read does not change the order. Python's OrderedDict can move a key to the newest end and remove a key from the oldest end. This keeps the value and recency order in one structure. Capacity is a count of entries, not a byte limit. Capacity zero is still valid: every inserted key is immediately evicted. This exercise is a deterministic event trace, not an actual parallel, thread, or network test.",
"scenario": ('An API gateway keeps a small in-memory cache of user profiles. When the cache is full, it removes the profile that was used least recently (LRU).'),
 "example_notes": ['Adding `c` to a full cache evicts `a`, the least recent key.', 'The get makes `a` recent, so `b` is evicted instead.', 'Overwriting `a` makes it the most recent. Nothing is evicted.'],
 "task":('**Input:** `data` has:\n'
    '- `capacity`: the maximum number of entries.\n'
    '- `ops`: a list of `put` (`key`, integer `value`), `get` (`key`), or `delete` (`key`).\n'
    '\n'
    '**Rules**\n'
    '- `put`: insert or overwrite, and make the key the most recent. If the cache is now over capacity, evict the least recent key. The result is the evicted key, or `null`.\n'
    '- `get`: return the value and make the key the most recent. If the key is absent, return `null` and change nothing.\n'
    '- `delete`: remove the key. Return `true` if it existed, otherwise `false`.\n'
    '\n'
    '**Return** `{"results": [...], "entries": [[key, value], ...]}`. List the final entries from least recent to most recent.'),
"constraints":["Capacity is 0–100; there are 0–300 operations.","Keys are nonempty ASCII strings. Values are integers from -1000000 to 1000000."],"hints":["Keep one end as least recent and the other as most recent.","Both successful reads and overwrites must move the key."],"starter":"def solve(data: dict) -> dict:\n    # Return results and final entries in LRU-to-MRU order.\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){Map<String,Object> values=new HashMap<>();List<String> order=new ArrayList<>();List<Object> results=new ArrayList<>();int capacity=n(d.get("capacity"));for(Object raw:arr(d.get("ops"))){Map<String,Object> op=obj(raw);String key=s(op.get("key")),kind=s(op.get("op"));if(kind.equals("put")){values.put(key,op.get("value"));order.remove(key);order.add(key);String evicted=null;if(order.size()>capacity){evicted=order.remove(0);values.remove(evicted);}results.add(evicted);}else if(kind.equals("get")){if(values.containsKey(key)){results.add(values.get(key));order.remove(key);order.add(key);}else results.add(null);}else{results.add(values.containsKey(key));values.remove(key);order.remove(key);}}List<Object> entries=new ArrayList<>();for(String key:order)entries.add(list(key,values.get(key)));return map("results",results,"entries",entries);}''',
"approach":"Use OrderedDict to keep least recent entries first. Each operation takes expected O(1), and final output takes O(K). Space is O(K + O) including results. The Java marker uses an independent list model. Real caches also need synchronization, memory accounting, and explicit expiration rules.","cases":CASES,"generated":[{"capacity":i%6,"ops":[p(rng.choice("abcde"),rng.randint(-9,9)) if j%3==0 else g(rng.choice("abcde")) if j%3==1 else x(rng.choice("abcde")) for j in range(i+15)]} for i in range(24)],"mutations":[{"name":"evicts most recent entry","old":"cache.popitem(last=False)","new":"cache.popitem(last=True)"}],"sources":["https://docs.python.org/3.11/library/collections.html#collections.OrderedDict"]}
