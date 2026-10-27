"""Shared test driver (Python) and checker kit (Java) for the OOP course.

Every test input is ``{"ops": [step, ...]}``. The Python driver runs each step on
the learner's classes. The Java kit replays the same steps on an independent
Java model inside Marker. Both return one plain JSON value per step.
"""

DRIVER = '''

# ---------------------------------------------------------------------------
# Supplied test driver. Do not edit below this line.
# Each test is a list of steps. The driver runs every step on your classes and
# records its result, or {"error": "<ExceptionName>"} when the step raises.
# ---------------------------------------------------------------------------
import builtins as _builtins
import dataclasses as _dataclasses
import inspect as _inspect
import operator as _operator

_BINARY = {"+": _operator.add, "-": _operator.sub, "*": _operator.mul,
           "@": _operator.matmul, "==": _operator.eq, "!=": _operator.ne,
           "<": _operator.lt, "<=": _operator.le, ">": _operator.gt,
           ">=": _operator.ge, "in": lambda left, right: left in right}
_BUILTIN = {"repr": repr, "str": str, "len": len, "bool": bool,
            "list": list, "sorted": sorted}


def _lookup(name, env):
    if name in env:
        return env[name]
    if name in globals():
        return globals()[name]
    return getattr(_builtins, name)


def _value(raw, env):
    if isinstance(raw, dict) and list(raw) == ["ref"]:
        return env[raw["ref"]]
    if isinstance(raw, list):
        return [_value(item, env) for item in raw]
    if isinstance(raw, dict):
        return {key: _value(item, env) for key, item in raw.items()}
    return raw


def _plain(value):
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    return {"object": type(value).__name__}


def _check(step, env):
    kind = step["is"]
    if kind in ("instance", "callable"):
        target = _lookup(step["obj"], env)
        return callable(target) if kind == "callable" else isinstance(target, _lookup(step["of"], env))
    cls = _lookup(step["cls"], env)
    if kind == "mro":
        return [klass.__name__ for klass in cls.__mro__]
    if kind == "subclass":
        return issubclass(cls, _lookup(step["of"], env))
    if kind == "abstract":
        return _inspect.isabstract(cls)
    if kind == "dataclass":
        return _dataclasses.is_dataclass(cls)
    found = _inspect.getattr_static(cls, step["attr"], None)
    return isinstance(found, {"property": property, "staticmethod": staticmethod,
                              "classmethod": classmethod}[kind])


def _step(step, env):
    do = step["do"]
    args = _value(step.get("args", []), env)
    kwargs = _value(step.get("kwargs", {}), env)
    if do == "check":
        return _check(step, env)
    if do == "op":
        return _BINARY[step["op"]](_value(step["left"], env), _value(step["right"], env))
    target = _lookup(step.get("obj", step.get("cls")), env)
    if do == "new":
        return target(*args, **kwargs)
    if do == "get":
        return getattr(target, step["attr"])
    if do == "set":
        setattr(target, step["attr"], _value(step["value"], env))
        return None
    if do == "call":
        return getattr(target, step["method"])(*args, **kwargs)
    if do == "invoke":
        return target(*args, **kwargs)
    if do == "item":
        return target[_value(step["key"], env)]
    if do == "setitem":
        target[_value(step["key"], env)] = _value(step["value"], env)
        return None
    if do == "with":
        body = []
        try:
            with target as entered:
                if "as" in step:
                    env[step["as"]] = entered
                body.extend(_run(inner, env) for inner in step["body"])
                if "raise" in step:
                    raise getattr(_builtins, step["raise"])("raised by the test")
        except Exception as error:
            return {"body": body, "error": type(error).__name__}
        return {"body": body, "error": None}
    return _BUILTIN[do](target)


def _run(step, env):
    try:
        result = _step(step, env)
    except Exception as error:
        return {"error": type(error).__name__}
    if "save" in step:
        env[step["save"]] = result
    return _plain(result)


def solve(data):
    env = {}
    return [_run(step, env) for step in data["ops"]]
'''

JAVA_KIT = '''
static class Err extends RuntimeException {
    final String type;
    Err(String type) { super(type, null, false, false); this.type = type; }
}
static Err err(String type) { return new Err(type); }
interface Obj {
    String type();
    default Object plain() { return map("object", type()); }
    default Object enter() { throw err("AttributeError"); }
    default boolean exit(String error) { throw err("AttributeError"); }
}
Map<String,Object> env = new HashMap<>();
Object val(Object raw) {
    if (raw instanceof Map) {
        Map<String,Object> m = obj(raw);
        if (m.size() == 1 && m.containsKey("ref")) {
            if (!env.containsKey(s(m.get("ref")))) throw err("KeyError");
            return env.get(s(m.get("ref")));
        }
    }
    if (raw instanceof List) { List<Object> out = new ArrayList<>(); for (Object x : arr(raw)) out.add(val(x)); return out; }
    if (raw instanceof Map) { Map<String,Object> out = new LinkedHashMap<>(); for (Map.Entry<String,Object> e : obj(raw).entrySet()) out.put(e.getKey(), val(e.getValue())); return out; }
    return raw;
}
Object plain(Object x) {
    if (x instanceof Obj) return ((Obj) x).plain();
    if (x instanceof List) { List<Object> out = new ArrayList<>(); for (Object v : arr(x)) out.add(plain(v)); return out; }
    if (x instanceof Map) { Map<String,Object> out = new LinkedHashMap<>(); for (Map.Entry<String,Object> e : obj(x).entrySet()) out.put(e.getKey(), plain(e.getValue())); return out; }
    if (x instanceof Integer) return Long.valueOf((Integer) x);
    return x;
}
/** A saved object, or the class name as a String. */
Object target(Map<String,Object> op) {
    String name = s(op.containsKey("obj") ? op.get("obj") : op.get("cls"));
    return env.containsKey(name) ? env.get(name) : name;
}
List<Object> args(Map<String,Object> op) { return op.containsKey("args") ? arr(val(op.get("args"))) : list(); }
Map<String,Object> kwargs(Map<String,Object> op) { return op.containsKey("kwargs") ? obj(val(op.get("kwargs"))) : new HashMap<>(); }
Object arg(Map<String,Object> op, int i, String name, Object fallback) {
    List<Object> a = args(op); Map<String,Object> k = kwargs(op);
    if (i < a.size()) return a.get(i);
    if (k.containsKey(name)) return k.get(name);
    if (fallback == MISSING) throw err("TypeError");
    return fallback;
}
static final Object MISSING = new Object();
/** Python int check: a JSON integer that is not a boolean. */
static boolean isInt(Object x) { return isInteger(x); }
String typeName(Object x) {
    if (x instanceof Obj) return ((Obj) x).type();
    if (x instanceof String) return "str";
    if (x instanceof Boolean) return "bool";
    if (x instanceof List) return "list";
    if (x instanceof Map) return "dict";
    if (x == null) return "NoneType";
    return "int";
}
Object check(Map<String,Object> op) {
    String kind = s(op.get("is"));
    if (kind.equals("mro")) {
        String prefix = "mro " + s(op.get("cls")) + " ";
        for (String f : facts()) if (f.startsWith(prefix)) return new ArrayList<Object>(Arrays.asList(f.substring(prefix.length()).split(",")));
        throw err("AttributeError");
    }
    String subject = kind.equals("instance") || kind.equals("callable") ? typeName(env.get(s(op.get("obj")))) : s(op.get("cls"));
    String key = kind + " " + subject + (op.containsKey("attr") ? " " + s(op.get("attr")) : "") + (op.containsKey("of") ? " " + s(op.get("of")) : "");
    for (String f : facts()) if (f.equals(key)) return true;
    return false;
}
Object run1(Map<String,Object> op) {
    Object result;
    try { result = dispatch(op); }
    catch (Err e) { return map("error", e.type); }
    catch (ArithmeticException e) { return map("error", "ZeroDivisionError"); }
    catch (ClassCastException e) { return map("error", "AttributeError"); }
    if (op.containsKey("save")) env.put(s(op.get("save")), result);
    return plain(result);
}
Object dispatch(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("check")) return check(op);
    if (d.equals("with")) {
        Object t = target(op);
        if (!(t instanceof Obj)) throw err("AttributeError");
        Obj o = (Obj) t;
        List<Object> body = new ArrayList<>();
        Object entered;
        try { entered = o.enter(); } catch (Err e) { return map("body", body, "error", e.type); }
        if (op.containsKey("as")) env.put(s(op.get("as")), entered);
        for (Object inner : arr(op.get("body"))) body.add(run1(obj(inner)));
        String pending = op.containsKey("raise") ? s(op.get("raise")) : null;
        String error;
        try { error = o.exit(pending) ? null : pending; } catch (Err e) { error = e.type; }
        return map("body", body, "error", error);
    }
    return step(op);
}
public Object solve(Map<String,Object> d) {
    env = new HashMap<>();
    List<Object> out = new ArrayList<>();
    for (Object o : arr(d.get("ops"))) out.add(run1(obj(o)));
    return out;
}
'''
