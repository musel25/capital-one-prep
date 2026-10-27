import random
REFERENCE='''def solve(data: dict) -> dict:
    state = "closed"
    failures = 0
    retry_at = None
    results = []
    for call in data["calls"]:
        now = call["at"]
        if state == "open" and now < retry_at:
            results.append({"mode": "blocked", "result": "blocked", "state": "open"})
            continue
        mode = "probe" if state == "open" else "closed"
        if call["ok"]:
            state, failures, retry_at = "closed", 0, None
            result = "success"
        else:
            failures += 1
            result = "failure"
            if mode == "probe" or failures >= data["threshold"]:
                state = "open"
                retry_at = now + data["cooldown"]
        results.append({"mode": mode, "result": result, "state": state})
    return {"results": results, "state": state, "failures": failures, "retry_at": retry_at}
'''
def o(at=0,ok=False):return {"at":at,"ok":ok}
def log(mode="closed",result="failure",state="closed"):return {"mode":mode,"result":result,"state":state}
def c(th,cd,calls,logs,state,fail,retry,label):return {"input":{"threshold":th,"cooldown":cd,"calls":calls},"expected":{"results":logs,"state":state,"failures":fail,"retry_at":retry},"label":label}
CASES=[c(2,5,[o(),o(1)],[log(),log(state="open")],"open",2,6,"consecutive failures open breaker"),c(1,5,[o(),o(4,True)],[log(state="open"),log("blocked","blocked","open")],"open",1,5,"open breaker ignores supplied outcome"),c(1,5,[o(),o(5,True)],[log(state="open"),log("probe","success","closed")],"closed",0,None,"probe succeeds at deadline"),c(2,5,[],[],"closed",0,None,"empty trace"),c(2,5,[o(ok=True)],[log(result="success")],"closed",0,None,"healthy call"),c(2,5,[o(),o(1,True),o(2)],[log(),log(result="success"),log()],"closed",1,None,"success clears consecutive failures"),c(1,5,[o(),o(5)],[log(state="open"),log("probe","failure","open")],"open",2,10,"failed probe starts new cooldown"),c(1,1,[o(),o(1),o(2,True)],[log(state="open"),log("probe","failure","open"),log("probe","success","closed")],"closed",0,None,"recovery after failed probe"),c(3,5,[o(),o(0),o(0)],[log(),log(),log(state="open")],"open",3,5,"equal timestamps preserve order"),c(1,5,[o(10),o(100,True)],[log(state="open"),log("probe","success","closed")],"closed",0,None,"late probe"),c(1,5,[o(),o(2),o(4)],[log(state="open"),log("blocked","blocked","open"),log("blocked","blocked","open")],"open",1,5,"blocked calls neither count nor extend"),c(2,3,[o(),o(1),o(4,True),o(5),o(6)],[log(),log(state="open"),log("probe","success","closed"),log(),log(state="open")],"open",2,9,"new failure streak after recovery")]
rng=random.Random(45)
generated=[]
for i in range(24):
 now=i;calls=[]
 for j in range(30):now+=rng.randrange(4);calls.append(o(now,rng.choice([True,False])))
 generated.append({"threshold":i%4+1,"cooldown":i%7+1,"calls":calls})
SPEC={"number":45,"slug":"circuit-breaker-state","title":"Trace a circuit breaker through recovery","difficulty":"Hard","time":35,"prerequisites":"State machines, consecutive counters, and time boundaries.",
"learn":"A circuit breaker stops repeated calls to a failing dependency. While closed, it allows calls and counts consecutive failures. Enough failures open the breaker for a cooldown period. During that period calls are blocked and do not reach the dependency. At the deadline, the next call is a half-open probe. A successful probe closes the breaker and resets failures. A failed probe opens it for a new cooldown. The half-open state is transient here because each allowed call completes immediately in the trace. This exercise uses supplied outcomes and integer times. It is a deterministic event trace, not an actual parallel, thread, or network test.",
"scenario": ('A payment service calls a fraud-check service. If the fraud service keeps failing, the payment service stops calling it for a cooldown period (open). Then it tries one test call (a probe) to see if the service recovered.'),
 "example_notes": ['Two failures reach the threshold of 2, so the breaker is open until 6.', 'The call at 4 is before `retry_at` 5, so it is blocked.', 'At 5 the probe succeeds, so the breaker closes.'],
 "task":('**Input:** `data` has:\n'
    '- `threshold`, `cooldown`: positive integers.\n'
    '- `calls`: a list of `{"at": int, "ok": bool}`. Times never decrease.\n'
    '\n'
    '**Rules:** the breaker starts `closed` with 0 failures. Opening the breaker sets `retry_at = at + cooldown`.\n'
    '- **Closed:** a success resets failures to 0. A failure adds 1 to failures, and the breaker opens when failures reach `threshold`.\n'
    '- **Open and `at < retry_at`:** block the call and ignore its outcome. A blocked call changes nothing.\n'
    '- **Open and `at` ≥ `retry_at`:** allow one half-open probe. A success closes the breaker and resets failures to 0. A failure adds 1 to failures and opens the breaker for a new cooldown, whatever the threshold.\n'
    '\n'
    '**Return** `{"results": [...], "state": ..., "failures": ..., "retry_at": ...}`\n'
    '- `results`: one `{"mode": ..., "result": ..., "state": ...}` per call. `mode` is `closed`, `probe`, or `blocked`. `result` is `success`, `failure`, or `blocked`. `state` is the state after the call.\n'
    '- `retry_at` is `null` when the final state is closed.'),"constraints":["0–300 calls; threshold is 1–100, cooldown is 1–1000000, at is 0–1000000.","No call remains in flight between trace entries."],"hints":["Check the open deadline before reading the outcome.","A failed probe opens immediately, even if the threshold is larger than one."],"starter":"def solve(data: dict) -> dict:\n    # Keep breaker state, consecutive failures, and retry deadline.\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){String state="closed";long failures=0;Long retry=null;List<Object> results=new ArrayList<>();for(Object raw:arr(d.get("calls"))){Map<String,Object> call=obj(raw);long now=lng(call.get("at"));if(state.equals("open")&&now<retry){results.add(map("mode","blocked","result","blocked","state","open"));continue;}String mode=state.equals("open")?"probe":"closed",result;if(b(call.get("ok"))){state="closed";failures=0;retry=null;result="success";}else{failures++;result="failure";if(mode.equals("probe")||failures>=lng(d.get("threshold"))){state="open";retry=now+lng(d.get("cooldown"));}}results.add(map("mode",mode,"result",result,"state",state));}return map("results",results,"state",state,"failures",failures,"retry_at",retry);}''',
"approach":"Process each call once with explicit closed, blocked-open, and half-open-probe paths. Time is O(C); working state is O(1), plus O(C) results. Production breakers must define which failures count, how concurrent probes are limited, and whether state is shared across processes.","cases":CASES,"generated":generated,"mutations":[{"name":"blocks the recovery probe at the exact deadline","old":"now < retry_at","new":"now <= retry_at"}],"sources":["https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker"]}
