class Animal:
    sound = "..."
    legs = 0

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} says {self.sound}"


class Lion(Animal):
    sound = "roar"
    legs = 4


class Parrot(Animal):
    sound = "squawk"
    legs = 2


class Snake(Animal):
    sound = "hiss"
    legs = 0


class Zoo:
    KINDS = {"lion": Lion, "parrot": Parrot, "snake": Snake}

    def __init__(self, name: str):
        self.name = name
        self._next = 1
        self._animals: dict[int, Animal] = {}

    def admit(self, kind: str, name: str) -> int:
        if kind not in self.KINDS:
            raise ValueError(f"unknown kind: {kind!r}")
        number = self._next
        self._next += 1
        self._animals[number] = self.KINDS[kind](name)
        return number

    def animal(self, number: int) -> Animal:
        return self._animals[number]

    def release(self, number: int) -> str:
        return self._animals.pop(number).name

    def roster(self) -> list[str]:
        return [f"#{number} {a.name} ({type(a).__name__})" for number, a in self._animals.items()]

    def total_legs(self) -> int:
        return sum(a.legs for a in self._animals.values())


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

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
