"""Replacement, partial updates, and atomic validation."""
import random
REF='''def solve(data):
    state = dict(data["initial"])
    out = []
    for request in data["requests"]:
        body = request["body"]
        valid = isinstance(body, dict)
        if valid:
            valid = not (set(body) - {"name", "email"})
            valid = valid and (request["method"] != "PUT" or "name" in body)
            valid = valid and ("name" not in body or (isinstance(body["name"], str) and 1 <= len(body["name"]) <= 20))
            valid = valid and ("email" not in body or body["email"] is None or (isinstance(body["email"], str) and len(body["email"]) <= 30))
        if not valid:
            out.append({"status": 422, "body": {"error": "invalid"}})
            continue
        if request["method"] == "PUT":
            state = {"name": body["name"], "email": body.get("email")}
        else:
            for key in ("name", "email"):
                if key in body:
                    state[key] = body[key]
        out.append({"status": 200, "body": dict(state)})
    return {"responses": out, "state": state}
'''
JAVA='''public Object solve(Map<String,Object> d){
    Map<String,Object> state=new LinkedHashMap<>(obj(d.get("initial")));List<Object> out=new ArrayList<>();
    for(Object value:arr(d.get("requests"))){Map<String,Object> r=obj(value);Object raw=r.get("body");boolean put=s(r.get("method")).equals("PUT");
        boolean valid=raw instanceof Map;Map<String,Object> v=valid?obj(raw):new HashMap<>();
        valid=valid&&new HashSet<>(list("name","email")).containsAll(v.keySet())&&(!put||v.containsKey("name"));
        if(v.containsKey("name"))valid=valid&&v.get("name") instanceof String&&s(v.get("name")).length()>=1&&s(v.get("name")).length()<=20;
        if(v.containsKey("email"))valid=valid&&(v.get("email")==null||(v.get("email") instanceof String&&s(v.get("email")).length()<=30));
        if(!valid){out.add(map("status",422,"body",map("error","invalid")));continue;}
        if(put)state=map("name",v.get("name"),"email",v.get("email"));else state.putAll(v);
        out.add(map("status",200,"body",new LinkedHashMap<>(state)));
    }return map("responses",out,"state",state);
}'''
INITIAL={"name":"Ada","email":"a@x"}
def req(method,body):return {"method":method,"body":body}
def case(requests, states,label,initial=None):
    initial=INITIAL if initial is None else initial
    out=[]; final=dict(initial)
    for s in states:
        if s is None:out.append({"status":422,"body":{"error":"invalid"}})
        else:final=s;out.append({"status":200,"body":s})
    return {"input":{"initial":initial,"requests":requests},"expected":{"responses":out,"state":final},"label":label}
CASES=[case([req("PATCH",{"name":"Bo"})],[{"name":"Bo","email":"a@x"}],"PATCH keeps omitted email"),case([req("PUT",{"name":"Bo"})],[{"name":"Bo","email":None}],"PUT resets omitted email"),case([req("PATCH",{"email":None})],[{"name":"Ada","email":None}],"explicit null clears email"),case([],[],"no requests"),case([req("PATCH",{})],[INITIAL],"empty patch"),case([req("PUT",{})],[None],"replacement needs name"),case([req("PATCH",{"name":None})],[None],"name cannot be null"),case([req("PATCH",{"name":"Bo","email":7})],[None],"invalid update is atomic"),case([req("PATCH",{"extra":1})],[None],"unknown key"),case([req("PUT",{"name":"x"*20,"email":"y"*30})],[{"name":"x"*20,"email":"y"*30}],"length boundaries"),case([req("PUT",{"name":"x"*21})],[None],"name too long"),case([req("PATCH",{"email":""})],[{"name":"Ada","email":""}],"empty email stays empty"),case([req("PATCH",None),req("PUT",[])],[None,None],"non-object bodies"),case([req("PATCH",{"name":""})],[None],"empty name"),case([req("PATCH",{"name":"Bo"}),req("PUT",{"name":"Cy"}),req("PATCH",{"name":""})],[{"name":"Bo","email":"a@x"},{"name":"Cy","email":None},None],"snapshots and rejected later update")]
R=random.Random(23)
GENERATED=[{"initial":{"name":f"user{i}","email":None if i%2 else "x@y"},"requests":[req(R.choice(["PUT","PATCH"]),R.choice([{}, {"email":None},{"name":f"new{i}"},{"name":""},{"email":""},{"name":False}])) for _ in range(i+1)]} for i in range(16)]
SPEC={"number":23,"slug":"put-patch-fields","title":"Replace or patch a profile","difficulty":"Medium","time":30,"prerequisites":"Problems 21–22; dictionary membership and atomic state changes.","learn":"Replacement and partial update need different rules for absent fields. A replacement describes the new representation. A partial update changes selected fields in the current representation. An absent key is also different from a key whose value is null. For example, absence can preserve an email while null clears it. Validate the entire change before writing any field. Otherwise one invalid field can leave a partial update behind. HTTP PATCH does not prescribe one universal document format; this exercise defines its own two-field patch format. Its PUT rule also supplies a documented default. Both choices must be explicit to API clients.","task":('**Input:** `data` has:\n'
    '- `initial`: a valid profile `{"name": string, "email": string | null}`.\n'
    '- `requests`: a list of `{"method": "PUT" | "PATCH", "body": any JSON}`.\n'
    '\n'
    '**Valid body:** an object with no keys other than `name` and `email`.\n'
    '- `name`, if present: an ASCII string of length 1–20.\n'
    '- `email`, if present: `null` or an ASCII string of length 0–30. Do not check the email syntax.\n'
    '- A PUT body must contain `name`.\n'
    '\n'
    '**Rules**\n'
    '- PUT replaces the whole profile. `email` is `null` when the body omits it.\n'
    '- PATCH changes only the fields in the body. Omitted fields stay the same. `"email": null` clears the email. An empty PATCH body `{}` is valid.\n'
    '- Invalid body → `{"status": 422, "body": {"error": "invalid"}}`. Nothing changes.\n'
    '- Valid update → `{"status": 200, "body": the profile after the update}`.\n'
    '\n'
    '**Return** `{"responses": [...], "state": the final profile}`.'),"constraints":["0–200 requests. Bodies are decoded JSON values with at most 10 fields.","All strings have at most 100 ASCII characters. Initial profiles meet the same field limits.","Each call starts with its supplied initial state. No network calls."],"hints":["Membership tests distinguish absent fields from null values.","Build or validate a candidate state before committing it."],"starter":"def solve(data: dict) -> dict:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"Validate all fields before changing the current dictionary. PUT builds a replacement and PATCH applies only present keys. Copy the state into each successful response. Each request takes O(1) work under the two-field schema. Output uses O(q) space. Production APIs need a defined patch media type and concurrency control.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"drop explicit null patch","old":"if key in body:","new":"if key in body and body[key] is not None:"}],"sources":["https://www.rfc-editor.org/rfc/rfc9110.html#name-put","https://www.rfc-editor.org/rfc/rfc5789.html"]}
