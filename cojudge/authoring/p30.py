"""A bounded upstream pagination client with failure guards."""
REF='''def solve(data):
    cursor = data["start"]
    seen_cursors = set()
    seen_ids = set()
    requests = []
    items = []
    error = None
    while cursor is not None:
        if cursor in seen_cursors:
            error = "cycle"
            break
        if len(requests) >= data["max_pages"]:
            error = "limit"
            break
        seen_cursors.add(cursor)
        requests.append(cursor)
        page = data["pages"].get(cursor)
        if page is None:
            error = "missing"
            break
        if page["status"] != 200:
            error = "upstream"
            break
        for item in page["items"]:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                items.append(dict(item))
        cursor = page["next"]
    return {"items": items, "requests": requests, "error": error}
'''
JAVA='''public Object solve(Map<String,Object> d){
    Map<String,Object> pages=obj(d.get("pages"));String cursor=s(d.get("start")),error=null;Set<String> seen=new HashSet<>();Set<Integer> ids=new HashSet<>();List<Object> requests=new ArrayList<>(),items=new ArrayList<>();
    while(cursor!=null){if(seen.contains(cursor)){error="cycle";break;}if(requests.size()>=n(d.get("max_pages"))){error="limit";break;}seen.add(cursor);requests.add(cursor);
        if(!pages.containsKey(cursor)){error="missing";break;}Map<String,Object> p=obj(pages.get(cursor));if(n(p.get("status"))!=200){error="upstream";break;}
        for(Object item:arr(p.get("items")))if(ids.add(n(obj(item).get("id"))))items.add(item);
        cursor=p.get("next")==null?null:s(p.get("next"));
    }return map("items",items,"requests",requests,"error",error);
}'''
def item(i,v=None):return {"id":i,"value":str(i) if v is None else v}
def page(items=(),next=None):return {"status":200,"items":list(items),"next":next}
def case(pages,maximum,items,requests,error,label,start="a"):return {"input":{"pages":pages,"start":start,"max_pages":maximum},"expected":{"items":items,"requests":requests,"error":error},"label":label}
A=item(1);B=item(2)
CASES=[case({"a":page([A],"b"),"b":page([A,B])},5,[A,B],["a","b"],None,"deduplicate across pages"),case({"a":page([A],"a")},5,[A],["a"],"cycle","stop before fetching a repeated cursor"),case({"a":page([A],"b"),"b":{"status":503}},5,[A],["a","b"],"upstream","preserve earlier data on failure"),case({"a":page()},1,[],["a"],None,"empty final page"),case({},2,[],["a"],"missing","missing initial fixture"),case({"a":page([A],"b")},2,[A],["a","b"],"missing","missing later page"),case({"a":page([A],"b"),"b":page([B])},1,[A],["a"],"limit","limit prevents next request"),case({"a":page([A])},1,[A],["a"],None,"final page exactly at limit succeeds"),case({"a":page([A,item(1,"changed"),B])},2,[A,B],["a"],None,"first occurrence wins within page"),case({"a":page([],"b"),"b":page([B])},2,[B],["a","b"],None,"empty page with next is not completion"),case({"a":page([A],"b"),"b":page([B],"a")},2,[A,B],["a","b"],"cycle","cycle has priority over page limit"),case({"a":{"status":429}},3,[],["a"],"upstream","client does not retry upstream errors"),case({"other":page([B]),"a":page([A])},2,[B],["other"],None,"supplied start cursor" ,start="other"),case({"a":page([A],"b"),"b":page([item(1,"new")])},2,[A],["a","b"],None,"do not replace first item value")]
GENERATED=[]
for i in range(18):
    count=i%6+1
    pages={f"p{j}":page([item(j),item((j+i)%5,f"v{i}")],f"p{j+1}" if j+1<count else ("p0" if i%3==0 else None)) for j in range(count)}
    GENERATED.append({"start":"p0","pages":pages,"max_pages":i%7+1})
SPEC={"number":30,"slug":"upstream-page-client","title":"Build a guarded upstream page client","difficulty":"Hard","time":40,"prerequisites":"Problems 21–29; sets, pagination, and bounded client policies.","learn":"A pagination client needs a completion condition and guards against faulty upstream behavior. An empty page can still point to another page. Repeated records need a documented merge rule. A repeated cursor can create an infinite loop unless the client remembers which cursors it already requested. A separate page cap also stops a long chain of distinct cursors. Decide what happens to useful data when a later page fails. This exercise keeps the accepted prefix and reports the failure. The pages are supplied fixtures, so the client makes no network calls. Combining these rules checks control flow that a single happy-path page cannot reveal.","task":"Input has `start` cursor, `max_pages`, and `pages`, an object mapping cursors to page fixtures. Successful pages are `{status:200, items:[{id:int,value:string},...], next:string|null}`. Error pages contain only status, either 429 or 500–599. Begin at start. Before each fetch: first stop with error cycle if this cursor was already requested; otherwise stop with limit if max_pages were requested. Append the cursor to requests. A missing fixture stops with missing. An error page stops with upstream. Successful pages append only the first occurrence of each item id, preserving traversal order and its first value. Follow next even after an empty items list. Null next ends successfully. Return `{items:[...], requests:[cursor,...], error:null|\"cycle\"|\"limit\"|\"missing\"|\"upstream\"}`. Keep earlier items on failure. Do not retry. Unreachable fixtures are ignored.","constraints":["1–20 max_pages; 0–30 page fixtures; 0–30 items per page.","Cursors are nonempty ASCII strings of at most 30 characters. Ids are 0–1000000 and values are ASCII strings of length 0–50.","Repeated ids may have different values. Repeated cursors and missing fixtures are valid test inputs."],"hints":["Use separate sets for visited cursors and accepted item ids.","Check cycle before limit, then record an attempted fetch before looking up its fixture."],"starter":"def solve(data: dict) -> dict:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"A cursor set prevents repeated fetches and an id set preserves the first item for each id. The explicit cap bounds work even without a cycle. Expected time is O(p+i), where p is requested pages and i is items inspected. Extra space is O(p+i). Real clients must add transport errors, response validation, deadlines, and a suitable retry policy.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"stop at an empty page despite its next cursor","old":"cursor = page[\"next\"]","new":"cursor = page[\"next\"] if page[\"items\"] else None"}],"sources":["https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api","https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset"]}
