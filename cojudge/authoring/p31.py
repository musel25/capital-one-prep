"""SQLite filtering, safe parameters, and deterministic limits."""
import random
SCAFFOLD='''import sqlite3

def solve(data):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE transfers(id INTEGER PRIMARY KEY, owner TEXT NOT NULL, amount INTEGER NOT NULL, posted INTEGER NOT NULL)")
        connection.executemany("INSERT INTO transfers VALUES (?, ?, ?, ?)", [(r["id"], r["owner"], r["amount"], r["posted"]) for r in data["rows"]])
        return [dict(r) for r in select_rows(connection, data["owner"], data["minimum"], data["limit"])]
    finally:
        connection.close()

'''
QUERY='''def select_rows(connection, owner, minimum, limit):
    return connection.execute("SELECT id, amount FROM transfers WHERE owner = ? AND posted = 1 AND amount >= ? ORDER BY amount DESC, id ASC LIMIT ?", (owner, minimum, limit)).fetchall()
'''
JAVA='''public Object solve(Map<String,Object> d){
    List<Object> selected=new ArrayList<>();String owner=s(d.get("owner"));int minimum=n(d.get("minimum"));
    for(Object value:arr(d.get("rows"))){Map<String,Object> r=obj(value);if(s(r.get("owner")).equals(owner)&&b(r.get("posted"))&&n(r.get("amount"))>=minimum)selected.add(value);}
    selected.sort(Comparator.comparingInt((Object value)->n(obj(value).get("amount"))).reversed().thenComparingInt(value->n(obj(value).get("id"))));
    List<Object> out=new ArrayList<>();for(int i=0;i<Math.min(n(d.get("limit")),selected.size());i++){Map<String,Object> r=obj(selected.get(i));out.add(map("id",r.get("id"),"amount",r.get("amount")));}return out;
}'''
def row(i,amount,owner="a",posted=True):return {"id":i,"amount":amount,"owner":owner,"posted":posted}
def result(i,amount):return {"id":i,"amount":amount}
def case(rows,expected,label,owner="a",minimum=0,limit=10):return {"input":{"rows":rows,"owner":owner,"minimum":minimum,"limit":limit},"expected":expected,"label":label}
CASES=[case([row(3,20),row(1,20),row(2,10)],[result(1,20),result(3,20)],"sort before taking limit",limit=2),case([row(1,5,"O'Reilly"),row(2,9)],[result(1,5)],"quoted owner is a bound value",owner="O'Reilly"),case([row(1,10),row(2,9),row(3,20,posted=False)],[result(1,10)],"inclusive minimum and posted filter",minimum=10),case([],[],"empty table"),case([row(1,1)],[],"zero row limit",limit=0),case([row(1,1)],[result(1,1)],"single match"),case([row(1,1,"b")],[],"other owner"),case([row(1,1,posted=False)],[],"pending transfer"),case([row(1,-2),row(2,0),row(3,-5)],[result(2,0),result(1,-2)],"negative amount boundary",minimum=-2),case([row(1,2,"A"),row(2,1)],[result(2,1)],"owner is case sensitive"),case([row(1,100),row(2,99)],[],"minimum above all rows",minimum=101),case([row(1,5,"' OR 1=1 --"),row(2,99)],[result(1,5)],"SQL-looking text is data",owner="' OR 1=1 --"),case([row(10,5),row(2,5)],[result(2,5),result(10,5)],"numeric id tie break"),case([row(1,0),row(2,-1)],[result(1,0)],"zero amount meets zero minimum")]
R=random.Random(31)
GENERATED=[{"rows":[row(j,R.randint(-10,20),["a","b","O'Reilly"][(i+j)%3],bool((i+j)%2)) for j in range(1,i+2)],"owner":["a","b","O'Reilly"][i%3],"minimum":i-8,"limit":i%6} for i in range(18)]
SPEC={"number":31,"slug":"sql-filter-order","title":"Query posted transfers safely","difficulty":"Medium","time":30,"prerequisites":"Problems 1–30; Python functions and API input boundaries. No prior SQL is required.","learn":"SQL describes the rows you want from a table. SELECT chooses output columns. WHERE keeps rows that meet a condition. ORDER BY defines their result order, and LIMIT bounds the number returned. Without a complete ordering rule, equal values can appear in an unstable order. Add a unique id as a tie breaker. Python's sqlite3 module passes query values separately through placeholders. A name containing a quote must remain a value rather than become part of SQL text. The supplied code creates an in-memory database and loads the input. Your task is to write the selection query, not database setup code.","task":"Complete `select_rows(connection, owner, minimum, limit)` in the supplied SQLite scaffold. `rows` contains `{id:int, owner:string, amount:int, posted:bool}`; ids are unique. The table is `transfers(id, owner, amount, posted)` with posted stored as 0 or 1. Select rows whose owner equals the supplied owner exactly, posted is 1, and amount is at least minimum. Order by amount descending, then id ascending. Return at most limit rows with only id and amount. The scaffold turns query rows into the output list. Use bound parameters for owner, minimum, and limit. The reference executes real SQLite queries. The output judge checks results; it cannot enforce SQL use or parameter binding.","constraints":["0–300 rows; ids are 1–1000000. amount and minimum are integers in [-1000000,1000000].", "limit is 0–100. Owner strings have 1–80 printable ASCII characters, including possible quotes and SQL punctuation.","All input rows meet the schema; there are no duplicate ids or null fields."],"hints":["Use question-mark placeholders and pass a tuple of values to execute.","Apply ORDER BY before LIMIT, with id as the second sort key."],"starter":SCAFFOLD+"def select_rows(connection, owner, minimum, limit):\n    raise NotImplementedError\n","reference":SCAFFOLD+QUERY,"java":JAVA,"approach":"The query binds all external values, filters in WHERE, and orders by amount and id before applying LIMIT. Without extra indexes, scanning takes O(n) and sorting can take O(n log n), with O(n) temporary storage. The scaffold also loads O(n) rows. An index that starts with the filtering and ordering columns may help production workloads; query plans and data distribution determine the benefit.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"exclude exact minimum","old":"amount >= ?","new":"amount > ?"}],"sources":["https://docs.python.org/3.11/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries","https://www.sqlite.org/lang_select.html"]}
