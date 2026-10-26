"""A small conditional GET and ETag state machine."""
REF='''def solve(data):
    version, body = data["initial"]["version"], data["initial"]["body"]
    out = []
    for request in data["requests"]:
        if request["op"] == "put":
            version += 1
            body = request["body"]
            out.append({"status": 200, "etag": f'"v{version}"', "body": body})
            continue
        etag = f'"v{version}"'
        tags = request["tags"]
        matches = tags is not None and any(tag == "*" or (tag[2:] if tag.startswith("W/") else tag) == etag for tag in tags)
        out.append({"status": 304 if matches else 200, "etag": etag, "body": None if matches else body})
    return out
'''
JAVA='''public Object solve(Map<String,Object> d){
    Map<String,Object> initial=obj(d.get("initial"));int version=n(initial.get("version"));String body=s(initial.get("body"));List<Object> out=new ArrayList<>();
    for(Object value:arr(d.get("requests"))){Map<String,Object> r=obj(value);boolean put=s(r.get("op")).equals("put");if(put){version++;body=s(r.get("body"));}
        String etag="\\\"v"+version+"\\\"";boolean match=false;
        if(!put&&r.get("tags")!=null)for(Object valueTag:arr(r.get("tags"))){String tag=s(valueTag);if(tag.equals("*")||tag.equals(etag)||tag.equals("W/"+etag))match=true;}
        out.add(map("status",match?304:200,"etag",etag,"body",match?null:body));
    }return out;
}'''
def get(tags=None):return {"op":"get","tags":tags}
def put(body):return {"op":"put","body":body}
def ans(status=200,v=1,body="hello"):return {"status":status,"etag":f'"v{v}"',"body":body}
def case(requests,expected,label,version=1,body="hello"):return {"input":{"initial":{"version":version,"body":body},"requests":requests},"expected":expected,"label":label}
CASES=[case([get()],[ans()],"unconditional read returns representation"),case([get(['"v1"'])],[ans(304,body=None)],"matching tag avoids body"),case([put("new"),get(['"v1"'])],[ans(v=2,body="new"),ans(v=2,body="new")],"write invalidates old validator"),case([],[],"empty batch"),case([get([])],[ans()],"empty validator set"),case([get(['W/"v1"'])],[ans(304,body=None)],"weak tag matches for GET"),case([get(['*'])],[ans(304,body=None)],"wildcard matches existing representation"),case([get(['"v9"','"v1"'])],[ans(304,body=None)],"any listed tag can match"),case([get(['"v9"','W/"v2"'])],[ans()],"all tags stale"),case([put("hello"),get(['"v1"']),get(['"v2"'])],[ans(v=2),ans(v=2),ans(304,v=2,body=None)],"same body still increments version by local policy"),case([get()],[ans(body="")],"empty string is still a body",body=""),case([get(['"v10"'])],[ans(304,10,None)],"multi-digit version",version=10),case([put("a"),put("b"),get(['W/"v3"'])],[ans(v=2,body="a"),ans(v=3,body="b"),ans(304,3,None)],"successive writes and weak validation")]
GENERATED=[{"initial":{"version":i+2,"body":f"body{i}"},"requests":[get([f'"v{i+2}"']),put(f"next{i}"),get([f'W/"v{i+3}"']),get([f'"v{i+2}"'])]} for i in range(16)]
SPEC={"number":29,"slug":"etag-validation","title":"Validate cached representations with ETags","difficulty":"Medium","time":30,"prerequisites":"Problems 21–24; request contracts and versioned state.","learn":"A cached response can carry a validator called an entity tag, or ETag. The client later sends that tag with a conditional read. If it still matches, the server can return a not-modified response without the representation body. The client then keeps its cached body. For If-None-Match on GET, weak tags can match the same underlying tag value. A write can change the current validator. This exercise uses an integer version to create simple tags and supplies an already parsed list of client tags. It covers validation, not cache freshness, expiration, header parsing, or a complete HTTP cache implementation.","task":"`initial` is `{version:positive_int, body:string}`. Requests are `{op:\"put\", body:string}` or `{op:\"get\", tags:null|[tag,...]}`. The current strong ETag is the string `\"vN\"`, including its quote characters, where N is the version. Every put increments version by one, even for an unchanged body, and returns `{status:200, etag:current_tag, body:current_body}`. A get has no validator when tags is null. A supplied tag matches if it is `*`, the current strong tag, or `W/` followed by that strong tag. Any match returns `{status:304, etag:current_tag, body:null}`. Otherwise return status 200 with the body. Return responses in request order. The resource always exists. No actual header parser or network is required.","constraints":["0–200 requests; initial version is 1–1000000. Bodies are ASCII strings of length 0–200.","A tags list has 0–20 entries. Each is *, a quoted vN tag, or W/ followed by a quoted vN tag; N is 1–1000000.","Tags are pre-parsed; malformed tags and cache expiration are outside the domain."],"hints":["Use the same tag construction for reads and writes.","Remove W/ only for the comparison, not from the returned strong tag."],"starter":"def solve(data: dict) -> list:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"Track current version and body. Each GET compares the current strong tag with the supplied validators after weak-prefix normalization. For q requests and k tags per GET, time is O(qk), with O(q) output space. A production cache also needs freshness policy, Vary handling, and correct merging of validation metadata.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"ignore weak validators","old":"(tag[2:] if tag.startswith(\"W/\") else tag) == etag","new":"tag == etag"}],"sources":["https://www.rfc-editor.org/rfc/rfc9110.html#name-if-none-match","https://www.rfc-editor.org/rfc/rfc9111.html"]}
