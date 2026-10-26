"""Seek pagination with a composite ordering key."""
import random
REF='''def solve(data):
    records = [dict(row) for row in data["records"]]
    out = []
    for action in data["actions"]:
        if action["op"] == "insert":
            records.append(dict(action["record"]))
            continue
        after = action["after"]
        eligible = sorted((r for r in records if after is None or (r["ts"], r["id"]) > tuple(after)), key=lambda r: (r["ts"], r["id"]))
        selected = eligible[:action["limit"]]
        more = len(eligible) > len(selected)
        cursor = [selected[-1]["ts"], selected[-1]["id"]] if more else None
        out.append({"ids": [r["id"] for r in selected], "next": cursor})
    return out
'''
JAVA='''public Object solve(Map<String,Object> d){
    List<Object> rows=new ArrayList<>(arr(d.get("records"))), out=new ArrayList<>();
    Comparator<Object> order=Comparator.comparingInt((Object v)->n(obj(v).get("ts"))).thenComparingInt(v->n(obj(v).get("id")));
    for(Object v:arr(d.get("actions"))){Map<String,Object> a=obj(v);if(s(a.get("op")).equals("insert")){rows.add(a.get("record"));continue;}
        List<Object> eligible=new ArrayList<>();Object after=a.get("after");
        for(Object row:rows){Map<String,Object> r=obj(row);boolean keep=after==null;if(!keep){List<Object> c=arr(after);keep=n(r.get("ts"))>n(c.get(0))||(n(r.get("ts"))==n(c.get(0))&&n(r.get("id"))>n(c.get(1)));}if(keep)eligible.add(row);}
        eligible.sort(order);int count=Math.min(n(a.get("limit")),eligible.size());List<Object> ids=new ArrayList<>();for(int i=0;i<count;i++)ids.add(obj(eligible.get(i)).get("id"));Object next=null;
        if(count<eligible.size()){Map<String,Object> last=obj(eligible.get(count-1));next=list(last.get("ts"),last.get("id"));}out.add(map("ids",ids,"next",next));
    }return out;
}'''
def row(i,t):return {"id":i,"ts":t}
def page(after=None,limit=2):return {"op":"page","after":after,"limit":limit}
def insert(i,t):return {"op":"insert","record":row(i,t)}
def answer(ids,next=None):return {"ids":ids,"next":next}
def case(rows,actions,expected,label):return {"input":{"records":rows,"actions":actions},"expected":expected,"label":label}
CASES=[case([row(3,2),row(2,1),row(1,1)],[page(None,2)],[answer([1,2],[1,2])],"timestamp ties use id"),case([row(1,10),row(2,20)],[page(None,1),insert(3,5),page([10,1],1)],[answer([1],[10,1]),answer([2])],"insertion before cursor does not shift page"),case([row(1,10),row(2,20)],[page(None,1),insert(3,15),page([10,1],1)],[answer([1],[10,1]),answer([3],[15,3])],"new row after cursor can appear"),case([],[],[],"no actions"),case([],[page()],[answer([])],"empty page"),case([row(1,0)],[page()],[answer([1])],"one row"),case([row(1,1),row(2,1)],[page([1,1],1)],[answer([2])],"cursor excludes exact row"),case([row(1,1),row(2,1)],[page(None,2)],[answer([1,2])],"exactly full final page has null cursor"),case([row(1,1)],[page([100,100])],[answer([])],"cursor beyond final row"),case([row(5,7)],[page([7,2])],[answer([5])],"cursor need not name existing row"),case([row(1,1),row(2,2)],[page(None,1),page(None,1)],[answer([1],[1,1]),answer([1],[1,1])],"queries do not consume rows"),case([],[insert(4,0),page()],[answer([4])],"insert into empty data"),case([row(10,1),row(2,1)],[page(None,1)],[answer([2],[1,2])],"numeric id order"),case([row(1,1)],[insert(2,1),page([1,1])],[answer([2])],"same timestamp insertion after cursor")]
R=random.Random(25)
GENERATED=[{"records":[row(j,R.randrange(8)) for j in range(1,i+1)],"actions":[page(None,i%4+1),insert(100+i,R.randrange(8)),page([i%8,i//2+1],i%5+1)]} for i in range(16)]
SPEC={"number":25,"slug":"cursor-tie-breaks","title":"Page by timestamp and id","difficulty":"Medium","time":35,"prerequisites":"Problems 21–24; tuple ordering and state changes.","learn":"Offset pagination counts how many rows to skip. An insertion before that position can shift later pages. A cursor can instead store the final ordering key from the previous page. The next query asks for keys strictly after that key. A timestamp alone is not sufficient when records share a timestamp. Add a unique id to create a total order. This exercise makes the cursor visible as a pair so the ordering rule is easy to inspect. New records after the cursor can appear in later results. Records inserted before it will not appear there. Cursor pagination alone does not create a database snapshot.","task":"`records` is a list of `{id:int, ts:int}`. `actions` contains inserts `{op:\"insert\", record:{id,ts}}` and page requests `{op:\"page\", after:null|[ts,id], limit:int}`. Inserted ids are globally unique. For each page, use current records ordered by ascending `(ts,id)`. If after is non-null, keep only keys strictly greater than it. Take at most limit records. Return `{ids:[...], next:cursor}` for that page. Set next to the final selected `[ts,id]` only if more eligible records remain. Otherwise next is null, including an empty page. A cursor need not name an existing record. Return only page responses; inserts produce none. Each page uses its supplied cursor independently.","constraints":["0–200 initial rows and 0–200 actions. At most 400 rows in total.","Ids are 1–1000000; timestamps are 0–1000000. All are integers. Limits are 1–50.","No deletions or timestamp changes. No snapshot isolation or network calls."],"hints":["Compare the full pair, not just the timestamp.","Use one extra eligible row, or the eligible count, to determine whether next is needed."],"starter":"def solve(data: dict) -> list:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"For each page, filter with a strict tuple comparison and sort the remaining records. The reference takes O(n log n) time per page and O(n) temporary space. An indexed database can seek by the composite key more efficiently. Opaque signed cursors and snapshot consistency are separate production concerns.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"include cursor row again","old":"> tuple(after)","new":">= tuple(after)"}],"sources":["https://www.postgresql.org/docs/current/queries-order.html","https://www.postgresql.org/docs/current/queries-limit.html"]}
