The inventory importer must preserve quoted SKU data while it converts quantities to integers.

Implement `parse_inventory(csv_text)` with `csv.reader`. Return `{'sku': STRING, 'quantity': INTEGER}` records in CSV order. Keep duplicate SKUs separate.

The first CSV record contains exactly `sku` and `quantity`, in that order. Preserve each SKU exactly, including spaces, quoted commas, escaped double quotes, and quoted newlines. Convert each quantity to an integer.

Skip fully blank records, which `csv.reader` returns as empty lists. A blank physical line inside a quoted field belongs to that field. A header-only file returns an empty list. A final record ending is optional.

**Constraints:**

- At most 100 data records; each SKU contains 1–200 ASCII characters.
- Quantities are integers from 0 through 1000000000; csv_text has at most 30000 characters.
- CSV syntax is valid, with LF or CRLF record endings. Every nonblank data record has two fields. Quantities use canonical nonnegative decimal notation: `0`, or digits without a leading zero.
- Do not change input objects or their nested values. Each call starts with fresh state.
