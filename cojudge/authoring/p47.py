import random
REFERENCE='''from bisect import bisect_left, insort

def solve(data: dict) -> dict:
    points = sorted(node["hash"] for node in data["nodes"])
    owners = {node["hash"]: node["id"] for node in data["nodes"]}
    by_id = {node["id"]: node["hash"] for node in data["nodes"]}
    results = []
    for op in data["ops"]:
        if op["op"] == "lookup":
            if not points:
                results.append(None)
            else:
                index = bisect_left(points, op["hash"])
                results.append(owners[points[index % len(points)]])
        elif op["op"] == "add":
            insort(points, op["hash"])
            owners[op["hash"]] = op["id"]
            by_id[op["id"]] = op["hash"]
            results.append("added")
        else:
            key = op["id"]
            results.append(key in by_id)
            if key in by_id:
                point = by_id.pop(key)
                points.remove(point)
                del owners[point]
    return {"results": results, "ring": [[point, owners[point]] for point in points]}
'''
def node(id="a",h=100):return {"id":id,"hash":h}
def look(h):return {"op":"lookup","hash":h}
def add(id,h):return {"op":"add","id":id,"hash":h}
def rem(id="a"):return {"op":"remove","id":id}
def c(nodes,ops,results,ring,label):return {"input":{"nodes":nodes,"ops":ops},"expected":{"results":results,"ring":ring},"label":label}
CASES=[c([node(),node("b",500)],[look(101)],["b"],[[100,"a"],[500,"b"]],"clockwise successor"),c([node(),node("b",500)],[look(100)],["a"],[[100,"a"],[500,"b"]],"exact hash belongs to that node"),c([node(),node("b",500)],[look(999)],["a"],[[100,"a"],[500,"b"]],"wrap past final point"),c([],[],[],[],"empty ring"),c([],[look(0)],[None],[],"empty lookup"),c([node()],[look(0),look(100),look(999)],["a","a","a"],[[100,"a"]],"single node owns whole ring"),c([node("b",500),node()],[look(0)],["a"],[[100,"a"],[500,"b"]],"input need not be sorted"),c([node(),node("b",500)],[add("c",300),look(200),look(400)],["added","c","b"],[[100,"a"],[300,"c"],[500,"b"]],"add splits one interval"),c([node(),node("b",500)],[rem("b"),look(400)],[True,"a"],[[100,"a"]],"remove transfers interval"),c([node()],[rem(),look(0),rem()],[True,None,False],[],"remove final node and repeat"),c([],[add("z",999),add("a",0),look(0),look(1),look(999)],["added","added","a","z","z"],[[0,"a"],[999,"z"]],"ring endpoints"),c([node()],[rem("missing"),rem(),add("a",700),look(100)],[False,True,"added","a"],[[700,"a"]],"ID can be reused after removal")]
rng=random.Random(47)
SPEC={"number":47,"slug":"consistent-hash-ring","title":"Route requests around a consistent hash ring","difficulty":"Hard","time":30,"prerequisites":"Sorted lists, binary search, and dictionaries.",
"learn":"A hash ring assigns each request to the first node at or after its hash, moving in increasing hash order. If no node remains in that direction, the search wraps to the first node. An exact hash match belongs to that node. Adding a node changes the interval immediately before it; removing a node hands its interval to its successor. This exercise supplies deterministic integer hashes so that language hash randomization cannot change the answers. Python's bisect_left finds the required insertion position, including exact matches. The model uses one point per node. This is a deterministic event trace, not an actual parallel, thread, or network test.",
"scenario": ('A cache cluster spreads keys over servers with a hash ring. A key goes to the first server at or after its hash, and wraps around at the end of the ring. Servers can join and leave.'),
 "example_notes": ['Hash 101 goes to the next server, at 500: `b`.', 'Hash 100 is exactly at the point of `a`.', 'Hash 999 is after the last server, so it wraps around to `a`.'],
 "task":('**Input:** `data` has:\n'
    '- `nodes`: a list of `{"id": ..., "hash": ...}`, with unique IDs and hashes. Hashes are points on a ring from 0 to 999.\n'
    '- `ops`: a list of operations. Process them in order.\n'
    '\n'
    '**Rules**\n'
    '- `lookup` (`hash`): return the ID at the smallest active hash that is greater than or equal to `hash`. If there is none, wrap around to the smallest hash. Return `null` if the ring is empty.\n'
    '- `add` (`id`, `hash`, both currently unused): add the node and return `"added"`.\n'
    '- `remove` (`id`): remove the node and return `true`, or return `false` if it is absent.\n'
    '\n'
    "The input supplies the hashes. Do not call Python's `hash` function.\n"
    '\n'
    '**Return** `{"results": [...], "ring": [[hash, id], ...]}`, with the final ring sorted by hash.'),"constraints":["0–100 initial nodes and 0–300 operations. Active hashes and IDs remain unique.","IDs are nonempty ASCII strings. Removed IDs and hash points may later be reused."],"hints":["Use the left insertion position so equality selects the matching node.","An insertion index equal to the ring size wraps to index zero."],"starter":"from bisect import bisect_left, insort\n\ndef solve(data: dict) -> dict:\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){TreeMap<Integer,String> ring=new TreeMap<>();Map<String,Integer> ids=new HashMap<>();for(Object raw:arr(d.get("nodes"))){Map<String,Object> node=obj(raw);ring.put(n(node.get("hash")),s(node.get("id")));ids.put(s(node.get("id")),n(node.get("hash")));}List<Object> results=new ArrayList<>();for(Object raw:arr(d.get("ops"))){Map<String,Object> op=obj(raw);String kind=s(op.get("op"));if(kind.equals("lookup")){if(ring.isEmpty())results.add(null);else{Integer key=ring.ceilingKey(n(op.get("hash")));results.add(ring.get(key==null?ring.firstKey():key));}}else if(kind.equals("add")){int point=n(op.get("hash"));String id=s(op.get("id"));ring.put(point,id);ids.put(id,point);results.add("added");}else{Integer point=ids.remove(s(op.get("id")));results.add(point!=null);if(point!=null)ring.remove(point);}}List<Object> finalRing=new ArrayList<>();for(Map.Entry<Integer,String> e:ring.entrySet())finalRing.add(list(e.getKey(),e.getValue()));return map("results",results,"ring",finalRing);}''',
"approach":"Keep sorted hash points and mappings between points and node IDs. Lookup is O(log N); list insert and removal are O(N). Space is O(N + O) including results. Real rings need a stable hash function, collision policy, virtual nodes, and migration controls. This output judge cannot certify binary-search complexity.","cases":CASES,"generated":[{"nodes":[node("a",i),node("b",400+i)],"ops":[look(i),look(400+i),look(999),add("c",200+i),look(100+i),rem("b"),look(900),rem("missing")]+[look(rng.randrange(1000)) for _ in range(12)]} for i in range(24)],"mutations":[{"name":"routes exact matches to the next node","old":"index = bisect_left(points, op[\"hash\"])","new":"index = bisect_left(points, op[\"hash\"] + 1)"}],"sources":["https://docs.python.org/3.11/library/bisect.html"]}
