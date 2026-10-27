import random
REFERENCE='''def solve(data: dict) -> dict:
    replicas = {r["id"]: (r["version"], r["value"]) for r in data["replicas"]}
    results = []
    for op in data["ops"]:
        if op["op"] == "publish":
            previous = replicas[op["id"]][0]
            if op["version"] < previous:
                results.append("stale")
            elif op["version"] == previous:
                results.append("unchanged")
            else:
                replicas[op["id"]] = (op["version"], op["value"])
                results.append("applied")
        else:
            eligible = [key for key, (version, _) in replicas.items() if version >= op["min_version"]]
            if not eligible:
                results.append(None)
            else:
                key = min(eligible, key=lambda k: (-replicas[k][0], k))
                version, value = replicas[key]
                results.append({"id": key, "version": version, "value": value})
    return {"results": results, "replicas": [[key, *replicas[key]] for key in sorted(replicas)]}
'''
def rep(id="a",v=1):return {"id":id,"version":v,"value":v*10}
def read(v=0):return {"op":"read","min_version":v}
def pub(id="a",v=2):return {"op":"publish","id":id,"version":v,"value":v*10}
def c(replicas,ops,results,end,label):return {"input":{"replicas":replicas,"ops":ops},"expected":{"results":results,"replicas":end},"label":label}
CASES=[c([rep("a",1),rep("b",3)],[read(2)],[rep("b",3)],[["a",1,10],["b",3,30]],"choose freshest eligible replica"),c([rep("a",1)],[read(2)],[None],[["a",1,10]],"stale replica cannot satisfy read token"),c([rep("b",2),rep("a",2)],[read(2)],[rep("a",2)],[["a",2,20],["b",2,20]],"equal version tie uses ASCII ID"),c([],[],[],[],"no replicas or requests"),c([],[read()],[None],[],"empty replica pool"),c([rep("a",0)],[read()],[rep("a",0)],[["a",0,0]],"zero version and zero value"),c([rep()],[pub(),read(2)],["applied",rep("a",2)],[["a",2,20]],"replication catches up"),c([rep("a",3)],[pub(v=2),read(3)],["stale",rep("a",3)],[["a",3,30]],"out-of-order publication cannot regress"),c([rep()],[pub(v=1)],["unchanged"],[["a",1,10]],"duplicate publication"),c([rep()],[read(2),pub(v=2),read(2)],[None,"applied",rep("a",2)],[["a",2,20]],"retry after catch-up"),c([rep("a",3),rep("b",1)],[pub("b",4),read(1)],["applied",rep("b",4)],[["a",3,30],["b",4,40]],"freshest source changes"),c([rep()],[pub(v=5),pub(v=2),pub(v=5),read(6)],["applied","stale","unchanged",None],[["a",5,50]],"read floor can exceed all known versions")]
rng=random.Random(48)
SPEC={"number":48,"slug":"replica-version-reads","title":"Preserve read-your-writes with version floors","difficulty":"Medium","time":30,"prerequisites":"Version numbers, replication lag, and deterministic selection.",
"learn":"Replicas can lag behind a completed write. A client can carry the version of its last write as a minimum acceptable version for later reads. A replica below that floor must not answer the read, even if it is reachable. If none qualifies, the caller must wait or use another source. This exercise selects the freshest eligible replica and uses its ID to break ties. Replication updates can also arrive out of order, so a replica must never replace a newer version with an older one. All equal versions represent the same value here. This is a deterministic event trace, not an actual parallel, thread, or network test.",
"scenario": ("A database has several replicas that can lag behind. After a user saves data, the app gets a write token (a version). The user's next read must go to a replica that has at least that version, so the user sees their own change."),
 "example_notes": ['Only `b` has a version of at least 2.', 'No replica has version 2 yet, so the result is `null`.', '`a` and `b` both have version 2. The smaller ID, `a`, wins.'],
 "task":('**Input:** `data` has:\n'
    '- `replicas`: a list of `{"id": ..., "version": ..., "value": ...}`, with unique IDs.\n'
    '- `ops`: a list of operations:\n'
    '  - `publish`: an existing `id`, a `version`, and a `value`.\n'
    "  - `read`: a `min_version`, which is the client's write token.\n"
    '\n'
    'In all input records and publications, equal versions always have equal values.\n'
    '\n'
    '**Rules**\n'
    '- `publish`: a higher version than the replica\'s → update the replica and return `"applied"`. A lower version → ignore it and return `"stale"`. An equal version → return `"unchanged"`.\n'
    '- `read`: eligible replicas have a version of at least `min_version`. Return `{"id": ..., "version": ..., "value": ...}` of the replica with the highest version. On a tie, use the smallest ASCII ID. Return `null` if no replica is eligible. Use only the supplied `min_version`; do not infer it from other reads.\n'
    '\n'
    '**Return** `{"results": [...], "replicas": [[id, version, value], ...]}`, with the final replicas sorted by ID.'),"constraints":["0–100 replicas and 0–300 operations. Publish IDs always exist.","IDs are nonempty ASCII strings; versions and min_version are 0–1000000; values are integers from -1000000 to 1000000."],"hints":["Filter by the client's version floor before selecting a replica.","Order candidates by descending version, then ascending ID."],"starter":"def solve(data: dict) -> dict:\n    # Model replica updates and reads with an explicit version floor.\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){Map<String,long[]> replicas=new TreeMap<>();for(Object raw:arr(d.get("replicas"))){Map<String,Object> r=obj(raw);replicas.put(s(r.get("id")),new long[]{lng(r.get("version")),lng(r.get("value"))});}List<Object> results=new ArrayList<>();for(Object raw:arr(d.get("ops"))){Map<String,Object> op=obj(raw);if(s(op.get("op")).equals("publish")){String id=s(op.get("id"));long version=lng(op.get("version")),old=replicas.get(id)[0];if(version<old)results.add("stale");else if(version==old)results.add("unchanged");else{replicas.put(id,new long[]{version,lng(op.get("value"))});results.add("applied");}}else{String chosen=null;long highest=-1;for(String id:replicas.keySet()){long version=replicas.get(id)[0];if(version>=lng(op.get("min_version"))&&version>highest){chosen=id;highest=version;}}results.add(chosen==null?null:map("id",chosen,"version",highest,"value",replicas.get(chosen)[1]));}}List<Object> rows=new ArrayList<>();for(String id:replicas.keySet())rows.add(list(id,replicas.get(id)[0],replicas.get(id)[1]));return map("results",results,"replicas",rows);}''',
"approach":"Keep the latest state per replica and scan eligible replicas for each read. Time is O(R × O + R log R), and space is O(R + O). A real read-your-writes protocol must carry trustworthy version tokens, handle unavailable replicas, and define where a fallback read goes. This model has one global version sequence.","cases":CASES,"generated":[{"replicas":[rep("a",i),rep("b",i+1),rep("c",0)],"ops":[read(rng.randrange(i+8)) if j%2==0 else pub(rng.choice("abc"),rng.randrange(i+8)) for j in range(25)]} for i in range(24)],"mutations":[{"name":"allows replica one version below client token","old":"version >= op[\"min_version\"]","new":"version >= op[\"min_version\"] - 1"}],"sources":["https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels"]}
