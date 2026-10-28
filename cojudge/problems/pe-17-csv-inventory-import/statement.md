The inventory importer must preserve quoted SKU data while it converts quantities to integers.

Implement parse_inventory(csv_text). The first CSV record has exactly the fields sku and quantity, in that order. The text has valid CSV syntax with LF or CRLF record endings. Quoted fields may contain commas, escaped double quotes or newlines. Every nonblank data record has exactly two fields. A SKU is a nonempty ASCII string; preserve it exactly, including spaces and quoted newlines. A quantity is a canonical non-negative decimal integer: 0, or digits without a leading zero. Return a list of {'sku': string, 'quantity': integer} objects in record order. Keep duplicate SKUs as separate records. Use the standard-library csv.reader. Skip fully blank records, which csv.reader returns as empty lists. A blank physical line inside a quoted field belongs to that field. A header-only file returns an empty list. A final record ending is optional. Do not validate malformed CSV; it is outside the contract.

**Constraints:**

- At most 100 data records; each SKU contains 1–200 ASCII characters.
- Quantities are integers from 0 through 1000000000; csv_text has at most 30000 characters.
- The header and all records satisfy the stated CSV contract. Each call is independent.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `parse_inventory`. **Run** checks the examples. **Submit** checks all 15 cases.
