"""Shared deadlines constrain each sequential request."""
REF='''def solve(data):
    elapsed = completed = started = 0
    for step in data["steps"]:
        remaining = data["budget"] - elapsed
        if remaining <= 0:
            return {"result": "deadline", "elapsed": elapsed, "completed": completed, "started": started}
        started += 1
        allowance = min(step["timeout"], remaining)
        if step["duration"] > allowance:
            elapsed += allowance
            result = "deadline" if allowance == remaining else "timeout"
            return {"result": result, "elapsed": elapsed, "completed": completed, "started": started}
        elapsed += step["duration"]
        if step["outcome"] == "error":
            return {"result": "error", "elapsed": elapsed, "completed": completed, "started": started}
        completed += 1
    return {"result": "success", "elapsed": elapsed, "completed": completed, "started": started}
'''
JAVA='''public Object solve(Map<String,Object> d){
    int elapsed=0,completed=0,started=0,budget=n(d.get("budget"));String result="success";
    for(Object value:arr(d.get("steps"))){Map<String,Object> step=obj(value);int remaining=budget-elapsed;
        if(remaining<=0){result="deadline";break;}started++;int allowed=Math.min(n(step.get("timeout")),remaining),duration=n(step.get("duration"));
        if(duration>allowed){elapsed+=allowed;result=allowed==remaining?"deadline":"timeout";break;}
        elapsed+=duration;if(s(step.get("outcome")).equals("error")){result="error";break;}completed++;
    }return map("result",result,"elapsed",elapsed,"completed",completed,"started",started);
}'''
def step(d,t=10,o="ok"):return {"duration":d,"timeout":t,"outcome":o}
def case(budget,steps,result,elapsed,completed,started,label):return {"input":{"budget":budget,"steps":steps},"expected":{"result":result,"elapsed":elapsed,"completed":completed,"started":started},"label":label}
CASES=[case(10,[step(4),step(7)],"deadline",10,1,2,"second step gets only remaining budget"),case(20,[step(8,5)],"timeout",5,0,1,"per-step timeout can expire first"),case(10,[step(10)],"success",10,1,1,"completion at deadline succeeds"),case(0,[],"success",0,0,0,"no work needs no time"),case(0,[step(0)],"deadline",0,0,0,"no step starts without budget"),case(1,[step(0),step(0)],"success",0,2,2,"zero-duration work"),case(10,[step(3,10,"error"),step(1)],"error",3,0,1,"upstream error stops sequence"),case(5,[step(9,5,"error")],"deadline",5,0,1,"unobserved error loses to time limit"),case(10,[step(5,5)],"success",5,1,1,"completion at per-step timeout"),case(5,[step(5),step(0)],"deadline",5,1,1,"later zero-time step still needs start budget"),case(10,[step(2),step(3)],"success",5,2,2,"successful sequence"),case(10,[step(2),step(8,3)],"timeout",5,1,2,"elapsed includes failed wait"),case(10,[step(10,10,"error")],"error",10,0,1,"error observed exactly at deadline"),case(1,[step(2,10)],"deadline",1,0,1,"small shared budget")]
GENERATED=[{"budget":i,"steps":[step(j%7,(j+i)%8+1,"error" if j==i%6 else "ok") for j in range(i%9+1)]} for i in range(18)]
SPEC={"number":27,"slug":"shared-deadline","title":"Spend one timeout budget","difficulty":"Medium","time":30,"prerequisites":"Problem 26; integer clocks and sequential client operations.","learn":"A per-request timeout does not bound the total time of a sequence. Several individually acceptable waits can exceed a caller's deadline. Track one remaining budget across all operations. Before each request, limit its wait to the smaller of its own timeout and the remaining budget. Stop when either limit expires. Boundary rules must be explicit: this exercise accepts a response that arrives exactly at its allowance. It does not start another operation when no budget remains. The clock advances only by simulated waiting time. Real clients need a monotonic clock and must account for connection setup, processing, cancellation, and cleanup as well.","scenario": ('A checkout request must finish within a total time budget. It calls several services in order, and each call has its own timeout. `solve` simulates how much time the request uses and why it stops.'),
 "example_notes": ['The first call takes 4. The second call needs 7, but only 6 remain in the budget: `deadline`.', 'The call needs 8, but its own timeout is 5: `timeout`.', 'The call takes exactly 10 of a budget of 10. This is still a success.'],
 "task":('**Input:** `data` has:\n'
    '- `budget`: the total time allowance, in milliseconds.\n'
    '- `steps`: a list of `{"duration": int, "timeout": int, "outcome": "ok" | "error"}`.\n'
    '\n'
    '**Rules:** `elapsed`, `completed`, and `started` start at 0. For each step, in order:\n'
    '1. If the remaining budget (`budget - elapsed`) is 0, stop with `deadline`. Do not start the step.\n'
    '2. Add 1 to `started`. Set `allowance = min(timeout, remaining budget)`.\n'
    '3. If `duration > allowance`: add `allowance` to `elapsed` and stop. The result is `deadline` if the shared budget was the limit (allowance = remaining budget, also when `timeout` is equal to it). Otherwise the result is `timeout`.\n'
    '4. Otherwise add `duration` to `elapsed`. If the outcome is `error`, stop with `error`. If it is `ok`, add 1 to `completed`.\n'
    '\n'
    'If all steps finish, the result is `success`, even when the last step ends exactly at the deadline. An empty `steps` list gives `success`.\n'
    '\n'
    '**Return** `{"result": string, "elapsed": int, "completed": int, "started": int}`. `completed` counts only `ok` steps.'),"constraints":["budget is 0–1000000. There are 0–200 steps.","duration is 0–10000 and timeout is 1–10000. All clocks are integer milliseconds.","No retries, CPU time, sleeps, or actual network calls."],"hints":["Compute remaining from one accumulated elapsed value.","Check response arrival before deciding whether its outcome is an error."],"starter":"def solve(data: dict) -> dict:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"Keep three counters and stop at the first unsuccessful step. Each step consumes only its actual completed duration or its bounded wait. Time is O(s), with O(1) extra space. The model is sequential and excludes cancellation overhead. It cannot demonstrate live network timing guarantees.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"reject responses exactly at allowance","old":"step[\"duration\"] > allowance","new":"step[\"duration\"] >= allowance"}],"sources":["https://grpc.io/docs/guides/deadlines/","https://docs.python.org/3/library/time.html#time.monotonic"]}
