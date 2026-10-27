"""Original exercise: evaluate a bridge hand with a class."""
from cojudge.oop.steps import builtin, call, case, error, get, new, obj

DECK = [s + r for s in "SHDC" for r in "23456789TJQKA"]

SPEC = {
    "number": 22, "slug": "bridge-hand", "title": "Evaluate a bridge hand",
    "difficulty": "Hard", "time": 45, "level": 5,
    "prerequisites": "Levels 1–4. Properties, `__str__`, and validation in `__init__`.",
    "learn": """A domain class turns raw data into answers with names. Validate the raw data once in
`__init__`, keep it private, and expose each answer as a property. Each property is short
because it can use the others: `balanced` uses `shape`, and `shape` uses `lengths`.

**Bridge basics** for this exercise. A deck has 52 cards: 4 suits, spades `S`, hearts `H`,
diamonds `D`, and clubs `C`, with 13 ranks each, from low to high `2 3 4 5 6 7 8 9 T J Q K A`
(`T` is ten). A player gets 13 cards. Players evaluate a hand with simple counts:

- **High card points (HCP):** ace 4, king 3, queen 2, jack 1.
- **Shape:** the four suit lengths, sorted from long to short, such as `5-4-3-1`.
- **Losing trick count:** for each suit, look at its `min(length, 3)` highest cards. Count one
  loser for each of those positions that is not filled by the matching honor, A, K, Q in order.

`"23456789TJQKA".index(rank)` gives a rank's strength for sorting.""",
    "scenario": """A bridge training app shows a hand and asks the student to evaluate it. The app
then shows the correct counts and a suggested opening bid from a simplified practice system, so
the student can check their work.""",
    "task": """Write the class `Hand`. A card is a two-character string: a suit (`S`, `H`, `D`,
`C`) and a rank (`2`–`9`, `T`, `J`, `Q`, `K`, `A`), all uppercase.

- `Hand(cards)`: a list of exactly 13 different valid cards; otherwise raise `ValueError`.
- `hcp`: property. High card points (A 4, K 3, Q 2, J 1).
- `lengths`: property. `{"S": n, "H": n, "D": n, "C": n}`.
- `shape`: property. The four lengths from long to short, joined with `-`, such as `"5-4-3-1"`.
- `balanced`: property. `True` when the shape is `4-3-3-3`, `4-4-3-2`, or `5-3-3-2`.
- `losers`: property. The losing trick count: for each suit with `n` cards, `min(n, 3)` minus the
  number of honors from `"AKQ"[:min(n, 3)]` in that suit. Add the four suits.
  Examples: void 0, `A` 0, `K` 1, `KQ` 1, `Qx` 2, `AKx` 1, `KQJ` 1, `xxxx` 3.
- `str(hand)`: `"S: <ranks> | H: <ranks> | D: <ranks> | C: <ranks>"`, ranks high to low with no
  spaces, `-` for a void. Example: `S: AK72 | H: QJ5 | D: A98 | C: K43`.
- `opening()`: the first rule that matches:
  1. HCP ≥ 22: `"2C"`.
  2. Balanced and HCP 15–17: `"1NT"`.
  3. Balanced and HCP 20–21: `"2NT"`.
  4. HCP ≥ 12: `"1"` + the longest suit. For equal lengths, use the first suit in `S H D C`.
  5. Otherwise `"pass"`.

The card order in the input does not matter.""",
    "constraints": ["At most 30 steps per test."],
    "hints": ["Write a helper that returns the ranks of one suit, sorted high to low; most properties use it.",
              "`max(\"SHDC\", key=lambda s: lengths[s])` returns the first suit with the greatest length."],
    "starter": '''class Hand:
    def __init__(self, cards: list[str]):
        raise NotImplementedError

    @property
    def hcp(self) -> int:
        raise NotImplementedError

    @property
    def lengths(self) -> dict[str, int]:
        raise NotImplementedError

    @property
    def shape(self) -> str:
        raise NotImplementedError

    @property
    def balanced(self) -> bool:
        raise NotImplementedError

    @property
    def losers(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def opening(self) -> str:
        raise NotImplementedError
''',
    "reference": '''SUITS = "SHDC"
RANKS = "23456789TJQKA"
POINTS = {"A": 4, "K": 3, "Q": 2, "J": 1}
BALANCED = {"4-3-3-3", "4-4-3-2", "5-3-3-2"}


class Hand:
    def __init__(self, cards: list[str]):
        if len(cards) != 13 or len(set(cards)) != 13:
            raise ValueError("a hand has 13 different cards")
        for card in cards:
            if not isinstance(card, str) or len(card) != 2 or card[0] not in SUITS or card[1] not in RANKS:
                raise ValueError(f"invalid card: {card!r}")
        self._cards = list(cards)

    def _ranks(self, suit: str) -> list[str]:
        return sorted((card[1] for card in self._cards if card[0] == suit), key=RANKS.index, reverse=True)

    @property
    def hcp(self) -> int:
        return sum(POINTS.get(card[1], 0) for card in self._cards)

    @property
    def lengths(self) -> dict[str, int]:
        return {suit: len(self._ranks(suit)) for suit in SUITS}

    @property
    def shape(self) -> str:
        return "-".join(str(n) for n in sorted(self.lengths.values(), reverse=True))

    @property
    def balanced(self) -> bool:
        return self.shape in BALANCED

    @property
    def losers(self) -> int:
        total = 0
        for suit in SUITS:
            ranks = self._ranks(suit)
            considered = min(len(ranks), 3)
            total += considered - sum(1 for honor in "AKQ"[:considered] if honor in ranks)
        return total

    def __str__(self) -> str:
        return " | ".join(f"{suit}: {''.join(self._ranks(suit)) or '-'}" for suit in SUITS)

    def opening(self) -> str:
        points = self.hcp
        if points >= 22:
            return "2C"
        if self.balanced and 15 <= points <= 17:
            return "1NT"
        if self.balanced and 20 <= points <= 21:
            return "2NT"
        if points >= 12:
            lengths = self.lengths
            return "1" + max(SUITS, key=lambda suit: lengths[suit])
        return "pass"
''',
    "facts": ["property Hand hcp", "property Hand shape", "property Hand losers"],
    "java": '''static final String SUITS = "SHDC", RANKS = "23456789TJQKA";
static class Hand implements Obj {
    List<String> cards = new ArrayList<>();
    public String type() { return "Hand"; }
    String ranks(char suit) {
        List<Character> r = new ArrayList<>();
        for (String c : cards) if (c.charAt(0) == suit) r.add(c.charAt(1));
        r.sort((a, b) -> RANKS.indexOf(b) - RANKS.indexOf(a));
        StringBuilder sb = new StringBuilder(); for (char c : r) sb.append(c); return sb.toString();
    }
    long hcp() { long t = 0; for (String c : cards) t += "JQKA".indexOf(c.charAt(1)) + 1; return t; }
    String shape() {
        List<Integer> n = new ArrayList<>(); for (char s : SUITS.toCharArray()) n.add(ranks(s).length());
        n.sort(Collections.reverseOrder());
        return n.get(0) + "-" + n.get(1) + "-" + n.get(2) + "-" + n.get(3);
    }
    boolean balanced() { String s = shape(); return s.equals("4-3-3-3") || s.equals("4-4-3-2") || s.equals("5-3-3-2"); }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) {
        Hand h = new Hand();
        List<Object> raw = arr(arg(op, 0, "cards", MISSING));
        if (raw.size() != 13 || new HashSet<>(raw).size() != 13) throw err("ValueError");
        for (Object c : raw) {
            if (!(c instanceof String) || s(c).length() != 2 || SUITS.indexOf(s(c).charAt(0)) < 0 || RANKS.indexOf(s(c).charAt(1)) < 0) throw err("ValueError");
            h.cards.add(s(c));
        }
        return h;
    }
    Hand h = (Hand) target(op);
    if (d.equals("get")) {
        switch (s(op.get("attr"))) {
            case "hcp": return h.hcp();
            case "lengths": { Map<String,Object> m = new LinkedHashMap<>(); for (char su : SUITS.toCharArray()) m.put(String.valueOf(su), (long) h.ranks(su).length()); return m; }
            case "shape": return h.shape();
            case "balanced": return h.balanced();
            case "losers": {
                long total = 0;
                for (char su : SUITS.toCharArray()) {
                    String r = h.ranks(su); int k = Math.min(r.length(), 3);
                    total += k; for (char honor : "AKQ".substring(0, k).toCharArray()) if (r.indexOf(honor) >= 0) total--;
                }
                return total;
            }
        }
    }
    if (d.equals("str")) {
        List<String> parts = new ArrayList<>();
        for (char su : SUITS.toCharArray()) { String r = h.ranks(su); parts.add(su + ": " + (r.isEmpty() ? "-" : r)); }
        return String.join(" | ", parts);
    }
    if (d.equals("call") && s(op.get("method")).equals("opening")) {
        long p = h.hcp();
        if (p >= 22) return "2C";
        if (h.balanced() && p >= 15 && p <= 17) return "1NT";
        if (h.balanced() && p >= 20 && p <= 21) return "2NT";
        if (p >= 12) { char best = 'S'; for (char su : SUITS.toCharArray()) if (h.ranks(su).length() > h.ranks(best).length()) best = su; return "1" + best; }
        return "pass";
    }
    throw err("AttributeError");
}
''',
    "approach": """`__init__` validates count, uniqueness, and each card, then stores a private copy.
One helper, `_ranks(suit)`, sorts a suit high to low, and every property builds on it or on
another property, so each rule appears once. `opening` checks its rules in the stated order;
`max` over `"SHDC"` returns the first suit among equal lengths. The opening rules are a
simplified practice system, not a complete bidding system.""",
    "example_notes": [
        "HCP: A 4 + K 3 + Q 2 + J 1 + A 4 + K 3 = 17. Shape 4-3-3-3 is balanced, so the opening is 1NT.",
        "Spades AKx is 1 loser, hearts KQ 1, diamonds Qx 2, clubs 7 cards with A only: 2. Total 6.",
        "A 12-card list and a duplicate card are both invalid.",
    ],
    "cases": [
        case("balanced 1NT",
             (new("Hand", ["SA", "SK", "S7", "S2", "HQ", "HJ", "H5", "DA", "D9", "D8", "CK", "C4", "C3"], save="h"), obj("Hand")),
             (get("h", "hcp"), 17), (get("h", "shape"), "4-3-3-3"), (call("h", "opening"), "1NT"),
             (builtin("str", "h"), "S: AK72 | H: QJ5 | D: A98 | C: K43")),
        case("losing trick count",
             (new("Hand", ["SA", "SK", "S3", "HK", "HQ", "DQ", "D4", "CA", "C9", "C8", "C7", "C6", "C5"], save="h"), obj("Hand")),
             (get("h", "losers"), 6), (get("h", "lengths"), {"S": 3, "H": 2, "D": 2, "C": 6})),
        case("invalid card lists",
             (new("Hand", DECK[:12]), error("ValueError")),
             (new("Hand", ["SA", "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "ST", "SJ", "SQ"]), error("ValueError"))),
        case("invalid card strings",
             (new("Hand", ["sa"] + DECK[1:13]), error("ValueError")), (new("Hand", ["S10"] + DECK[1:13]), error("ValueError")),
             (new("Hand", ["X2"] + DECK[1:13]), error("ValueError")), (new("Hand", ["S1"] + DECK[1:13]), error("ValueError"))),
        case("thirteen spades",
             (new("Hand", DECK[:13], save="h"), obj("Hand")), (get("h", "shape"), "13-0-0-0"), (get("h", "hcp"), 10),
             (get("h", "losers"), 0), (builtin("str", "h"), "S: AKQJT98765432 | H: - | D: - | C: -"), (call("h", "opening"), "pass")),
        case("strong hand opens 2C",
             (new("Hand", ["SA", "SK", "SQ", "SJ", "HA", "HK", "HQ", "DA", "DK", "D2", "C4", "C3", "C2"], save="h"), obj("Hand")),
             (get("h", "hcp"), 26), (get("h", "balanced"), True), (call("h", "opening"), "2C")),
        case("2NT range",
             (new("Hand", ["SA", "SK", "S5", "S4", "HA", "HJ", "H3", "DK", "DQ", "D2", "CA", "C9", "C8"], save="h"), obj("Hand")),
             (get("h", "hcp"), 21), (get("h", "shape"), "4-3-3-3"), (call("h", "opening"), "2NT")),
        case("unbalanced opens the longest suit",
             (new("Hand", ["SA", "S9", "S8", "HK", "HQ", "H8", "H7", "H6", "H5", "DA", "D3", "C7", "C2"], save="h"), obj("Hand")),
             (get("h", "hcp"), 13), (get("h", "shape"), "6-3-2-2"), (get("h", "balanced"), False), (call("h", "opening"), "1H")),
        case("equal lengths prefer the higher suit",
             (new("Hand", ["S9", "S8", "S7", "S6", "S5", "HA", "HK", "HQ", "H9", "H8", "DA", "D2", "C2"], save="h"), obj("Hand")),
             (get("h", "shape"), "5-5-2-1"), (call("h", "opening"), "1S")),
        case("unbalanced with 14 points",
             (new("Hand", ["SA", "SK", "SQ", "S8", "S7", "S6", "HA", "HJ", "H3", "D9", "D8", "D7", "C6"], save="h"), obj("Hand")),
             (get("h", "hcp"), 14), (get("h", "shape"), "6-3-3-1"), (call("h", "opening"), "1S"), (get("h", "losers"), 6)),
        case("balanced shapes",
             (new("Hand", ["S9", "S8", "S7", "S6", "S5", "H9", "H8", "H7", "D9", "D8", "D7", "C9", "C8"], save="h"), obj("Hand")),
             (get("h", "shape"), "5-3-3-2"), (get("h", "balanced"), True), (get("h", "hcp"), 0), (call("h", "opening"), "pass"),
             (get("h", "losers"), 11)),
        case("input order does not matter",
             (new("Hand", ["C3", "DA", "SK", "H5", "C4", "S2", "HJ", "D8", "SA", "HQ", "D9", "S7", "CK"], save="h"), obj("Hand")),
             (builtin("str", "h"), "S: AK72 | H: QJ5 | D: A98 | C: K43"), (get("h", "lengths"), {"S": 4, "H": 3, "D": 3, "C": 3})),
    ],
    "generate": lambda rng: (lambda cards: (
        [new("Hand", cards, save="h")]
        + [rng.choice([get("h", "hcp"), get("h", "shape"), get("h", "balanced"), get("h", "losers"), get("h", "lengths"),
                       builtin("str", "h"), call("h", "opening")])
           for _ in range(rng.randint(3, 7))]))(
        rng.sample(DECK, 13) if rng.random() < 0.85 else rng.choice([rng.sample(DECK, 12), rng.sample(DECK, 12) + ["Z9"],
                                                                     (lambda c: c + [c[0]])(rng.sample(DECK, 12))])),
    "mutations": [
        {"name": "queen counted in a doubleton", "old": '"AKQ"[:considered]', "new": '"AKQ"'},
        {"name": "ties prefer clubs", "old": 'return "1" + max(SUITS, key=lambda suit: lengths[suit])',
         "new": 'return "1" + max(SUITS[::-1], key=lambda suit: lengths[suit])'},
        {"name": "5-4-2-2 called balanced", "old": 'BALANCED = {"4-3-3-3", "4-4-3-2", "5-3-3-2"}',
         "new": 'BALANCED = {"4-3-3-3", "4-4-3-2", "5-3-3-2", "5-4-2-2"}'},
        {"name": "duplicates accepted", "old": "len(cards) != 13 or len(set(cards)) != 13", "new": "len(cards) != 13"},
    ],
    "sources": ["https://docs.python.org/3.11/library/functions.html#property",
                "https://docs.python.org/3.11/library/functions.html#max"],
}
