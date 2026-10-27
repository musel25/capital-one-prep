"""Explicit retry classes and bounded exponential delays."""
REF='''def solve(data):
    delays = []
    for index in range(data["max_attempts"]):
        outcome = data["outcomes"][index]
        attempts = index + 1
        if isinstance(outcome, int) and 200 <= outcome < 300:
            return {"attempts": attempts, "delays": delays, "result": "success"}
        retryable = outcome == "timeout" or outcome in (429, 500, 502, 503, 504)
        if not retryable:
            return {"attempts": attempts, "delays": delays, "result": "failed"}
        if attempts == data["max_attempts"]:
            return {"attempts": attempts, "delays": delays, "result": "exhausted"}
        delays.append(min(data["cap"], data["base"] * 2 ** index))
'''
JAVA='''public Object solve(Map<String,Object> d){
    List<Object> delays=new ArrayList<>(), outcomes=arr(d.get("outcomes"));int max=n(d.get("max_attempts"));long delay=n(d.get("base")),cap=n(d.get("cap"));
    for(int i=0;i<max;i++){Object raw=outcomes.get(i);boolean timeout=raw instanceof String;int status=timeout?0:n(raw);String result=null;
        if(!timeout&&status>=200&&status<300)result="success";
        else if(!(timeout||status==429||status==500||status==502||status==503||status==504))result="failed";
        else if(i+1==max)result="exhausted";
        if(result!=null)return map("attempts",i+1,"delays",delays,"result",result);
        delays.add(Math.min(cap,delay));delay*=2;
    }throw new IllegalStateException();
}'''
def case(outcomes,maximum,base,cap,attempts,delays,result,label):return {"input":{"outcomes":outcomes,"max_attempts":maximum,"base":base,"cap":cap},"expected":{"attempts":attempts,"delays":delays,"result":result},"label":label}
CASES=[case([503,503,200],3,2,3,3,[2,3],"success","backoff is capped"),case([400,200],2,1,10,1,[],"failed","do not retry a client error"),case(["timeout",504],2,4,20,2,[4],"exhausted","no delay after final failure"),case([200],1,1,1,1,[],"success","immediate success"),case([429],1,1,10,1,[],"exhausted","one allowed attempt"),case([201,500],2,10,5,1,[],"success","all 2xx responses succeed"),case([299],1,1,1,1,[],"success","upper success boundary"),case([300],1,1,1,1,[],"failed","redirect is terminal here"),case([501,200],2,1,10,1,[],"failed","not all server errors are retryable"),case([502,200],2,9,3,2,[3],"success","cap applies from first delay"),case([500,502,503,504,429,"timeout"],6,1,8,6,[1,2,4,8,8],"exhausted","all specified transient outcomes"),case(["timeout",403,200],3,2,20,2,[2],"failed","terminal error after retry"),case([599],1,2,4,1,[],"failed","unlisted server error"),case([199],1,2,4,1,[],"failed","below success range")]
GENERATED=[{"outcomes":[[500,502,503,504,429,"timeout"][(i+j)%6] for j in range(i%6)]+[200 if i%2 else 422]+[503]*8,"max_attempts":i%8+1,"base":i+1,"cap":i%5+1} for i in range(18)]
SPEC={"number":26,"slug":"retry-backoff","title":"Classify retries and cap backoff","difficulty":"Medium","time":25,"prerequisites":"Problems 21–25; loops, status codes, and bounded state.","learn":"A retry policy needs three decisions: which failures are temporary, how many attempts are allowed, and how long to wait between attempts. Retrying every failure can repeat a permanent error and overload a service. Exponential backoff increases delays after repeated temporary failures. A cap bounds each delay. An attempt limit includes the first request, so three attempts allow at most two waits. Production clients often add random jitter and honor server guidance. This exercise excludes both to make results deterministic. Its retry set is an explicit local policy. Apply it to an operation that is safe to repeat, such as a read or a protected write.","scenario": ('A payment client calls a bank API. Some failures are temporary (timeouts, 429, and some 5xx errors), and the client retries them with exponential backoff. Other failures, such as 400, are permanent, and the client must stop at once. `outcomes` lists what the API returns on each attempt.'),
 "example_notes": ['503 two times, then 200. The delays are 2, then 4 capped to 3.', '400 is not retryable, so the client stops after 1 attempt.', 'Two retryable failures with a maximum of 2 attempts: `exhausted`, with one delay.'],
 "task":('**Input:** `data` has:\n'
    '- `outcomes`: a list. Each entry is an integer HTTP status or the string `"timeout"`.\n'
    '- `max_attempts`: the maximum number of attempts.\n'
    '- `base`, `cap`: integers, in milliseconds.\n'
    '\n'
    '**Rules:** use one outcome per attempt, in order, for at most `max_attempts` attempts.\n'
    '- Status 200–299 → stop with `success`.\n'
    '- Retryable outcomes are only `"timeout"` and the statuses 429, 500, 502, 503, and 504.\n'
    '- Any other status → stop with `failed`.\n'
    '- A retryable outcome on the last allowed attempt → stop with `exhausted`.\n'
    '- A retryable outcome with attempts left → record a delay, then retry. Before retry number k (k starts at 1), the delay is `min(cap, base * 2**(k-1))`.\n'
    '\n'
    'Record a delay only when another attempt will run. Ignore unused outcomes. Do not sleep or make network calls.\n'
    '\n'
    '**Return** `{"attempts": int, "delays": [int], "result": "success" | "failed" | "exhausted"}`.'),"constraints":["max_attempts is 1–10. outcomes contains at least max_attempts and at most 30 entries.","Statuses are integers 100–599. base is 1–1000 and cap is 1–10000, in milliseconds.","The exercise has no Retry-After header, jitter, or overall deadline."],"hints":["Return immediately for success and permanent failure.","The first delay is base, subject to the cap."],"starter":"def solve(data: dict) -> dict:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"Walk the outcome sequence until success, permanent failure, or the attempt limit. Append only delays that precede an actual retry. Time and output space are O(a) for a attempts. A production policy also considers idempotency, server hints, jitter, and a total deadline.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"retry every server error","old":"outcome in (429, 500, 502, 503, 504)","new":"(isinstance(outcome, int) and (outcome == 429 or outcome >= 500))"}],"sources":["https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/"]}
