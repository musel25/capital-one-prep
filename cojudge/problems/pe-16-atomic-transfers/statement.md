# 16. Apply account transfers atomically

A balance service must apply each transfer without a partial debit or credit.

Implement `apply_transfers(balances, transfers)`. `balances` maps account names to integer cents. Each transfer has `from`, `to`, and `amount`. Process transfers in input order. Accept only when both accounts exist and the source has at least `amount` cents. On success, subtract from the source and add to the target as one atomic change. A self-transfer succeeds only when funds are sufficient and leaves the balance unchanged. Rejected transfers change no balances and create no accounts. Return `{"accepted": [...], "balances": {...}}` with one boolean per transfer and every final account balance. Empty inputs are allowed. Do not modify the inputs. Calls are independent.

**Constraints:**

- 0–300 accounts and 0–300 transfers. All required fields are present.
- Account names are nonempty ASCII strings of at most 80 characters.
- Initial balances are integers from 0 to 1000000000000 cents; amounts are integers from 1 to 1000000000000 cents.
- Inputs satisfy the contract; no validation is required.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `apply_transfers`. **Run** checks the examples. **Submit** checks all 17 cases.
