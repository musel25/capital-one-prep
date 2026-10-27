"""Deterministic latest-row selection with a SQLite window function."""
import random
SCAFFOLD='''import sqlite3

def solve(data):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE readings(id INTEGER PRIMARY KEY, device TEXT NOT NULL, ts INTEGER NOT NULL, value INTEGER)")
        connection.executemany("INSERT INTO readings VALUES (?, ?, ?, ?)", [(r["id"], r["device"], r["ts"], r["value"]) for r in data["rows"]])
        return [dict(r) for r in latest_rows(connection, data["cutoff"])]
    finally:
        connection.close()

'''
QUERY='''def latest_rows(connection, cutoff):
    return connection.execute("WITH ranked AS (SELECT device, id, ts, value, ROW_NUMBER() OVER (PARTITION BY device ORDER BY ts DESC, id DESC) AS position FROM readings WHERE ts <= ?) SELECT device, id, ts, value FROM ranked WHERE position = 1 ORDER BY device ASC", (cutoff,)).fetchall()
'''
JAVA='''public Object solve(Map<String,Object> d){
    TreeMap<String,Map<String,Object>> best=new TreeMap<>();int cutoff=n(d.get("cutoff"));
    for(Object value:arr(d.get("rows"))){Map<String,Object> r=obj(value);if(n(r.get("ts"))>cutoff)continue;String device=s(r.get("device"));Map<String,Object> old=best.get(device);
        if(old==null||n(r.get("ts"))>n(old.get("ts"))||(n(r.get("ts"))==n(old.get("ts"))&&n(r.get("id"))>n(old.get("id"))))best.put(device,r);}
    List<Object> out=new ArrayList<>();for(Map<String,Object> r:best.values())out.add(map("device",r.get("device"),"id",r.get("id"),"ts",r.get("ts"),"value",r.get("value")));return out;
}'''
def row(i,device,ts,value=10):return {"id":i,"device":device,"ts":ts,"value":value}
def result(i,device,ts,value=10):return {"device":device,"id":i,"ts":ts,"value":value}
def case(rows,expected,label,cutoff=100):return {"input":{"rows":rows,"cutoff":cutoff},"expected":expected,"label":label}
CASES=[case([row(1,"a",5),row(2,"a",9),row(3,"b",6)],[result(2,"a",9),result(3,"b",6)],"latest row within each device"),case([row(1,"a",5,10),row(3,"a",5,30),row(2,"a",5,20)],[result(3,"a",5,30)],"largest id resolves timestamp tie"),case([row(1,"a",5),row(2,"a",20)],[result(1,"a",5)],"cutoff filters before ranking",cutoff=10),case([],[],"empty table"),case([row(1,"a",0)],[result(1,"a",0)],"zero timestamp at zero cutoff",cutoff=0),case([row(1,"a",5)],[result(1,"a",5)],"inclusive cutoff",cutoff=5),case([row(1,"a",6)],[],"device has no eligible row",cutoff=5),case([row(1,"a",1,99),row(2,"a",2,None)],[result(2,"a",2,None)],"latest null value is retained"),case([row(10,"a",1),row(2,"a",2)],[result(2,"a",2)],"timestamp outranks id"),case([row(1,"z",10),row(2,"a",1)],[result(2,"a",1),result(1,"z",10)],"output ordered by device"),case([row(1,"A",1),row(2,"a",1)],[result(1,"A",1),result(2,"a",1)],"case-sensitive partitions"),case([row(1,"a",1,-7)],[result(1,"a",1,-7)],"negative reading value"),case([row(1,"O'Reilly",3)],[result(1,"O'Reilly",3)],"quoted device name"),case([row(2,"a",5,0),row(10,"a",5,1)],[result(10,"a",5,1)],"numeric id comparison")]
R=random.Random(35)
GENERATED=[{"rows":[row(j,["a","b","A","z"][(i+j)%4],R.randrange(12),R.choice([None,-10,0,10])) for j in range(1,i+3)],"cutoff":i%13} for i in range(18)]
SPEC={"number":35,"slug":"sql-latest-per-device","title":"Select the latest row per device","difficulty":"Hard","time":35,"prerequisites":"Problems 31–34; SQL ordering, grouping, and NULL values.","learn":"Selecting the latest row in each group needs more than finding the maximum timestamp. Several rows can share that timestamp, and the result must keep values from one chosen row. A window function numbers rows within a partition while keeping their other columns. Partition by device and order each partition from newest to oldest. Add a unique id to resolve timestamp ties. Then select the row numbered one. A cutoff belongs before ranking when the question is the latest eligible row. Filtering only after choosing the overall newest row could remove a device that still has older eligible data.","scenario": ('An IoT dashboard shows the latest reading of each sensor at a given time (`cutoff`). Readings can arrive out of order.'),
 "example_notes": ['The latest reading of device `a` has ts 9.', 'All three rows have ts 5. The greatest id, 3, wins.', 'The ts 20 row is after the cutoff, so the ts 5 row is the latest.'],
 "task":('Complete `latest_rows(connection, cutoff)` in the SQLite scaffold. The table is `readings(id PRIMARY KEY, device, ts, value)`.\n'
    '\n'
    '**Input:** `data` has:\n'
    '- `rows`: a list of `{"id": int, "device": string, "ts": int, "value": int | null}`, with unique ids.\n'
    '- `cutoff`: an integer.\n'
    '\n'
    '**Rules**\n'
    '- Use only the rows with `ts` at most `cutoff`.\n'
    '- For each exact device string, select the row with the greatest `ts`. On a tie, select the greatest `id`.\n'
    '- Keep the value of that row, even when it is null.\n'
    '- A device with no eligible rows is not in the output.\n'
    '\n'
    '**Return** a list of `{"device": ..., "id": ..., "ts": ..., "value": ...}`, ordered by `device` ascending in SQLite\'s default binary order.\n'
    '\n'
    '**Practice:** use `ROW_NUMBER` with `PARTITION BY` and a deterministic order. The reference runs a real SQLite window query. The judge cannot check SQL or window-function use.'),"constraints":["0–400 rows. Ids are 1–1000000; ts and cutoff are integers from 0 through 1000000.","Device names have 1–50 printable ASCII characters and are case sensitive.","value is null or an integer in [-1000000,1000000]. Input row order has no meaning."],"hints":["Filter by cutoff inside the ranked subquery or common table expression.","Order each partition by ts DESC, id DESC, then keep row number one."],"starter":SCAFFOLD+"def latest_rows(connection, cutoff):\n    raise NotImplementedError\n","reference":SCAFFOLD+QUERY,"java":JAVA,"approach":"A common table expression ranks eligible rows within each device. The outer query retains rank one and sets the final device order. Without a supporting index, window ordering takes O(n log n) time and O(n) temporary space. The Java oracle independently scans for each device's best pair. Real schemas should choose a tie breaker that reflects a documented business rule.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"choose smallest id on a timestamp tie","old":"ORDER BY ts DESC, id DESC","new":"ORDER BY ts DESC, id ASC"}],"sources":["https://www.sqlite.org/windowfunctions.html","https://docs.python.org/3.11/library/sqlite3.html"]}
