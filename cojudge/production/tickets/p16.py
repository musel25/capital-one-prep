"""Apply atomic transfers between account balances."""


def transfer(source, target, amount):
    return {"from": source, "to": target, "amount": amount}


def case(balances, transfers, accepted, remaining, label):
    return {"input": {"balances": balances, "transfers": transfers},
            "expected": {"accepted": accepted, "balances": remaining}, "label": label}


CASES = [
    case({}, [], [], {}, "empty accounts and transfers"),
    case({"a": 50, "b": 0}, [], [], {"a": 50, "b": 0}, "no transfers preserve balances"),
    case({"a": 50, "b": 10}, [transfer("a", "b", 20)], [True],
         {"a": 30, "b": 30}, "successful transfer debits and credits"),
    case({"a": 50, "b": 0}, [transfer("a", "b", 50)], [True],
         {"a": 0, "b": 50}, "exact source balance is sufficient"),
    case({"a": 50, "b": 0}, [transfer("a", "b", 51)], [False],
         {"a": 50, "b": 0}, "insufficient funds change neither account"),
    case({"a": 10}, [transfer("missing", "a", 1)], [False],
         {"a": 10}, "missing source is not created"),
    case({"a": 10}, [transfer("a", "missing", 1)], [False],
         {"a": 10}, "missing target does not debit source"),
    case({}, [transfer("a", "b", 1)], [False], {}, "both accounts missing"),
    case({"a": 10}, [transfer("a", "a", 10)], [True],
         {"a": 10}, "funded self-transfer is a no-op"),
    case({"a": 10}, [transfer("a", "a", 11)], [False],
         {"a": 10}, "self-transfer still checks funds"),
    case({"a": 0, "b": 1}, [transfer("a", "b", 1)], [False],
         {"a": 0, "b": 1}, "zero balance rejects positive transfer"),
    case({"a": 5, "b": 0, "c": 0}, [transfer("a", "b", 5), transfer("b", "c", 3)],
         [True, True], {"a": 0, "b": 2, "c": 3}, "later transfer uses credited funds"),
    case({"a": 5, "b": 0}, [transfer("a", "b", 6), transfer("a", "b", 5)],
         [False, True], {"a": 0, "b": 5}, "rejected transfer leaves funds available"),
    case({"a": 5, "b": 0}, [transfer("a", "b", 3), transfer("a", "b", 3)],
         [True, False], {"a": 2, "b": 3}, "repeat transfer is a new request"),
    case({"A": 7, "a": 1}, [transfer("A", "a", 2), transfer("a", "A", 3)],
         [True, True], {"A": 8, "a": 0}, "account names are case sensitive"),
    case({"large": 1000000000000, "other": 1000000000000},
         [transfer("large", "other", 1000000000000)], [True],
         {"large": 0, "other": 2000000000000}, "balances use integer cents beyond 32 bits"),
    case({"O'Brien": 4, "x; DROP TABLE balances;--": 0},
         [transfer("O'Brien", "x; DROP TABLE balances;--", 3)], [True],
         {"O'Brien": 1, "x; DROP TABLE balances;--": 3}, "account names are literal data"),
]

CASES = [CASES[2], CASES[4], CASES[6]] + [case for i, case in enumerate(CASES) if i not in (2, 4, 6)]

SPEC = {
    "number": 16,
    "slug": "atomic-transfers",
    "title": "Apply account transfers atomically",
    "difficulty": "Hard",
    "category": "04-jobs-and-storage",
    "ticket": "A balance service must apply each transfer without a partial debit or credit.",
    "task": "Implement `apply_transfers(balances, transfers)`. `balances` maps account names to "
            "integer cents. Each transfer has `from`, `to`, and `amount`. Process transfers in "
            "input order. Accept only when both accounts exist and the source has at least "
            "`amount` cents. On success, subtract from the source and add to the target as one "
            "atomic change. A self-transfer succeeds only when funds are sufficient and leaves "
            "the balance unchanged. Rejected transfers change no balances and create no accounts. "
            "Return `{\"accepted\": [...], \"balances\": {...}}` with one boolean per transfer and "
            "every final account balance. Empty inputs are allowed. Do not modify the inputs. "
            "Calls are independent.",
    "constraints": ["0–300 accounts and 0–300 transfers. All required fields are present.",
                    "Account names are nonempty ASCII strings of at most 80 characters.",
                    "Initial balances are integers from 0 to 1000000000000 cents; amounts are integers from 1 to 1000000000000 cents.",
                    "Inputs satisfy the contract; no validation is required."],
    "function": "apply_transfers",
    "starter": "def apply_transfers(balances, transfers):\n    raise NotImplementedError\n",
    "reference": '''import sqlite3


def apply_transfers(balances, transfers):
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE TABLE balances (account TEXT PRIMARY KEY, cents INTEGER NOT NULL CHECK(cents >= 0))")
        db.executemany("INSERT INTO balances VALUES (?, ?)", balances.items())
        db.commit()
        accepted = []
        for transfer in transfers:
            source_name, target_name = transfer["from"], transfer["to"]
            amount = transfer["amount"]
            with db:
                db.execute("BEGIN")
                source = db.execute("SELECT cents FROM balances WHERE account = ?", (source_name,)).fetchone()
                target = db.execute("SELECT cents FROM balances WHERE account = ?", (target_name,)).fetchone()
                ok = source is not None and target is not None and source[0] >= amount
                if ok:
                    db.execute("UPDATE balances SET cents = cents + ? WHERE account = ?", (-amount, source_name))
                    db.execute("UPDATE balances SET cents = cents + ? WHERE account = ?", (amount, target_name))
                accepted.append(ok)
        remaining = dict(db.execute("SELECT account, cents FROM balances"))
        return {"accepted": accepted, "balances": remaining}
    finally:
        db.close()
''',
    "java": '''public Object solve(Map<String,Object> d) {
    Map<String,Object> balances = new LinkedHashMap<>(obj(d.get("balances")));
    List<Object> accepted = new ArrayList<>();
    for (Object raw : arr(d.get("transfers"))) {
        Map<String,Object> transfer = obj(raw);
        String source = s(transfer.get("from")), target = s(transfer.get("to"));
        long amount = lng(transfer.get("amount"));
        boolean ok = balances.containsKey(source) && balances.containsKey(target)
                     && lng(balances.get(source)) >= amount;
        if (ok && !source.equals(target)) {
            long debit = lng(balances.get(source)) - amount;
            long credit = lng(balances.get(target)) + amount;
            balances.put(source, debit);
            balances.put(target, credit);
        }
        accepted.add(ok);
    }
    return map("accepted", accepted, "balances", balances);
}''',
    "cases": CASES,
    "mutations": [
        {"name": "rejects_exact_balance", "old": 'source[0] >= amount',
         "new": 'source[0] > amount'},
        {"name": "missing_target_still_debits_source", "old": 'target is not None',
         "new": 'True'},
        {"name": "credits_without_debiting", "old": '(-amount, source_name)',
         "new": '(0, source_name)'},
    ],
}
