"""Short constructors for test steps and expected results in the OOP specs."""


def _save(step, save):
    if save:
        step["save"] = save
    return step


def new(cls, *args, save=None, **kwargs):
    step = {"do": "new", "cls": cls, "args": list(args)}
    if kwargs:
        step["kwargs"] = kwargs
    return _save(step, save)


def get(obj, attr, save=None):
    return _save({"do": "get", "obj": obj, "attr": attr}, save)


def put(obj, attr, value):
    return {"do": "set", "obj": obj, "attr": attr, "value": value}


def call(obj, method, *args, save=None, **kwargs):
    step = {"do": "call", "obj": obj, "method": method, "args": list(args)}
    if kwargs:
        step["kwargs"] = kwargs
    return _save(step, save)


def invoke(obj, *args, save=None):
    return _save({"do": "invoke", "obj": obj, "args": list(args)}, save)


def op(left, symbol, right, save=None):
    return _save({"do": "op", "op": symbol, "left": left, "right": right}, save)


def item(obj, key):
    return {"do": "item", "obj": obj, "key": key}


def setitem(obj, key, value):
    return {"do": "setitem", "obj": obj, "key": key, "value": value}


def builtin(name, obj, save=None):
    return _save({"do": name, "obj": obj}, save)


def check(kind, subject, attr=None, of=None):
    step = {"do": "check", "is": kind}
    step["obj" if kind in ("instance", "callable") else "cls"] = subject
    if attr is not None:
        step["attr"] = attr
    if of is not None:
        step["of"] = of
    return step


def with_(obj, body, as_=None, raise_=None):
    step = {"do": "with", "obj": obj, "body": body}
    if as_:
        step["as"] = as_
    if raise_:
        step["raise"] = raise_
    return step


def ref(name):
    return {"ref": name}


def error(name):
    return {"error": name}


def obj(cls):
    return {"object": cls}


def case(label, *pairs):
    """case("label", (step, expected), ...) keeps each step next to its answer."""
    return {"label": label, "ops": [p[0] for p in pairs], "expected": [p[1] for p in pairs]}
