"""Original deterministic HTTP routing exercise."""
import random

REF = '''import re

def solve(data):
    items = {item["id"]: dict(item) for item in data["items"]}
    out = []
    for request in data["requests"]:
        path, method = request["path"], request["method"]
        match = re.fullmatch(r"/items/([1-9][0-9]*)", path)
        if path == "/health":
            allowed = ["GET"]
        elif path == "/items":
            allowed = ["GET"]
        elif match:
            allowed = ["GET", "DELETE"]
        else:
            out.append({"status": 404, "body": {"error": "not_found"}})
            continue
        if method not in allowed:
            out.append({"status": 405, "body": {"error": "method_not_allowed"}, "allow": allowed})
        elif path == "/health":
            out.append({"status": 200, "body": {"status": "ok"}})
        elif path == "/items":
            out.append({"status": 200, "body": [dict(items[k]) for k in sorted(items)]})
        elif int(match[1]) not in items:
            out.append({"status": 404, "body": {"error": "not_found"}})
        elif method == "GET":
            out.append({"status": 200, "body": dict(items[int(match[1])])})
        else:
            del items[int(match[1])]
            out.append({"status": 204, "body": None})
    return out
'''
JAVA = '''public Object solve(Map<String,Object> d) {
    TreeMap<Integer,Object> items = new TreeMap<>();
    for(Object v:arr(d.get("items"))) items.put(n(obj(v).get("id")),v);
    List<Object> out = new ArrayList<>();
    for(Object v:arr(d.get("requests"))) {
        Map<String,Object> r=obj(v); String p=s(r.get("path")), m=s(r.get("method"));
        boolean detail=p.matches("/items/[1-9][0-9]*");
        if(!p.equals("/health")&&!p.equals("/items")&&!detail) {out.add(map("status",404,"body",map("error","not_found")));continue;}
        List<Object> allowed=detail?list("GET","DELETE"):list("GET");
        if(!allowed.contains(m)){out.add(map("status",405,"body",map("error","method_not_allowed"),"allow",allowed));continue;}
        if(p.equals("/health")){out.add(map("status",200,"body",map("status","ok")));continue;}
        if(p.equals("/items")){out.add(map("status",200,"body",new ArrayList<>(items.values())));continue;}
        int id=Integer.parseInt(p.substring(7));
        if(!items.containsKey(id)){out.add(map("status",404,"body",map("error","not_found")));continue;}
        if(m.equals("GET"))out.add(map("status",200,"body",items.get(id)));
        else {items.remove(id);out.add(map("status",204,"body",null));}
    } return out;
}'''
def req(path, method="GET"): return {"path": path, "method": method}
def response(status, body, **kw): return {"status": status, "body": body, **kw}
def case(items, requests, expected, label): return {"input": {"items": items, "requests": requests}, "expected": expected, "label": label}
NOT=response(404,{"error":"not_found"})
A={"id":1,"name":"pen"}; B={"id":2,"name":"book"}
CASES=[
case([B,A],[req("/items")],[response(200,[A,B])],"collection is ordered by numeric id"),
case([A],[req("/items/1","DELETE"),req("/items/1")],[response(204,None),NOT],"delete then read"),
case([],[req("/items/9","POST")],[response(405,{"error":"method_not_allowed"},allow=["GET","DELETE"])],"method check precedes item lookup"),
case([],[],[],"empty request batch"),
case([],[req("/items")],[response(200,[])],"empty collection"),
case([],[req("/health")],[response(200,{"status":"ok"})],"health route"),
case([A],[req("/items/1")],[response(200,A)],"one item"),
case([],[req("/items/1")],[NOT],"missing item"),
case([A],[req("/items/1","DELETE"),req("/items/1","DELETE")],[response(204,None),NOT],"repeated delete"),
case([A],[req("/items/01"),req("/items/0"),req("/items/1/")],[NOT,NOT,NOT],"noncanonical paths"),
case([],[req("/health","HEAD")],[response(405,{"error":"method_not_allowed"},allow=["GET"])],"no implicit HEAD in this contract"),
case([],[req("/other","POST")],[NOT],"unknown route before method"),
case([A,B],[req("/items"),req("/items/1","DELETE"),req("/items")],[response(200,[A,B]),response(204,None),response(200,[B])],"earlier response is a snapshot"),
case([],[req("/items","POST")],[response(405,{"error":"method_not_allowed"},allow=["GET"])],"collection rejects POST"),
]
R=random.Random(21)
GENERATED=[{"items":[{"id":j,"name":f"item-{j}"} for j in range(1,i%7+1)],"requests":[req(R.choice(["/health","/items",f"/items/{R.randint(1,9)}","/bad"]),R.choice(["GET","DELETE","POST"])) for _ in range(i+1)]} for i in range(16)]
SPEC={"number":21,"slug":"route-contract","title":"Route and method contracts","difficulty":"Easy","time":25,"prerequisites":"Problems 1–20: dictionaries, functions, and state transitions.","learn":"An API contract defines the response for each route and method. A route selects a resource shape. A method selects an operation on that shape. Keep these decisions separate from the search for one stored record. A missing route and an unsupported method have different meanings. A successful delete can return no representation. Response bodies must also be snapshots: a later write must not change an earlier response. This exercise uses familiar HTTP status codes but defines a small explicit routing policy. It is a deterministic simulation. It does not start a server, parse a URL, or implement every HTTP rule.","scenario": ('You build a small HTTP API for an internal inventory tool. There is no real server: `solve` gets the stored items and a list of requests, and returns the response to each request, in order.'),
 "example_notes": ['`GET /items` lists all items, sorted by id.', '`DELETE` returns 204. A later `GET` of the same item returns 404.', '`POST` is not allowed on `/items/9`: 405 with the allowed methods. The method is checked before the item lookup.'],
 "task":('**Input:** `data` has:\n'
    '- `items`: a list of `{"id": int, "name": string}`. IDs are unique positive integers.\n'
    '- `requests`: a list of `{"path": string, "method": string}`. Methods are uppercase.\n'
    '\n'
    'Process the requests in order. **Return** a list with one response object per request.\n'
    '\n'
    '**Routes:** paths must match exactly. There is no query parsing and no slash normalization.\n'
    '\n'
    '| Route | Allowed methods |\n'
    '| --- | --- |\n'
    '| `/health` | GET |\n'
    '| `/items` | GET |\n'
    '| `/items/N` | GET, DELETE |\n'
    '\n'
    '`N` matches only a canonical positive decimal number. For example, `/items/01`, `/items/0`, `/items/+1`, and `/items/1/` are unknown routes.\n'
    '\n'
    '**Responses**\n'
    '- `GET /health` → `{"status": 200, "body": {"status": "ok"}}`\n'
    '- `GET /items` → `{"status": 200, "body": [all items, sorted by id]}`\n'
    '- `GET /items/N` → `{"status": 200, "body": item}`\n'
    '- `DELETE /items/N` → remove the item and return `{"status": 204, "body": null}`\n'
    '- Item `N` does not exist → `{"status": 404, "body": {"error": "not_found"}}`\n'
    '- Unknown route → the same 404 response.\n'
    '- Known route, method not allowed → `{"status": 405, "body": {"error": "method_not_allowed"}, "allow": [...]}`. `allow` lists the allowed methods in the table order, for example `["GET", "DELETE"]`.\n'
    '\n'
    'On a known route, check the method before you check that the item exists. Only 405 responses have an `allow` field.'),"constraints":["0–100 items and 0–200 requests; ids and any numeric path suffix are at most 1000000.","Names and paths have at most 80 ASCII characters. Methods are GET, DELETE, POST, PUT, PATCH, or HEAD.","No network calls. Each solve call starts with its own items."],"hints":["Resolve the route before checking its method.","Copy each response representation before later mutations."],"starter":"def solve(data: dict) -> list:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"A dictionary stores current items. Route classification gives the allowed methods. Each response copies the current representation. For q requests and n items, item operations take expected O(1), while each collection response takes O(n log n) to sort. Memory includes stored items and output snapshots. Real routing frameworks and HTTP response writers perform more work than this simulation.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"treat successful delete as missing","old":"\"status\": 204","new":"\"status\": 404"}],"sources":["https://www.rfc-editor.org/rfc/rfc9110.html"]}
