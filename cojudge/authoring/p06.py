"""Original constructed exercise; not employer interview material."""

SPEC = {'number': 6,
 'slug': 'csv-account-totals',
 'title': 'Read quoted CSV records',
 'difficulty': 'Easy',
 'time': 20,
 'prerequisites': 'Lists, dictionaries, and functions.',
 'learn': 'CSV fields can contain commas, quotes, and line breaks. Splitting text at commas or '
          'splitting it into lines before parsing destroys those fields. The csv module reads '
          'records according to the quoting rules. A quoted double quote is written as two double '
          'quotes. Open a text stream with newline handling that lets the CSV reader see the '
          'original line endings. The reader returns strings, so convert a numeric column only '
          'after parsing the record. Keep aggregation separate from parsing. A dictionary '
          'preserves the first insertion order of account IDs, which gives a simple way to return '
          'totals in first-seen order.',
 'task': ('**Input:** `data` has:\n'
    '- `csv`: valid CSV text.\n'
    '  - The first record (the header) is exactly `account,amount`.\n'
    '  - Every later record has exactly two fields.\n'
    '  - `account` is a string of at most 1,000 characters. It can be empty or contain a comma, a quote, or a line break.\n'
    '  - `amount` is an ASCII integer string, optionally negative, with absolute value at most 1,000,000. It has at most 20 characters, including any sign and leading zeros.\n'
    '  - Standard double-quote escaping applies: `""` inside a quoted field is one `"`.\n'
    '  - Records are separated by LF or CRLF. There are no blank records. The last record may have no separator.\n'
    '\n'
    '**Return** a list of `{"account": string, "total": int}`\n'
    "- `total` is the sum of that account's amounts.\n"
    '- Accounts are in the order they first appear.'),
 'constraints': ['At most 100 data records after the header.',
                 'Each decoded account field has at most 1,000 characters. Each amount field has '
                 'at most 20 characters.',
                 'The complete CSV text has at most 200,000 characters. All text follows the '
                 'stated valid CSV format.'],
 'hints': ['Pass the complete text stream to csv.reader.',
           'Use a dictionary to accumulate totals without changing first-seen order.'],
 'starter': 'def solve(data: dict) -> list[dict]:\n    raise NotImplementedError\n',
 'reference': 'import csv\n'
              'from io import StringIO\n'
              '\n'
              'def solve(data: dict) -> list[dict]:\n'
              "    records = csv.reader(StringIO(data['csv'], newline=''))\n"
              '    next(records)\n'
              '    totals = {}\n'
              '    for account, amount in records:\n'
              '        totals[account] = totals.get(account, 0) + int(amount)\n'
              "    return [{'account': account, 'total': total} for account, total in "
              'totals.items()]\n',
 'java': 'private List<List<String>> csvRows(String text) {\n'
         '    List<List<String>> rows=new ArrayList<>(); List<String> row=new ArrayList<>(); '
         'StringBuilder field=new StringBuilder(); boolean quoted=false;\n'
         '    for(int i=0;i<text.length();i++) {\n'
         '        char c=text.charAt(i);\n'
         '        if(c==\'"\') { if(quoted && i+1<text.length() && text.charAt(i+1)==\'"\') { '
         'field.append(\'"\'); i++; } else quoted=!quoted; }\n'
         "        else if(c==',' && !quoted) { row.add(field.toString()); field.setLength(0); }\n"
         "        else if(c=='\\n' && !quoted) { row.add(field.toString()); rows.add(row); row=new "
         'ArrayList<>(); field.setLength(0); }\n'
         "        else if(c=='\\r' && !quoted) { }\n"
         '        else field.append(c);\n'
         '    }\n'
         '    if(field.length()>0 || !row.isEmpty()) { row.add(field.toString()); rows.add(row); '
         '}\n'
         '    return rows;\n'
         '}\n'
         'public Object solve(Map<String,Object> d) {\n'
         '    List<List<String>> rows=csvRows(s(d.get("csv"))); Map<String,Long> totals=new '
         'LinkedHashMap<>();\n'
         '    for(int i=1;i<rows.size();i++) { List<String> r=rows.get(i); '
         'totals.merge(r.get(0),Long.parseLong(r.get(1)),Long::sum); }\n'
         '    List<Object> out=new ArrayList<>(); for(Map.Entry<String,Long> e:totals.entrySet()) '
         'out.add(map("account",e.getKey(),"total",e.getValue())); return out;\n'
         '}',
 'approach': 'The reference uses csv.reader, then one dictionary for totals. Time is O(c), where c '
             'is the text length. Space is O(c + k) for the input stream and k accounts. Tests '
             'cover quoted commas, quotes, and embedded line breaks. The output judge cannot '
             'certify use of csv. This exercise assumes valid CSV and does not define '
             'malformed-file recovery.',
 'cases': [{'input': {'csv': 'account,amount\n"Acme, West",10\nBeta,3\n"Acme, West",-4\n'},
            'expected': [{'account': 'Acme, West', 'total': 6}, {'account': 'Beta', 'total': 3}],
            'label': 'quoted comma and repeated account'},
           {'input': {'csv': 'account,amount\n"a""b",7\n"line\nbreak",2\n'},
            'expected': [{'account': 'a"b', 'total': 7}, {'account': 'line\nbreak', 'total': 2}],
            'label': 'quote and embedded line break'},
           {'input': {'csv': 'account,amount\n'}, 'expected': [], 'label': 'header only'},
           {'input': {'csv': 'account,amount\nA,0'},
            'expected': [{'account': 'A', 'total': 0}],
            'label': 'no final newline'},
           {'input': {'csv': 'account,amount\r\nA,1\r\nB,2\r\n'},
            'expected': [{'account': 'A', 'total': 1}, {'account': 'B', 'total': 2}],
            'label': 'CRLF records'},
           {'input': {'csv': 'account,amount\n,5\n,6\n'},
            'expected': [{'account': '', 'total': 11}],
            'label': 'empty account'},
           {'input': {'csv': 'account,amount\nZ,1\nA,2\nZ,3\n'},
            'expected': [{'account': 'Z', 'total': 4}, {'account': 'A', 'total': 2}],
            'label': 'first seen order'},
           {'input': {'csv': 'account,amount\nA,-5\nA,5\n'},
            'expected': [{'account': 'A', 'total': 0}],
            'label': 'zero total is retained'},
           {'input': {'csv': 'account,amount\n" spaces ","0007"\n'},
            'expected': [{'account': ' spaces ', 'total': 7}],
            'label': 'preserve account spaces'},
           {'input': {'csv': 'account,amount\n"x\r\ny",-2\n'},
            'expected': [{'account': 'x\r\ny', 'total': -2}],
            'label': 'CRLF within a quoted field'},
           {'input': {'csv': 'account,amount\nA,1000000\nA,1000000\n'},
            'expected': [{'account': 'A', 'total': 2000000}],
            'label': 'large sum'},
           {'input': {'csv': 'account,amount'},
            'expected': [],
            'label': 'header without final newline'},
           {'input': {'csv': 'account,amount\n"""",1\n"a,b,c",2\n'},
            'expected': [{'account': '"', 'total': 1}, {'account': 'a,b,c', 'total': 2}],
            'label': 'one quote and several commas'},
           {'input': {'csv': 'account,amount\n'
                             'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx,1\n'
                             'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx,2\n'},
            'expected': [{'account': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                          'total': 3}],
            'label': 'account field at the 1,000-character limit'},
           {'input': {'csv': 'account,amount\nA,00000000000000000001\n'},
            'expected': [{'account': 'A', 'total': 1}],
            'label': 'amount field at the 20-character limit'}],
 'generated': [{'csv': 'account,amount\n"Group,0",1\nOther,0\n"Group,0",2\n'},
               {'csv': 'account,amount\n"Group,1",2\nOther,-1\n"Group,1",2\n'},
               {'csv': 'account,amount\n"Group,2",3\nOther,-2\n"Group,2",2\n'},
               {'csv': 'account,amount\n"Group,3",4\nOther,-3\n"Group,3",2\n'},
               {'csv': 'account,amount\n"Group,4",5\nOther,-4\n"Group,4",2\n'},
               {'csv': 'account,amount\n"Group,5",6\nOther,-5\n"Group,5",2\n'},
               {'csv': 'account,amount\n"Group,6",7\nOther,-6\n"Group,6",2\n'},
               {'csv': 'account,amount\n"Group,7",8\nOther,-7\n"Group,7",2\n'},
               {'csv': 'account,amount\n"Group,8",9\nOther,-8\n"Group,8",2\n'},
               {'csv': 'account,amount\n"Group,9",10\nOther,-9\n"Group,9",2\n'},
               {'csv': 'account,amount\n"Group,10",11\nOther,-10\n"Group,10",2\n'},
               {'csv': 'account,amount\n"Group,11",12\nOther,-11\n"Group,11",2\n'}],
 'mutations': [{'name': 'overwrites repeated account total',
                'old': 'totals.get(account, 0) + int(amount)',
                'new': 'int(amount)'}],
 'sources': ['https://docs.python.org/3.11/library/csv.html']}
