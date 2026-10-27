import java.util.*;
import java.math.*;
import java.time.*;
import java.time.format.*;
import java.util.regex.*;
import java.nio.charset.StandardCharsets;

class Marker extends Support {

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
String[] facts() { return new String[]{"property Player score", "property Player best", "property Player history"}; }
static class Player implements Obj {
    String name; long score = 0, best = 0; List<Object> history = new ArrayList<>(List.of(0L));
    public String type() { return "Player"; }
    void setScore(Object v) {
        if (!isInt(v)) throw err("TypeError");
        long x = lng(v);
        if (x < 0) throw err("ValueError");
        score = x; best = Math.max(best, x); history.add(x);
    }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    if (d.equals("new")) { Player p = new Player(); p.name = s(arg(op, 0, "name", MISSING)); return p; }
    Object t = target(op);
    if (t instanceof List && d.equals("call") && s(op.get("method")).equals("append")) { arr(t).add(args(op).get(0)); return null; }
    if (t instanceof List && d.equals("len")) return (long) arr(t).size();
    Player p = (Player) t;
    String a = op.containsKey("attr") ? s(op.get("attr")) : "";
    if (d.equals("get")) {
        if (a.equals("name")) return p.name;
        if (a.equals("score")) return p.score;
        if (a.equals("best")) return p.best;
        if (a.equals("history")) return new ArrayList<>(p.history);
        throw err("AttributeError");
    }
    if (d.equals("set")) {
        if (a.equals("best") || a.equals("history")) throw err("AttributeError");
        if (a.equals("score")) p.setScore(val(op.get("value")));
        if (a.equals("name")) p.name = s(val(op.get("value")));
        return null;
    }
    if (d.equals("call") && s(op.get("method")).equals("reset")) { p.setScore(0L); return null; }
    throw err("AttributeError");
}

    public String run(String payload) { return J.dump(solve(obj(J.parse(payload)))); }
    public boolean isCorrect(String payload, String output) {
        try { return J.equal(J.parse(run(payload)), J.parse(output)); }
        catch (Exception error) { return false; }
    }
}

/** Small, strict JSON codec. Each published marker is self-contained. */
class Support {
    @SuppressWarnings("unchecked") static Map<String,Object> obj(Object x) { return (Map<String,Object>) x; }
    @SuppressWarnings("unchecked") static List<Object> arr(Object x) { return (List<Object>) x; }
    static String s(Object x) { return (String) x; }
    static int n(Object x) { return ((Number) x).intValue(); }
    static long lng(Object x) { return ((Number) x).longValue(); }
    static boolean isInteger(Object x) {
        return x instanceof BigInteger || x instanceof Byte || x instanceof Short || x instanceof Integer || x instanceof Long;
    }
    static boolean b(Object x) { return (Boolean) x; }
    static Map<String,Object> map(Object... pairs) {
        if (pairs.length % 2 != 0) throw new IllegalArgumentException("Unpaired map key");
        Map<String,Object> out = new LinkedHashMap<>();
        for (int i = 0; i < pairs.length; i += 2) out.put((String) pairs[i], pairs[i + 1]);
        return out;
    }
    static List<Object> list(Object... values) { return new ArrayList<>(Arrays.asList(values)); }
}

class J {
    private final String text;
    private int pos;
    private J(String text) { this.text = text; }
    static Object parse(String text) {
        J reader = new J(text);
        Object out = reader.value();
        reader.space();
        if (reader.pos != text.length()) throw new IllegalArgumentException("Trailing JSON data");
        return out;
    }
    private void space() {
        while (pos < text.length() && " \n\r\t".indexOf(text.charAt(pos)) >= 0) pos++;
    }
    private char take() {
        if (pos >= text.length()) throw new IllegalArgumentException("Unexpected end of JSON");
        return text.charAt(pos++);
    }
    private boolean consume(char ch) {
        space();
        if (pos < text.length() && text.charAt(pos) == ch) { pos++; return true; }
        return false;
    }
    private void require(char ch) {
        if (!consume(ch)) throw new IllegalArgumentException("Expected " + ch);
    }
    private Object value() {
        space();
        if (pos >= text.length()) throw new IllegalArgumentException("Missing JSON value");
        char ch = text.charAt(pos);
        if (ch == '"') return string();
        if (ch == '{') {
            pos++;
            Map<String,Object> out = new LinkedHashMap<>();
            if (consume('}')) return out;
            do {
                space();
                String key = string();
                require(':');
                if (out.containsKey(key)) throw new IllegalArgumentException("Duplicate JSON key");
                out.put(key, value());
            } while (consume(','));
            require('}');
            return out;
        }
        if (ch == '[') {
            pos++;
            List<Object> out = new ArrayList<>();
            if (consume(']')) return out;
            do { out.add(value()); } while (consume(','));
            require(']');
            return out;
        }
        for (String word : new String[]{"true", "false", "null"}) {
            if (text.startsWith(word, pos)) {
                pos += word.length();
                return word.equals("null") ? null : Boolean.valueOf(word);
            }
        }
        java.util.regex.Matcher match = java.util.regex.Pattern
            .compile("-?(?:0|[1-9][0-9]*)(?:\\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
            .matcher(text.substring(pos));
        if (!match.lookingAt()) throw new IllegalArgumentException("Invalid JSON value");
        pos += match.end();
        String token = match.group();
        if (!token.contains(".") && !token.contains("e") && !token.contains("E")) return new BigInteger(token);
        BigDecimal decimal = new BigDecimal(token);
        // Preserve a floating JSON token when a parsed value is encoded again.
        return decimal.scale() <= 0 ? decimal.setScale(1) : decimal;
    }
    private String string() {
        if (take() != '"') throw new IllegalArgumentException("Expected JSON string");
        StringBuilder out = new StringBuilder();
        while (true) {
            char ch = take();
            if (ch == '"') return out.toString();
            if (ch < 32) throw new IllegalArgumentException("Unescaped control character");
            if (ch != '\\') { out.append(ch); continue; }
            char escape = take();
            switch (escape) {
                case '"': case '\\': case '/': out.append(escape); break;
                case 'b': out.append('\b'); break;
                case 'f': out.append('\f'); break;
                case 'n': out.append('\n'); break;
                case 'r': out.append('\r'); break;
                case 't': out.append('\t'); break;
                case 'u':
                    if (pos + 4 > text.length()) throw new IllegalArgumentException("Short Unicode escape");
                    String hex = text.substring(pos, pos + 4);
                    if (!hex.matches("[0-9a-fA-F]{4}")) throw new IllegalArgumentException("Invalid Unicode escape");
                    out.append((char) Integer.parseInt(hex, 16));
                    pos += 4;
                    break;
                default: throw new IllegalArgumentException("Invalid JSON escape");
            }
        }
    }
    static String dump(Object x) {
        if (x == null) return "null";
        if (x instanceof String) {
            StringBuilder out = new StringBuilder("\"");
            for (char ch : ((String) x).toCharArray()) {
                if (ch == '"' || ch == '\\') out.append('\\').append(ch);
                else if (ch < 32) out.append(String.format("\\u%04x", (int) ch));
                else out.append(ch);
            }
            return out.append('"').toString();
        }
        if (x instanceof Boolean) return x.toString();
        if (x instanceof Number) return new BigDecimal(x.toString()).toPlainString();
        if (x instanceof Map<?,?>) {
            List<String> entries = new ArrayList<>();
            for (Map.Entry<?,?> e : ((Map<?,?>) x).entrySet()) {
                if (!(e.getKey() instanceof String)) throw new IllegalArgumentException("JSON key must be a string");
                entries.add(dump(e.getKey()) + ":" + dump(e.getValue()));
            }
            return "{" + String.join(",", entries) + "}";
        }
        if (x instanceof Iterable<?>) {
            List<String> entries = new ArrayList<>();
            for (Object value : (Iterable<?>) x) entries.add(dump(value));
            return "[" + String.join(",", entries) + "]";
        }
        if (x.getClass().isArray()) {
            List<String> entries = new ArrayList<>();
            for (int i = 0; i < java.lang.reflect.Array.getLength(x); i++)
                entries.add(dump(java.lang.reflect.Array.get(x, i)));
            return "[" + String.join(",", entries) + "]";
        }
        throw new IllegalArgumentException("Not a JSON value: " + x.getClass());
    }
    static boolean equal(Object a, Object b) {
        if (a == null || b == null) return a == b;
        if (a instanceof Number && b instanceof Number)
            return new BigDecimal(a.toString()).compareTo(new BigDecimal(b.toString())) == 0;
        if (a instanceof Map<?,?> && b instanceof Map<?,?>) {
            Map<?,?> x = (Map<?,?>) a, y = (Map<?,?>) b;
            if (!x.keySet().equals(y.keySet())) return false;
            for (Object key : x.keySet()) if (!equal(x.get(key), y.get(key))) return false;
            return true;
        }
        if (a instanceof List<?> && b instanceof List<?>) {
            List<?> x = (List<?>) a, y = (List<?>) b;
            if (x.size() != y.size()) return false;
            for (int i = 0; i < x.size(); i++) if (!equal(x.get(i), y.get(i))) return false;
            return true;
        }
        return a.getClass() == b.getClass() && a.equals(b);
    }
}
