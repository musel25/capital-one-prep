"""Per-user rolling windows with exact expiration boundaries."""
REF='''from collections import defaultdict, deque

def solve(data):
    accepted = defaultdict(deque)
    out = []
    for event in data["events"]:
        now = event["time"]
        queue = accepted[event["user"]]
        while queue and queue[0] <= now - data["window"]:
            queue.popleft()
        allowed = len(queue) < data["limit"]
        if allowed:
            queue.append(now)
        out.append({"allowed": allowed, "remaining": data["limit"] - len(queue), "retry_after": 0 if allowed else queue[0] + data["window"] - now})
    return out
'''
JAVA='''public Object solve(Map<String,Object> d){
    Map<String,List<Integer>> histories=new HashMap<>();List<Object> out=new ArrayList<>();int limit=n(d.get("limit")),window=n(d.get("window"));
    for(Object v:arr(d.get("events"))){Map<String,Object> e=obj(v);int now=n(e.get("time"));String user=s(e.get("user"));List<Integer> active=new ArrayList<>();
        for(int t:histories.getOrDefault(user,new ArrayList<>()))if(t>now-window)active.add(t);
        boolean allowed=active.size()<limit;if(allowed)active.add(now);histories.put(user,active);
        out.add(map("allowed",allowed,"remaining",limit-active.size(),"retry_after",allowed?0:active.get(0)+window-now));
    }return out;
}'''
def e(t,u="a"):return {"time":t,"user":u}
def a(rem=0):return {"allowed":True,"remaining":rem,"retry_after":0}
def no(wait):return {"allowed":False,"remaining":0,"retry_after":wait}
def case(limit,window,events,expected,label):return {"input":{"limit":limit,"window":window,"events":events},"expected":expected,"label":label}
CASES=[case(2,10,[e(0),e(1),e(2)],[a(1),a(),no(8)],"third call exceeds window"),case(1,10,[e(0),e(10)],[a(),a()],"timestamp at left boundary expires"),case(1,10,[e(0,"a"),e(0,"b"),e(1,"a")],[a(),a(),no(9)],"users have independent windows"),case(1,1,[],[],"empty event list"),case(3,10,[e(5)],[a(2)],"remaining after accepted call"),case(1,10,[e(0),e(0)],[a(),no(10)],"same timestamp counts twice"),case(1,10,[e(0),e(9),e(10)],[a(),no(1),a()],"rejection does not extend window"),case(2,10,[e(0),e(5),e(10),e(11)],[a(1),a(),a(),no(4)],"only oldest event expires"),case(2,10,[e(0),e(1),e(100)],[a(1),a(),a(1)],"large jump expires all"),case(1,1,[e(0),e(1),e(2)],[a(),a(),a()],"smallest window"),case(1,10,[e(0,"A"),e(0,"a")],[a(),a()],"case-sensitive user keys"),case(2,3,[e(2),e(2),e(2),e(5),e(5)],[a(1),a(),no(3),a(1),a()],"multiple expirations at same boundary"),case(1,10,[e(999990),e(1000000)],[a(),a()],"large absolute clock")]
GENERATED=[{"limit":i%4+1,"window":i%7+1,"events":[e(j*(i%3),["a","b","a","c"][(j+i)%4]) for j in range(i+3)]} for i in range(18)]
SPEC={"number":28,"slug":"rolling-rate-limit","title":"Rate limits with a rolling window","difficulty":"Medium","time":30,"prerequisites":"Problems 20 and 27; deque, dictionaries, and integer clocks.","learn":"A rolling limit counts accepted requests in a recent time interval. Its exact boundary matters. For the interval used here, a request at time t counts earlier accepted requests whose timestamps are greater than t minus the window. A timestamp exactly at that boundary has expired. A deque fits this rule because events arrive in time order and expire from the front. Keep one history per user. Rejected requests do not enter that history, so repeated rejection cannot push the next allowed time farther away. This sequential simulation checks the policy. A live service would also need atomic updates across simultaneous callers and shared storage across workers.","task":('**Input:** `data` has:\n'
    '- `limit`: a positive integer.\n'
    '- `window`: a positive integer.\n'
    '- `events`: a list of `{"time": int, "user": string}`, in time order.\n'
    '\n'
    "**Rules:** each user can have at most `limit` accepted events in the window `(time - window, time]`. Every user's history starts empty. For each event:\n"
    "1. Remove that user's accepted timestamps that are less than or equal to `time - window`.\n"
    '2. If the number left is below `limit`, accept the event and add its timestamp. Otherwise reject it and do not add it.\n'
    '\n'
    '**Return** one `{"allowed": bool, "remaining": int, "retry_after": int}` per event:\n'
    "- `remaining`: the user's free capacity after this decision.\n"
    "- `retry_after`: 0 if accepted. If rejected, the positive time until the user's oldest active accepted timestamp expires.\n"
    '\n'
    '**Practice:** use a `deque`. The judge checks only the output.'),"constraints":["limit is 1–100, window is 1–10000, and there are 0–500 events.","Times are integers from 0 through 1000000 and are globally nondecreasing; ties are allowed.","User keys are case-sensitive nonempty ASCII strings of at most 30 characters."],"hints":["Remove expired timestamps with a while loop, not one if statement.","Only accepted calls belong in the deque."],"starter":"from collections import defaultdict, deque\n\ndef solve(data: dict) -> list:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"Maintain a deque for each user. Each accepted timestamp is appended once and removed at most once, giving O(e) total time. Active histories use O(u * limit) space for u users, plus output. The Java oracle independently filters timestamp lists. This does not test concurrent rate-limit enforcement.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"keep timestamp at expired boundary","old":"queue[0] <= now - data[\"window\"]","new":"queue[0] < now - data[\"window\"]"}],"sources":["https://docs.python.org/3/library/collections.html#collections.deque"]}
