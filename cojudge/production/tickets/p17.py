"""Import inventory records from valid CSV data."""

CASES = [
    {"input": {"csv_text": "sku,quantity\nA-1,3\nB-2,0\n"}, "expected": [{"sku": "A-1", "quantity": 3}, {"sku": "B-2", "quantity": 0}], "label": "read ordered inventory rows"},
    {"input": {"csv_text": 'sku,quantity\n"A,B",12\n'}, "expected": [{"sku": "A,B", "quantity": 12}], "label": "quoted SKU contains a comma"},
    {"input": {"csv_text": 'sku,quantity\n"A""B",5\n'}, "expected": [{"sku": 'A"B', "quantity": 5}], "label": "escaped double quote inside a quoted SKU"},
    {"input": {"csv_text": "sku,quantity"}, "expected": [], "label": "header without final newline"},
    {"input": {"csv_text": "sku,quantity\n"}, "expected": [], "label": "header with final newline"},
    {"input": {"csv_text": "sku,quantity\r\nA,2\r\nB,4\r\n"}, "expected": [{"sku": "A", "quantity": 2}, {"sku": "B", "quantity": 4}], "label": "CRLF record endings"},
    {"input": {"csv_text": "sku,quantity\n\nA,1\n\n\nB,2\n\n"}, "expected": [{"sku": "A", "quantity": 1}, {"sku": "B", "quantity": 2}], "label": "skip fully blank records"},
    {"input": {"csv_text": 'sku,quantity\n"multi\nline",7\n'}, "expected": [{"sku": "multi\nline", "quantity": 7}], "label": "quoted SKU spans physical lines"},
    {"input": {"csv_text": 'sku,quantity\r\n"multi\r\nline",7\r\n'}, "expected": [{"sku": "multi\r\nline", "quantity": 7}], "label": "preserve CRLF inside a quoted SKU"},
    {"input": {"csv_text": 'sku,quantity\n"a\n\nb",2\n\n'}, "expected": [{"sku": "a\n\nb", "quantity": 2}], "label": "blank physical line within a quoted field is data"},
    {"input": {"csv_text": "sku,quantity\n  A  ,1000000000"}, "expected": [{"sku": "  A  ", "quantity": 1000000000}], "label": "preserve SKU spacing and upper quantity bound"},
    {"input": {"csv_text": 'sku,quantity\n"Q","0"'}, "expected": [{"sku": "Q", "quantity": 0}], "label": "quoted quantity is converted to an integer"},
    {"input": {"csv_text": "sku,quantity\nA,1\nA,2"}, "expected": [{"sku": "A", "quantity": 1}, {"sku": "A", "quantity": 2}], "label": "duplicate SKU records remain separate"},
    {"input": {"csv_text": 'sku,quantity\n"comma, quote"" and\nnewline",10\n'}, "expected": [{"sku": 'comma, quote" and\nnewline', "quantity": 10}], "label": "combined quoted field features"},
    {"input": {"csv_text": "sku,quantity\r\n\r\n\r\n"}, "expected": [], "label": "header followed only by CRLF blank records"},
]

SPEC = {
    "number": 17,
    "slug": "csv-inventory-import",
    "title": "Parse an inventory CSV import",
    "difficulty": "Medium",
    "category": "05-files-time-and-boundaries",
    "ticket": "The inventory importer must preserve quoted SKU data while it converts quantities to integers.",
    "task": "Implement parse_inventory(csv_text). The first CSV record has exactly the fields sku and quantity, in that order. The text has valid CSV syntax with LF or CRLF record endings. Quoted fields may contain commas, escaped double quotes or newlines. Every nonblank data record has exactly two fields. A SKU is a nonempty ASCII string; preserve it exactly, including spaces and quoted newlines. A quantity is a canonical non-negative decimal integer: 0, or digits without a leading zero. Return a list of {'sku': string, 'quantity': integer} objects in record order. Keep duplicate SKUs as separate records. Use the standard-library csv.reader. Skip fully blank records, which csv.reader returns as empty lists. A blank physical line inside a quoted field belongs to that field. A header-only file returns an empty list. A final record ending is optional. Do not validate malformed CSV; it is outside the contract.",
    "constraints": ["At most 100 data records; each SKU contains 1–200 ASCII characters.", "Quantities are integers from 0 through 1000000000; csv_text has at most 30000 characters.", "The header and all records satisfy the stated CSV contract. Each call is independent."],
    "function": "parse_inventory",
    "starter": "def parse_inventory(csv_text):\n    raise NotImplementedError\n",
    "cases": CASES,
}

SPEC["reference"] = '''import csv
import io


def parse_inventory(csv_text):
    rows = csv.reader(io.StringIO(csv_text, newline=""))
    next(rows, None)
    return [{"sku": row[0], "quantity": int(row[1])} for row in rows if row]
'''

SPEC["java"] = r'''private List<List<String>> csvRecords(String text) {
    List<List<String>> rows = new ArrayList<>();
    List<String> fields = new ArrayList<>();
    StringBuilder field = new StringBuilder();
    boolean quoted = false, started = false;
    for (int i = 0; i < text.length(); i++) {
        char ch = text.charAt(i);
        if (quoted) {
            if (ch == '"') {
                if (i + 1 < text.length() && text.charAt(i + 1) == '"') {
                    field.append('"');
                    i++;
                } else quoted = false;
            } else field.append(ch);
            continue;
        }
        if (ch == '"') {
            quoted = true;
            started = true;
        } else if (ch == ',') {
            fields.add(field.toString());
            field.setLength(0);
            started = true;
        } else if (ch == '\r' || ch == '\n') {
            if (started) {
                fields.add(field.toString());
                rows.add(new ArrayList<>(fields));
            }
            fields.clear();
            field.setLength(0);
            started = false;
            if (ch == '\r' && i + 1 < text.length() && text.charAt(i + 1) == '\n') i++;
        } else {
            field.append(ch);
            started = true;
        }
    }
    if (started) {
        fields.add(field.toString());
        rows.add(fields);
    }
    return rows;
}

public Object solve(Map<String,Object> d) {
    List<List<String>> rows = csvRecords(s(d.get("csv_text")));
    List<Object> result = new ArrayList<>();
    for (int i = 1; i < rows.size(); i++) {
        List<String> row = rows.get(i);
        result.add(map("sku", row.get(0), "quantity", Integer.parseInt(row.get(1))));
    }
    return result;
}
'''

SPEC["mutations"] = [
    {"name": "split physical lines instead of reading CSV", "old": 'rows = csv.reader(io.StringIO(csv_text, newline=""))', "new": 'rows = (line.split(",") for line in csv_text.splitlines())'},
    {"name": "treat blank records as data", "old": 'for row in rows if row', "new": 'for row in rows'},
    {"name": "strip SKU whitespace", "old": '"sku": row[0]', "new": '"sku": row[0].strip()'},
    {"name": "return quantity strings", "old": 'int(row[1])', "new": 'row[1]'},
    {"name": "skip first data record", "old": 'next(rows, None)', "new": 'next(rows, None)\n    next(rows, None)'},
]
