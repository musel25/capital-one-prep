import random
REFERENCE='''def solve(data: dict) -> dict:
    messages = {key: {"token": 0, "until": 0, "done": False} for key in data["messages"]}
    results = []
    for op in data["ops"]:
        now = op["at"]
        if op["op"] == "receive":
            chosen = next((key for key, m in messages.items() if not m["done"] and m["until"] <= now), None)
            if chosen is None:
                results.append(None)
            else:
                m = messages[chosen]
                m["token"] += 1
                m["until"] = now + data["timeout"]
                results.append({"id": chosen, "token": m["token"]})
        else:
            m = messages.get(op["id"])
            accepted = m is not None and not m["done"] and m["token"] > 0 and m["token"] == op["token"] and now < m["until"]
            if accepted:
                m["done"] = True
            results.append(accepted)
    return {"results": results, "pending": [key for key, m in messages.items() if not m["done"]]}
'''
def r(at=0):return {"op":"receive","at":at}
def a(at=0,id="a",token=1):return {"op":"ack","at":at,"id":id,"token":token}
def rec(id="a",token=1):return {"id":id,"token":token}
def c(ids,timeout,ops,results,pending,label):return {"input":{"messages":ids,"timeout":timeout,"ops":ops},"expected":{"results":results,"pending":pending},"label":label}
CASES=[c(["a"],5,[r(),a(4)],[rec(),True],[],"ack before visibility timeout"),c(["a"],5,[r(),r(5),a(6,token=1),a(6,token=2)],[rec(),rec(token=2),False,True],[],"redelivery invalidates stale token"),c(["a"],5,[r(),a(5)],[rec(),False],["a"],"ack at timeout is too late"),c([],5,[],[],[],"empty queue and trace"),c([],5,[r(),a()],[None,False],[],"empty receive and unknown ack"),c(["a"],5,[a(token=0)],[False],["a"],"never received message cannot be acked"),c(["a"],5,[r(),r(4)],[rec(),None],["a"],"hidden message is unavailable"),c(["a"],5,[r(),a(),a()],[rec(),True,False],[],"duplicate ack rejected"),c(["a","b"],5,[r(),r(),r()],[rec(),rec("b"),None],["a","b"],"skip hidden earlier message"),c(["b","a"],5,[r(),r(5)],[rec("b"),rec("b",2)],["b","a"],"original queue order controls redelivery"),c(["a","b"],2,[r(),a(1),r(2),a(3,"b")],[rec(),True,rec("b"),True],[],"independent token counters"),c(["a"],1,[r(),r(1),r(2),a(2,token=2),a(2,token=3)],[rec(),rec(token=2),rec(token=3),False,True],[],"multiple visibility cycles")]
rng=random.Random(44)
generated=[]
for i in range(24):
 now=0;ops=[]
 for j in range(25):
  now+=rng.randrange(3);ops.append(r(now) if j%2==0 else a(now,rng.choice("abcx"),rng.randrange(0,8)))
 generated.append({"messages":list("abc"[:i%4]),"timeout":i+1,"ops":ops})
SPEC={"number":44,"slug":"queue-visibility-tokens","title":"Reject stale queue acknowledgements","difficulty":"Hard","time":35,"prerequisites":"State machines, integer clocks, and message retries.",
"learn":"Receiving a queue message can hide it for a limited time without deleting it. If the consumer does not acknowledge it before that deadline, another receive can deliver it again. Each delivery needs a fresh receipt token. An old consumer must not acknowledge the new delivery with its old token. This model uses an increasing token per message and accepts an acknowledgement only during that token's active visibility interval. At the exact deadline the message is visible again and the old token is invalid. These are the explicit rules of this exercise, not a promise about every queue provider. The task is a deterministic event trace, not an actual parallel, thread, or network test.",
"scenario": ('A job queue hides a message for `timeout` time units after a worker receives it. If the worker does not finish in time, the message becomes visible again, and another worker can take it. Each receipt gets a new token, so a slow first worker cannot acknowledge a message that another worker now owns.'),
 "example_notes": ['Received at 0 and acknowledged at 4, before the deadline of 5.', 'Redelivered at 5 with token 2. The old token 1 fails. Token 2 succeeds.', 'The acknowledgement at 5 is too late (the deadline is 5), so the message stays pending.'],
 "task":('**Input:** `data` has:\n'
    '- `messages`: unique IDs in queue order.\n'
    '- `timeout`: a positive visibility duration.\n'
    '- `ops`: a list of operations. Their `at` times never decrease.\n'
    '\n'
    '**Rules:** all messages start visible at time 0.\n'
    '- `receive`: select the first unacknowledged message whose deadline is at or before `at`. Add 1 to its token (the first token is 1) and set its deadline to `at + timeout`. Return `{"id": ..., "token": ...}`, or `null` if no message is visible.\n'
    '- `ack` (`id`, `token`): return `true` and remove the message only if it has an active delivery with exactly this token and `at < deadline`. Otherwise return `false`. Unknown IDs and token 0 can occur, and they always fail.\n'
    '\n'
    '**Return** `{"results": [...], "pending": [...]}`. `pending` lists the unacknowledged IDs in original order, including hidden messages.'),"constraints":["0–100 messages; 0–300 operations. IDs are nonempty ASCII strings.","Times are 0–1000000, timeout is 1–1000000, tokens are 0–1000000."],"hints":["Visibility and acknowledgement are separate state properties.","Check both token equality and the exclusive deadline before accepting an ack."],"starter":"def solve(data: dict) -> dict:\n    # Model ordered messages, receipt versions, and visibility deadlines.\n    raise NotImplementedError\n","reference":REFERENCE,
"java":'''public Object solve(Map<String,Object> d){List<Object> ids=arr(d.get("messages"));int count=ids.size();long[] tokens=new long[count],until=new long[count];boolean[] done=new boolean[count];List<Object> results=new ArrayList<>();for(Object raw:arr(d.get("ops"))){Map<String,Object> op=obj(raw);long now=lng(op.get("at"));if(s(op.get("op")).equals("receive")){int chosen=-1;for(int i=0;i<count;i++)if(!done[i]&&until[i]<=now){chosen=i;break;}if(chosen<0)results.add(null);else{tokens[chosen]++;until[chosen]=now+lng(d.get("timeout"));results.add(map("id",ids.get(chosen),"token",tokens[chosen]));}}else{int i=ids.indexOf(op.get("id"));boolean ok=i>=0&&!done[i]&&tokens[i]>0&&tokens[i]==lng(op.get("token"))&&now<until[i];if(ok)done[i]=true;results.add(ok);}}List<Object> pending=new ArrayList<>();for(int i=0;i<count;i++)if(!done[i])pending.add(ids.get(i));return map("results",results,"pending",pending);}''',
"approach":"Track a deadline, token counter, and acknowledged flag for each message. Scan in queue order on receive. This costs O(M × O) time and O(M + O) space. A real queue needs durable state and concurrent lease handling; receipt-token and expiry semantics differ between providers.","cases":CASES,"generated":generated,"mutations":[{"name":"accepts stale receipt tokens","old":"m[\"token\"] == op[\"token\"]","new":"m[\"token\"] >= op[\"token\"]"}],"sources":["https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html"]}
