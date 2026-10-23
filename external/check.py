"""Check the learner's existing file without copying answers or writing bytecode."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

# Hand-derived examples. Existing item rules form the regression boundary;
# the Conjured group checks the requested upstream extension.
SMOKE = [
    ("ordinary future", "Elixir of the Mongoose", 5, 7, 1, 4, 6),
    ("ordinary sell-in one", "+5 Dexterity Vest", 1, 8, 1, 0, 7),
    ("ordinary due", "+5 Dexterity Vest", 0, 8, 1, -1, 6),
    ("ordinary expired", "+5 Dexterity Vest", -2, 8, 1, -3, 6),
    ("ordinary floor", "+5 Dexterity Vest", 0, 1, 1, -1, 0),
    ("ordinary zero", "+5 Dexterity Vest", 3, 0, 1, 2, 0),
    ("brie increases", "Aged Brie", 2, 0, 1, 1, 1),
    ("brie expired", "Aged Brie", 0, 10, 1, -1, 12),
    ("brie cap", "Aged Brie", 0, 49, 1, -1, 50),
    ("brie already capped", "Aged Brie", 5, 50, 1, 4, 50),
    ("backstage eleven", "Backstage passes to a TAFKAL80ETC concert", 11, 20, 1, 10, 21),
    ("backstage ten", "Backstage passes to a TAFKAL80ETC concert", 10, 20, 1, 9, 22),
    ("backstage six", "Backstage passes to a TAFKAL80ETC concert", 6, 20, 1, 5, 22),
    ("backstage five", "Backstage passes to a TAFKAL80ETC concert", 5, 20, 1, 4, 23),
    ("backstage cap", "Backstage passes to a TAFKAL80ETC concert", 5, 49, 1, 4, 50),
    ("backstage last day", "Backstage passes to a TAFKAL80ETC concert", 1, 20, 1, 0, 23),
    ("backstage expired", "Backstage passes to a TAFKAL80ETC concert", 0, 20, 1, -1, 0),
    ("legendary", "Sulfuras, Hand of Ragnaros", 1, 80, 1, 1, 80),
    ("legendary expired", "Sulfuras, Hand of Ragnaros", -1, 80, 3, -1, 80),
    ("prefix must match", "Not Conjured Cake", 3, 8, 1, 2, 7),
    ("prefix case sensitive", "conjured cake", 3, 8, 1, 2, 7),
]
CONJURED = [
    ("conjured future", "Conjured Mana Cake", 3, 6, 1, 2, 4),
    ("conjured last day", "Conjured Mana Cake", 1, 8, 1, 0, 6),
    ("conjured due", "Conjured Mana Cake", 0, 8, 1, -1, 4),
    ("conjured expired", "Conjured Mana Cake", -2, 8, 1, -3, 4),
    ("conjured future floor", "Conjured Mana Cake", 3, 1, 1, 2, 0),
    ("conjured expired floor", "Conjured Mana Cake", 0, 3, 1, -1, 0),
    ("conjured zero", "Conjured Mana Cake", 0, 0, 1, -1, 0),
    ("conjured other product", "Conjured Elixir", 3, 8, 1, 2, 6),
    ("conjured crosses expiry", "Conjured Mana Cake", 1, 12, 3, -2, 2),
]


def check(workspace, smoke_only=False):
    source = workspace.resolve() / "gilded_rose.py"
    if not source.is_file():
        raise ValueError(f"No existe gilded_rose.py en {workspace}")
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(source.parent))
    spec = importlib.util.spec_from_file_location("gilded_rose", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    checks = []
    groups = [("smoke", SMOKE)]
    if not smoke_only:
        groups.append(("conjured", CONJURED))
    for group, cases in groups:
        for title, name, sell_in, quality, days, want_sell_in, want_quality in cases:
            item = module.Item(name, sell_in, quality)
            items = [item]
            rose = module.GildedRose(items)
            for _ in range(days):
                rose.update_quality()
            actual = [item.name, item.sell_in, item.quality]
            expected = [name, want_sell_in, want_quality]
            checks.append({"group": group, "name": title, "passed": actual == expected,
                           "actual": actual, "expected": expected})
    # Update all items in one call: an early return must not skip later items.
    mixed = [module.Item("Aged Brie", 2, 0), module.Item("Elixir", 1, 8)]
    expected = [["Aged Brie", 1, 1], ["Elixir", 0, 7]]
    if not smoke_only:
        mixed.insert(1, module.Item("Conjured Mana Cake", 0, 8))
        expected.insert(1, ["Conjured Mana Cake", -1, 4])
    module.GildedRose(mixed).update_quality()
    actual = [[item.name, item.sell_in, item.quality] for item in mixed]
    checks.append({"group": "smoke" if smoke_only else "conjured", "name": "mixed inventory",
                   "passed": actual == expected, "actual": actual, "expected": expected})
    return {"workspace": str(workspace.resolve()), "passed": all(c["passed"] for c in checks),
            "checks": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--smoke", action="store_true", help="Only check existing behavior")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        report = check(args.workspace, args.smoke)
    except Exception as error:
        print(f"Error al comprobar gilded_rose.py: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for case in report["checks"]:
            state = "PASS" if case["passed"] else "FAIL"
            print(f"{state} [{case['group']}] {case['name']}")
            if not case["passed"]:
                print(f"  expected: {case['expected']}; actual: {case['actual']}")
        print(f"{sum(c['passed'] for c in report['checks'])}/{len(report['checks'])} checks passed")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
