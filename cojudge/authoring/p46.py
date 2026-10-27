import random
REFERENCE='''def solve(data: dict) -> dict:
    dependencies = {job["id"]: set(job["depends"]) for job in data["jobs"]}
    pending = set(dependencies)
    completed = set()
    rounds = []
    while pending:
        ready = sorted(key for key in pending if dependencies[key] <= completed)
        if not ready:
            break
        selected = ready[:data["workers"]]
        rounds.append(selected)
        pending.difference_update(selected)
        completed.update(selected)
    return {"rounds": rounds, "blocked": sorted(pending), "has_cycle": bool(pending)}
'''
def j(id,depends=()):return {"id":id,"depends":list(depends)}
def c(jobs,workers,rounds,blocked,label):return {"input":{"jobs":jobs,"workers":workers},"expected":{"rounds":rounds,"blocked":blocked,"has_cycle":bool(blocked)},"label":label}
CASES=[c([j("a"),j("b",["a"]),j("c",["a"])],2,[["a"],["b","c"]],[],"dependencies finish before next round"),c([j("c"),j("b"),j("a")],2,[["a","b"],["c"]],[],"worker limit and ASCII tie break"),c([j("a",["b"]),j("b",["a"])],2,[],["a","b"],"cycle blocks both jobs"),c([],3,[],[],"empty graph"),c([j("a")],1,[["a"]],[],"single job"),c([j("a",["a"])],1,[],["a"],"self cycle"),c([j("a"),j("b",["a"]),j("c",["b"])],5,[["a"],["b"],["c"]],[],"chain cannot use spare workers"),c([j("a"),j("b"),j("c",["a","b"])],1,[["a"],["b"],["c"]],[],"join waits for all prerequisites"),c([j("a"),j("b",["a"]),j("c",["a"]),j("d",["b","c"])],2,[["a"],["b","c"],["d"]],[],"diamond dependency"),c([j("a"),j("b",["c"]),j("c",["b"]),j("d",["c"])],2,[["a"]],["b","c","d"],"cycle also blocks downstream job"),c([j("a"),j("b",["a"]),j("c")],1,[["a"],["b"],["c"]],[],"newly ready job can outrank waiting job"),c([j("a",["b"]),j("b",["a"]),j("c"),j("d",["c"])],2,[["c"],["d"]],["a","b"],"independent work completes beside cycle"),c([j("d",["a","b","c"]),j("c"),j("b"),j("a")],2,[["a","b"],["c"],["d"]],[],"unfinished prerequisite across rounds")]
rng=random.Random(46)
generated=[]
for i in range(24):
 ids=list("abcdefgh"[:i%7+2]);jobs=[]
 for id in ids:jobs.append(j(id,[other for other in ids if rng.randrange(5)==0]))
 generated.append({"jobs":jobs,"workers":i%4+1})
SPEC={"number":46,"slug":"dependency-job-rounds","title":"Schedule dependent jobs and detect blocked cycles","difficulty":"Hard","time":35,"prerequisites":"Sets, directed graphs, and dependency order.",
"learn":"A job is ready when every prerequisite has completed. A dependency scheduler can repeatedly select ready jobs, run a bounded batch, and then mark that batch complete. All jobs in this task take one round, so a job cannot start in the same round as its prerequisite. If unfinished jobs remain but none is ready, the remaining dependency graph contains a cycle. Some blocked jobs may only depend on a cycle and are not themselves part of it. Report all unfinished jobs separately from the cycle flag. A fixed tie rule makes results reproducible. This is a deterministic event trace model, not an actual parallel, thread, or network test.",
"task":('**Input:** `data` has:\n'
    '- `jobs`: a list of `{"id": string, "depends": [ids]}`. IDs are unique ASCII strings. `depends` lists distinct existing job IDs. Self-dependencies and cycles can occur.\n'
    '- `workers`: the maximum number of jobs per round.\n'
    '\n'
    '**Rules:** repeat rounds.\n'
    '1. At the start of a round, find every unfinished job whose dependencies all finished in earlier rounds.\n'
    '2. Select up to `workers` of these jobs, in ascending ASCII ID order. All selected jobs finish at the end of the round.\n'
    '3. Stop when all jobs are finished or no job is ready.\n'
    '\n'
    '**Return** `{"rounds": [[id, ...], ...], "blocked": [...], "has_cycle": bool}`\n'
    '- `blocked`: the unfinished jobs, sorted.\n'
    '- `has_cycle`: `true` exactly when some jobs are blocked. Do not claim that every blocked job is part of a cycle.'),"constraints":["0–100 jobs, at most 100 dependencies per job, and 1–20 workers.","Every dependency refers to a supplied job. Each job takes exactly one round and always succeeds."],"hints":["Compute the whole ready set before marking this round complete.","A stalled nonempty remainder proves a cycle when all dependency IDs exist."],"starter":"def solve(data: dict) -> dict:\n    # Build deterministic rounds and report unscheduled jobs.\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){Map<String,Set<String>> deps=new TreeMap<>();for(Object raw:arr(d.get("jobs"))){Map<String,Object> job=obj(raw);Set<String> set=new HashSet<>();for(Object x:arr(job.get("depends")))set.add(s(x));deps.put(s(job.get("id")),set);}Set<String> done=new HashSet<>();List<Object> rounds=new ArrayList<>();while(done.size()<deps.size()){List<Object> selected=new ArrayList<>();for(String id:deps.keySet())if(!done.contains(id)&&done.containsAll(deps.get(id))&&selected.size()<n(d.get("workers")))selected.add(id);if(selected.isEmpty())break;rounds.add(selected);for(Object id:selected)done.add(s(id));}List<Object> blocked=new ArrayList<>();for(String id:deps.keySet())if(!done.contains(id))blocked.add(id);return map("rounds",rounds,"blocked",blocked,"has_cycle",!blocked.isEmpty());}''',
"approach":"Scan unfinished jobs at each round and compare their dependency sets with completed jobs. Worst-case time is O(V × (V + E) + V² log V) for this small model; space is O(V + E). An indegree graph and ordered ready queue can scale better. Real schedulers also need failures, duration estimates, and resource limits.","cases":CASES,"generated":generated,"mutations":[{"name":"runs a job when only one prerequisite is done","old":"dependencies[key] <= completed","new":"(not dependencies[key] or bool(dependencies[key] & completed))"}],"sources":["https://docs.python.org/3.11/library/graphlib.html"]}
