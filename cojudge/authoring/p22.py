"""Strict request bodies with deterministic error ordering."""
import random
REF='''import re

def solve(data):
    out = []
    for body in data["bodies"]:
        if not isinstance(body, dict):
            out.append({"status": 400, "errors": ["body"]})
            continue
        errors = []
        account = body.get("account")
        amount = body.get("amount")
        note = body.get("note")
        if not isinstance(account, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,11}", account):
            errors.append("account")
        if type(amount) is not int or not 1 <= amount <= 10000:
            errors.append("amount")
        if note is not None and (not isinstance(note, str) or len(note) > 20):
            errors.append("note")
        if set(body) - {"account", "amount", "note"}:
            errors.append("unknown")
        if errors:
            out.append({"status": 422, "errors": errors})
        else:
            out.append({"status": 201, "body": {"account": account, "amount": amount, "note": note}})
    return out
'''
JAVA='''public Object solve(Map<String,Object> d) {
    List<Object> out=new ArrayList<>();
    for(Object value:arr(d.get("bodies"))) {
        if(!(value instanceof Map)){out.add(map("status",400,"errors",list("body")));continue;}
        Map<String,Object> v=obj(value); Object account=v.get("account"), amount=v.get("amount"), note=v.get("note");
        List<Object> errors=new ArrayList<>();
        if(!(account instanceof String)||!s(account).matches("[a-z][a-z0-9_]{0,11}"))errors.add("account");
        boolean validAmount=isInteger(amount) && n(amount)>=1 && n(amount)<=10000;
        if(!validAmount)errors.add("amount");
        if(note!=null&&(!(note instanceof String)||s(note).length()>20))errors.add("note");
        if(!new HashSet<>(list("account","amount","note")).containsAll(v.keySet()))errors.add("unknown");
        if(errors.isEmpty())out.add(map("status",201,"body",map("account",account,"amount",amount,"note",note)));
        else out.add(map("status",422,"errors",errors));
    }return out;
}'''
def ok(a="a", n=1, note=None):return {"status":201,"body":{"account":a,"amount":n,"note":note}}
def err(*fields):return {"status":422,"errors":list(fields)}
def case(bodies, expected,label):return {"input":{"bodies":bodies},"expected":expected,"label":label}
CASES=[case([{"account":"acct_1","amount":25}],[ok("acct_1",25)],"valid body gets default null note"),case([{"account":"A","amount":0,"note":False,"extra":1}],[err("account","amount","note","unknown")],"all field errors have fixed order"),case([None],[{"status":400,"errors":["body"]}],"JSON null is not an object"),case([],[],"empty batch"),case([{}],[err("account","amount")],"required fields absent"),case([{"account":"a","amount":True}],[err("amount")],"boolean is not an amount"),case([{"account":"a","amount":1.0}],[err("amount")],"integral float is not an integer token"),case([{"account":"a","amount":1.5}],[err("amount")],"fractional amount is rejected"),case([{"account":"a","amount":1e2,"note":"exponent"}],[err("amount")],"exponent-decoded float is rejected"),case([{"account":"a","amount":10000}],[ok("a",10000)],"upper amount boundary"),case([{"account":"a","amount":10001}],[err("amount")],"amount exceeds boundary"),case([{"account":"a","amount":1,"note":"x"*20}],[ok(note="x"*20)],"note length boundary"),case([{"account":"a","amount":1,"note":"x"*21}],[err("note")],"note too long"),case([{"account":"a"*12,"amount":1}],[ok("a"*12)],"account length boundary"),case([{"account":"a"*13,"amount":1}],[err("account")],"account too long"),case([[],"text",7],[{"status":400,"errors":["body"]}]*3,"non-object shapes"),case([{"account":"a","amount":"1"}],[err("amount")],"do not coerce strings"),case([{"account":"a\n","amount":1}],[err("account")],"full string match"),case([{"account":"a","amount":1,"note":""},{"account":"a","amount":1,"note":None}],[ok(note=""),ok()],"empty and null notes remain distinct")]
R=random.Random(22)
GENERATED=[{"bodies":[{"account":f"acct_{i}","amount":R.choice([0,1,1.0,1.5,9999,10000,10001,False]),"note":"n"*(i%23)}, {"account":"bad-"+str(i),"amount":i+1}]} for i in range(18)]
SPEC={"number":22,"slug":"body-validation","title":"Validate a request body","difficulty":"Easy","time":25,"prerequisites":"Problem 21; strict Python type checks and regular expressions.","learn":"A JSON parser can accept a value that your API cannot use. Validation is a separate boundary. First check the whole body shape. Then check required fields, types, ranges, and unknown keys. Do not silently turn a string into a number unless the contract permits that conversion. Python needs care because bool is a subclass of int. Error ordering is part of this exercise's contract, so clients can compare responses reliably. The status choices below are a local API policy, not a claim that every service uses the same validation convention. A successful result includes explicit defaults for optional fields.","task":"`data.bodies` is a list of decoded JSON values. Return one response per body. A non-object body returns `{status:400, errors:[\"body\"]}`. An object allows only `account`, `amount`, and optional `note`. `account` is required and must fully match `[a-z][a-z0-9_]{0,11}`. `amount` is required and must be a JSON integer from 1 through 10000, excluding booleans and floats. For example, `1` is an integer token but `1.0` and `1e0` are not. `note` defaults to null and must be null or an ASCII string of at most 20 characters. On invalid fields return status 422 with `errors` in this exact order: account, amount, note, unknown. Include only failed checks. Use one `unknown` entry if any unknown key exists. Otherwise return `{status:201, body:{account:..., amount:..., note:...}}`. Do not include errors in a success response. Do not trim or coerce input.","constraints":["0–200 bodies. Every string and object key is ASCII and at most 100 characters.","Numeric inputs are finite JSON numbers in [-100000,100000]. Decimal or exponent notation decodes as float and must fail the amount check.","Bodies and field values may have any JSON type. Nested lists and objects have at most 10 elements."],"hints":["Check body shape before reading fields.","Use type(value) is int to exclude booleans."],"starter":"def solve(data: dict) -> list:\n    raise NotImplementedError\n","reference":REF,"java":JAVA,"approach":"Validate each body without changing it. Accumulate field names in contract order, then build one response. Time is linear in the number of input fields and characters. Output space is linear in the number of bodies. Real APIs also limit byte size and nesting before decoding.","cases":CASES,"generated":GENERATED,"mutations":[{"name":"accept booleans as integer amounts","old":"type(amount) is not int","new":"not isinstance(amount, int)"},{"name":"accept integral and fractional floats as amounts","old":"type(amount) is not int","new":"type(amount) not in (int, float)"}],"sources":["https://docs.python.org/3/library/stdtypes.html#boolean-type-bool","https://www.rfc-editor.org/rfc/rfc9110.html"]}
