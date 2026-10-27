"""Bug fix: a WHERE predicate can remove unmatched LEFT JOIN rows."""
import random
SCAFFOLD='''import sqlite3

def solve(data):
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        connection.execute("CREATE TABLE payments(id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER NOT NULL, status TEXT NOT NULL)")
        connection.executemany("INSERT INTO customers VALUES (?, ?)", [(r["id"], r["name"]) for r in data["customers"]])
        connection.executemany("INSERT INTO payments VALUES (?, ?, ?, ?)", [(r["id"], r["customer_id"], r["amount"], r["status"]) for r in data["payments"]])
        return [dict(r) for r in report_rows(connection)]
    finally:
        connection.close()

'''
QUERY='''def report_rows(connection):
    return connection.execute("SELECT c.id AS customer_id, c.name AS name, p.id AS payment_id, p.amount AS amount FROM customers AS c LEFT JOIN payments AS p ON p.customer_id = c.id AND p.status = 'paid' ORDER BY c.id ASC, p.id ASC").fetchall()
'''
BUG='''def report_rows(connection):
    # BUG: customers without paid payments disappear. Fix this query.
    return connection.execute("SELECT c.id AS customer_id, c.name AS name, p.id AS payment_id, p.amount AS amount FROM customers AS c LEFT JOIN payments AS p ON p.customer_id = c.id WHERE p.status = 'paid' ORDER BY c.id ASC, p.id ASC").fetchall()
'''
JAVA='''public Object solve(Map<String,Object> d){
    List<Object> customers=new ArrayList<>(arr(d.get("customers"))),payments=new ArrayList<>(arr(d.get("payments"))),out=new ArrayList<>();
    customers.sort(Comparator.comparingInt(v->n(obj(v).get("id"))));payments.sort(Comparator.comparingInt(v->n(obj(v).get("id"))));
    for(Object cv:customers){Map<String,Object> c=obj(cv);boolean matched=false;for(Object pv:payments){Map<String,Object> p=obj(pv);if(p.get("customer_id")!=null&&n(p.get("customer_id"))==n(c.get("id"))&&s(p.get("status")).equals("paid")){matched=true;out.add(map("customer_id",c.get("id"),"name",c.get("name"),"payment_id",p.get("id"),"amount",p.get("amount")));}}
        if(!matched)out.add(map("customer_id",c.get("id"),"name",c.get("name"),"payment_id",null,"amount",null));
    }return out;
}'''
def customer(i,name=None):return {"id":i,"name":str(i) if name is None else name}
def payment(i,cid,amount=10,status="paid"):return {"id":i,"customer_id":cid,"amount":amount,"status":status}
def result(cid,pid=None,amount=None,name=None):return {"customer_id":cid,"name":str(cid) if name is None else name,"payment_id":pid,"amount":amount}
def case(customers,payments,expected,label):return {"input":{"customers":customers,"payments":payments},"expected":expected,"label":label}
CASES=[case([customer(1),customer(2)],[payment(1,1)],[result(1,1,10),result(2)],"keep customer with no payments"),case([customer(1)],[payment(1,1,status="pending")],[result(1)],"pending-only customer remains with nulls"),case([customer(1)],[payment(3,1,30),payment(2,1,20)],[result(1,2,20),result(1,3,30)],"one output row per paid payment"),case([],[],[],"empty database"),case([],[payment(1,99)],[],"orphan payments create no customer"),case([customer(1)],[],[result(1)],"one unmatched customer"),case([customer(1)],[payment(1,None)],[result(1)],"null foreign key does not match"),case([customer(1)],[payment(1,2)],[result(1)],"missing related customer id"),case([customer(1)],[payment(1,1,0)],[result(1,1,0)],"zero amount is not missing"),case([customer(1)],[payment(1,1,-5)],[result(1,1,-5)],"negative paid amount"),case([customer(2,"same"),customer(1,"same")],[],[result(1,name="same"),result(2,name="same")],"names do not identify customers"),case([customer(10),customer(2)],[payment(10,2),payment(2,2)],[result(2,2,10),result(2,10,10),result(10)],"numeric order on both ids"),case([customer(1)],[payment(1,1,status="pending"),payment(2,1)],[result(1,2,10)],"do not add null row when a paid match exists"),case([customer(1,"O'Reilly")],[],[result(1,name="O'Reilly")],"quoted name survives scaffold")]
R=random.Random(32)
GENERATED=[{"customers":[customer(j,f"name{(j+i)%3}") for j in range(1,i%7+1)],"payments":[payment(j,R.choice([None,1,2,3,4,5,99]),R.randint(-5,20),R.choice(["paid","pending"])) for j in range(1,i+2)]} for i in range(18)]
SPEC={"number":32,"slug":"sql-left-join-fix","title":"Fix a LEFT JOIN that loses customers","difficulty":"Medium","time":30,"prerequisites":"Problem 31; SELECT, WHERE, ordering, and SQL NULL.","learn":"A LEFT JOIN keeps each row from its left table even when no right-table row matches. Missing right-side values become NULL. A condition in ON controls which right rows can match. A condition in WHERE runs after the join and can remove those generated NULL rows. This difference often breaks reports that must include customers with no activity. The starter query has that defect. Move the payment qualification to the correct place while preserving the full output contract. A zero amount is a real value, not a missing value. Customers can also share a name, so joins must use their ids rather than display text.","task":('**Bug fix.** The `report_rows(connection)` query is intentionally faulty. Fix it.\n'
    '\n'
    '**Input:** `data` has the lists `customers` and `payments`. The scaffold loads them into:\n'
    '- `customers(id PRIMARY KEY, name)`\n'
    '- `payments(id PRIMARY KEY, customer_id nullable, amount, status)`\n'
    '\n'
    '**Rules**\n'
    '- For each customer, output one row per payment that has a matching `customer_id` and `status` paid.\n'
    '- A customer with no matching paid payment gets exactly one row, with `payment_id` and `amount` set to null.\n'
    '- Ignore orphan payments, payments with a null `customer_id`, and pending payments.\n'
    '\n'
    '**Return** a list of `{"customer_id": ..., "name": ..., "payment_id": ..., "amount": ...}`, ordered by `customer_id` ascending, then `payment_id` ascending.\n'
    '\n'
    '**Practice:** use a LEFT JOIN. The reference runs SQLite. The judge cannot check SQL use or query structure.'),"constraints":["0–200 customers and 0–300 payments. Ids are positive integers at most 1000000 and unique within each table.","Payment customer_id is null or a positive integer at most 1000000. Foreign keys are intentionally not enforced.","status is paid or pending. amount is an integer in [-1000000,1000000]. Names have 1–50 printable ASCII characters."],"hints":["An unmatched right row contains SQL NULL in every selected payment column.","The paid condition belongs in the match rule, not a later filter that removes unmatched customers."],"starter":SCAFFOLD+BUG,"reference":SCAFFOLD+QUERY,"java":JAVA,"approach":"LEFT JOIN matches on customer id and the paid predicate together. Unmatched customers retain one NULL-filled payment side. Explicit ordering makes results stable. Without indexes, a simple join can require O(c*p) work; SQLite may build an automatic index. Sorting and output depend on the number of resulting rows. This fixture accepts orphan payments to make join behavior visible.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"move paid qualification to WHERE","old":"AND p.status = 'paid'","new":"WHERE p.status = 'paid'"}],"sources":["https://www.sqlite.org/lang_select.html#whereclause"]}
